#!/usr/bin/env python3
"""审计竞赛雷达 —— 扫「真钱赛道」，找正在开放/即将开放的比赛与常驻赏金。

为什么上云：手机没电/卡住时本地定时器会死；GitHub Actions 不依赖手机。

判据：只关心「还能进场的」——Live / Upcoming / 常驻 bug bounty。
付费赛道（竞技审计）目前四家轮换，需要 6 小时级盯梢才有机会抢到开场。
"""
import json, os, re, sys, urllib.request, datetime

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
STATE = os.path.join(os.path.dirname(__file__), "..", "state", "audit_radar.json")
REPORT = os.path.join(os.path.dirname(__file__), "..", "reports", "audit_radar_latest.json")


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")


def strip(h):
    h = re.sub(r"<script.*?</script>|<style.*?</style>|<svg.*?</svg>", " ", h, flags=re.S)
    t = re.sub(r"<[^>]+>", "|", h)
    import html as H
    t = H.unescape(t)
    return re.sub(r"\s+", " ", re.sub(r"\|+", "|", t))


# ---------- 各源 ----------

def src_code4rena():
    """Code4rena 有 JSON API —— 最可靠的一个"""
    out = []
    try:
        d = json.loads(get("https://code4rena.com/api/v1/audits"))
        for a in d.get("data", {}).get("audits", []):
            st = (a.get("status") or "").lower()
            if st in ("active", "upcoming", "reporting"):
                out.append({"src": "code4rena", "status": st,
                            "title": a.get("title"),
                            "org": a.get("org"), "amount": a.get("formattedAmount"),
                            "url": "https://code4rena.com/audits/" + (a.get("slug") or "")})
    except Exception as e:
        out.append({"src": "code4rena", "error": str(e)})
    return out


def src_sherlock_contests():
    out = []
    try:
        t = strip(get("https://audits.sherlock.xyz/contests"))
        m = re.search(r"Contests\|All\|(\d+)\|Active\|Upcoming", t)
        if m:
            active, up = int(m.group(1)), 0
            m2 = re.search(r"\|Active\|(\d+)\|Upcoming", t)
            if m2:
                up = int(m2.group(1))
            out.append({"src": "sherlock", "status": "counts",
                        "active": active, "upcoming": up,
                        "url": "https://audits.sherlock.xyz/contests"})
    except Exception as e:
        out.append({"src": "sherlock", "error": str(e)})
    return out


def src_codehawks():
    out = []
    try:
        t = strip(get("https://codehawks.cyfrin.io/contests"))
        # 抓 "Public|Live|标题|主办|奖金" 这类片段
        for m in re.finditer(r"(Live|Upcoming)\|([^|]{3,60})\|([^|]{2,40})\|([\d,\.]+)\|(USDC|ETH|OP)", t):
            out.append({"src": "codehawks", "status": m.group(1).lower(),
                        "title": m.group(2).strip(), "org": m.group(3).strip(),
                        "amount": f"{m.group(4)} {m.group(5)}",
                        "url": "https://codehawks.cyfrin.io/contests"})
        if not out:
            out.append({"src": "codehawks", "status": "none-live"})
    except Exception as e:
        out.append({"src": "codehawks", "error": str(e)})
    return out


def src_sherlock_bounties():
    """常驻赏金 —— 不空窗，真钱在这"""
    out = []
    try:
        t = strip(get("https://audits.sherlock.xyz/bug-bounties"))
        # 实际格式: 标题|Last Updated • Apr 8, 2025|16,000,000 USDC|Payout
        for m in re.finditer(r"([^|]{3,45}?)\|Last Updated • ([\w]{3} \d{1,2}, \d{4})\|([\d,]+) (USDC|USD)\|Payout", t):
            out.append({"src": "sherlock-bounty", "status": "live",
                        "title": m.group(1).strip(), "updated": m.group(2),
                        "amount": "$" + m.group(3), "url": "https://audits.sherlock.xyz/bug-bounties"})
    except Exception as e:
        out.append({"src": "sherlock-bounty", "error": str(e)})
    return out[:20]


def src_immunefi():
    out = []
    try:
        t = strip(get("https://immunefi.com/bug-bounty/"))
        m = re.search(r"Showing all (\d+) bounty programs", t)
        n = int(m.group(1)) if m else None
        rows = []
        for mm in re.finditer(r"([A-Z][\w \.\-]{2,40})\|(Triaged by \|Immunefi\|)?(?:Private|\$[\d\.]+k|\$[\d\.]+M)\|\$([\d\.]+[kM])\|", t):
            rows.append({"title": mm.group(1).strip(), "max": "$" + mm.group(3)})
        out.append({"src": "immunefi", "status": "live", "programs": n, "top": rows[:12],
                    "url": "https://immunefi.com/bug-bounty/?filter=KYC+"})
    except Exception as e:
        out.append({"src": "immunefi", "error": str(e)})
    return out


SOURCES = [src_code4rena, src_sherlock_contests, src_codehawks, src_sherlock_bounties, src_immunefi]


def main():
    res = []
    for f in SOURCES:
        try:
            res.extend(f())
        except Exception as e:
            res.append({"src": f.__name__, "error": repr(e)})

    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)

    # 状态 diff：找新出现的「可进场」条目
    try:
        prev = json.load(open(STATE)) if os.path.exists(STATE) else {}
    except Exception:
        prev = {}
    seen = set(prev.get("keys", []))
    new = []
    keys = []
    for r in res:
        if r.get("error") or r.get("status") == "none-live":
            continue
        k = f"{r.get('src')}|{r.get('title') or r.get('programs')}"
        keys.append(k)
        if k not in seen:
            new.append(r)

    payload = {"at": datetime.datetime.utcnow().isoformat() + "Z",
               "count": len(res), "new": new, "all": res}
    json.dump({"keys": keys}, open(STATE, "w"), indent=1)
    json.dump(payload, open(REPORT, "w"), indent=1, ensure_ascii=False)

    print(f"[audit-radar] {datetime.datetime.utcnow():%Y-%m-%d %H:%MZ} sources={len(res)} new={len(new)}")
    for r in res:
        if r.get("error"):
            print("  ERR", r["src"], r["error"][:80])
        elif r.get("status") == "counts":
            print(f"  sherlock contests: active={r['active']} upcoming={r['upcoming']}")
        elif r.get("status") == "none-live":
            print("  codehawks: 0 live")
        elif r["src"] == "sherlock-bounty":
            print(f"  bounty: {r['title'][:38]:<40} {r['amount']}")
        elif r["src"] == "immunefi":
            print(f"  immunefi: {r.get('programs')} programs")
        else:
            print(f"  {r['src']}: {r.get('status')} {str(r.get('title'))[:40]} {r.get('amount','')}")
    if new:
        print(f"  🆕 NEW: {len(new)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
