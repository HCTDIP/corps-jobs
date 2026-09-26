#!/usr/bin/env python3
"""Railway 赏金榜云端雷达 —— 用 Playwright 渲染 JS 页面后提取榜单。

为什么必须浏览器：station.railway.com/bounties 是纯客户端渲染，
curl 拿到的是空壳（0 个 /questions/ 链接），没有可用的 JSON 接口。

跑在 GitHub Actions 上 → 手机没电/卡死也不断线。
"""
import json, os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
STATE = os.path.join(ROOT, "state", "railway_bounty.json")
REPORT = os.path.join(ROOT, "reports", "railway_bounty_latest.json")

EXTRACT = """
() => {
  const out = [...document.querySelectorAll('a[href*="/questions/"]')].map(a => ({
    h: a.getAttribute('href'),
    t: (a.innerText || '').replace(/\\s+/g, ' ').trim().slice(0, 160)
  }));
  const seen = {}; const uniq = [];
  out.forEach(o => { if (!seen[o.h]) { seen[o.h] = 1; uniq.push(o); } });
  return uniq;
}
"""

# 平台基建事故 / 需官方介入 —— 社区解不了（与本地 radar.py 的 DEAD 名单同源）
INFRA = ["anycast", "misrout", "latency", "disk i/o", "i/o degradation", "blackhole",
         "outage", "slow", "performance issue", "internal registry", "point-in-time",
         "dns issue", "region impacting", "healthcheck", "48s", "ingress metadata",
         "hmrc", "backup restore", "system performance", "arangodb", "mongodb",
         "build failing", "csr", "volume restore", "domain problem", "n8n",
         "steadfast-education", "runtime-v2", "deploy-nodes", "deployment-fails"]
# 我们的强项：提问 / 配置 / API 型
STRONG = ["how do i", "how can i", "is there", "can railway", "clarif", "supported",
          "environment", "config", "variable", " api", " cli", " ssh", "token",
          "scope", "sync", "permission", "certificate"]


def score(item):
    t = (item.get("t") or "").lower()
    s, notes = 0, []
    m = re.search(r"\b(\d+)([mhd])\b", t)
    if m:
        n, u = int(m.group(1)), m.group(2)
        if u == "h":
            s += 3; notes.append("数小时内")
        elif u == "d" and n <= 2:
            s += 2; notes.append(f"{n}天内")
        else:
            s -= 3; notes.append("陈旧")
    r = re.search(r"(\d+)\s*repl", t)
    n = int(r.group(1)) if r else 0
    if n <= 2:
        s += 2; notes.append("竞争低")
    else:
        s -= 1; notes.append(f"已{n}回复")
    if any(k in t for k in INFRA):
        s -= 4; notes.append("⚠平台基建/已解")
    if any(k in t for k in STRONG):
        s += 2; notes.append("提问·配置型")
    return s, notes


def main():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 390, "height": 844})
        pg.goto("https://station.railway.com/bounties", wait_until="networkidle", timeout=60000)
        pg.wait_for_timeout(3000)
        items = pg.evaluate(EXTRACT)
        b.close()

    for it in items:
        it["score"], it["notes"] = score(it)
    items.sort(key=lambda x: -x["score"])
    hot = [x for x in items if x["score"] >= 3]

    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    try:
        prev = json.load(open(STATE))
    except Exception:
        prev = {}
    seen = set(prev.get("slugs", []))
    new = [x for x in items if x["h"] not in seen]
    json.dump({"slugs": [x["h"] for x in items]}, open(STATE, "w"), indent=1)
    json.dump({"at": datetime.datetime.now(datetime.UTC).isoformat(),
               "total": len(items), "hot": hot, "new": new, "all": items},
              open(REPORT, "w"), indent=1, ensure_ascii=False)

    print(f"[railway-radar] {datetime.datetime.now(datetime.UTC):%Y-%m-%d %H:%MZ} "
          f"total={len(items)} hot={len(hot)} new={len(new)}")
    for x in new:
        print(f"  🆕 {x['t'][:100]}")
    for x in hot:
        print(f"  [{x['score']:+d}] {x['t'][:88]}")
        print(f"        {', '.join(x['notes'])}")
    if not hot:
        print("  0 条值得抢")
    # 供 workflow 判是否需要开 issue
    open(os.path.join(ROOT, "reports", "_hot_count.txt"), "w").write(str(len(hot) + len(new)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
