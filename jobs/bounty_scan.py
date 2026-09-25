#!/usr/bin/env python3
"""外部赏金平台扫描器（替代已废弃的 GitHub 监控线）

目标：每轮扫一遍"外面"的赏金平台，挑出**新出现的、可能可做的**任务。
设计原则（来自 2026-09-23 尽调教训）：
  1. 只要真人出钱的平台，不要 agent 自嗨圈
  2. 必须能判断地区限制（Superteam 的 GLOBAL 标签不可信，看 sponsor.chapter）
  3. 低竞争优先（提交数少的）
  4. 输出差异（只报新出现的），不做全文倾倒

用法: python3 bounty_scan.py
状态: /var/minis/workspace/bounty-hunt/external_state.json
"""
import json, os, re, urllib.request, datetime

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"
import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
STATE = os.environ.get("BOUNTY_STATE") or str(ROOT / "state" / "external_state.json")
REPORTS = pathlib.Path(os.environ.get("BOUNTY_REPORTS") or ROOT / "reports")


def get_json(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def scan_superteam():
    """Superteam Earn 开放任务。sponsor.chapter is None => 疑似无地区限制（还要读描述确认）"""
    try:
        d = get_json("https://earn.superteam.fun/api/listings?take=60")
    except Exception as e:
        return {"error": str(e), "items": []}
    items = []
    for it in d:
        if it.get("status") != "OPEN":
            continue
        sp = it.get("sponsor") or {}
        subs = (it.get("_count") or {}).get("Submission", 0)
        reward = it.get("rewardAmount") or 0
        items.append({
            "id": it.get("slug"),
            "title": it.get("title"),
            "reward": reward, "token": it.get("token"),
            "deadline": (it.get("deadline") or "")[:10],
            "submissions": subs,
            "global_ok": sp.get("chapter") is None,
            "sponsor": sp.get("name"),
            "url": f"https://superteam.fun/earn/listing/{it.get('slug')}",
        })
    return {"items": items}


def scan_superteam_agent():
    """Superteam 的 agent 专用端点 —— 能拿到公开列表看不到的 AGENT_ONLY 任务。
    认证用 /var/minis/workspace/superteam/.env 里的 SUPERTEAM_API_KEY。
    规则：agents 不需要 OAuth/钱包/KYC；中奖后把 claimCode 交给人类领钱。"""
    key = os.environ.get("SUPERTEAM_API_KEY")
    env = "/var/minis/workspace/superteam/.env"
    if not key and os.path.exists(env):
        for line in open(env):
            if line.startswith("SUPERTEAM_API_KEY="):
                key = line.split("=", 1)[1].strip()
    if not key:
        return {"error": "no SUPERTEAM_API_KEY", "items": []}
    out = []
    for t in ("bounty", "project", "hackathon"):
        try:
            req = urllib.request.Request(
                f"https://superteam.fun/api/agents/listings/live?type={t}&take=30",
                headers={"Authorization": f"Bearer {key}", "Accept": "application/json",
                         "User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as r:
                d = json.loads(r.read().decode())
            items = d if isinstance(d, list) else (d.get("listings") or d.get("data") or [])
            for it in items:
                if isinstance(it, dict):
                    it["_type"] = t
                    out.append(it)
        except Exception as e:
            out.append({"_error": f"{t}: {e}"})
    return {"items": out}


def load_state():
    if os.path.exists(STATE):
        try:
            return json.load(open(STATE))
        except Exception:
            pass
    return {"seen": {}, "runs": 0}


def save_state(st):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(st, open(STATE, "w"), indent=1, ensure_ascii=False)


def _main():
    st = load_state()
    st["runs"] = st.get("runs", 0) + 1
    seen = st.get("seen", {})
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")

    res = scan_superteam()
    if res.get("error"):
        print(f"[warn] Superteam 扫描失败: {res['error']}")

    fresh, allg = [], []
    for it in res["items"]:
        key = it["id"]
        if key not in seen:
            fresh.append(it)
            seen[key] = now
        if it["global_ok"] and it["reward"] >= 100:
            allg.append(it)

    print(f"=== 外部赏金扫描 {now}（第 {st['runs']} 轮）===")
    print(f"Superteam 开放任务: {len(res['items'])} | 本轮新增: {len(fresh)}")
    print()
    if fresh:
        print("🆕 本轮新出现的:")
        for it in sorted(fresh, key=lambda x: -x["reward"]):
            flag = "无地区限制" if it["global_ok"] else "有地区分会"
            print(f"  ${it['reward']:<6} [{it['submissions']:>3} 提交] [{flag}] {it['title'][:56]}")
            print(f"           {it['url']}")
        print()
    print("💰 当前所有「疑似无地区限制 + 赏金 >=$100」（提交越少越值得抢）:")
    for it in sorted(allg, key=lambda x: (x["submissions"], -x["reward"])):
        print(f"  ${it['reward']:<6} [{it['submissions']:>3} 提交] {it['deadline']} | {it['title'][:52]}")
    print()
    print("⚠️  提醒：global_ok 只是「sponsor 没有地区分会」，真限制要读任务描述确认")

    # Superteam AGENT 专属端点（能看到 AGENT_ONLY 的隐藏任务）
    ares = scan_superteam_agent()
    if ares.get("error"):
        print(f"\n[warn] agent 端点: {ares['error']}")
    else:
        real = [x for x in ares["items"] if "_error" not in x]
        errs = [x for x in ares["items"] if "_error" in x]
        print(f"\n🤖 Superteam AGENT 专属任务（含隐藏的 AGENT_ONLY）: {len(real)} 个")
        for it in real:
            key2 = it.get("slug") or it.get("id")
            isnew = key2 not in seen
            if isnew:
                seen[key2] = now
            print(f"  {'🆕 ' if isnew else '   '}${it.get('rewardAmount')} {it.get('token')} "
                  f"[{it.get('agentAccess')}] {(it.get('title') or '')[:54]}")
            print(f"      https://superteam.fun/earn/listing/{key2}")
        if not real:
            print("   （当前没有 agent 可领的任务 —— 正常，等新的）")
        for e in errs:
            print("   err:", e["_error"][:120])

    save_state(st)




def main():
    """云端入口：跑原逻辑 → 报告落 reports/（会被 CI 提交回仓库）→ 机读摘要。"""
    import contextlib, io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _main()
    text = buf.getvalue()
    print(text)

    REPORTS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M")
    (REPORTS / f"bounty-{stamp}.md").write_text(text, encoding="utf-8")
    (REPORTS / "latest.md").write_text(text, encoding="utf-8")

    st = load_state()
    open_line = next((l for l in text.splitlines() if l.startswith("Superteam 开放任务")), "")
    m = re.search(r"开放任务:\s*(\d+).*?本轮新增:\s*(\d+)", open_line)
    new_items, in_new = [], False
    for l in text.splitlines():
        if l.startswith("🆕"): in_new = True; continue
        if in_new:
            if l.startswith("  $"): new_items.append(l.strip())
            elif not l.strip(): in_new = False
    top = [l.strip() for l in text.splitlines() if re.match(r"^  \$\d", l)]
    summary = {
        "at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "runs": st.get("runs"),
        "open_total": int(m.group(1)) if m else None,
        "new_count": int(m.group(2)) if m else None,
        "new_items": new_items,
        "global_candidates": top,
        "repo": "https://github.com/HCTDIP/corps-jobs",
    }
    (REPORTS / "latest.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[cloud] 报告 → reports/latest.md｜机读 → reports/latest.json")

if __name__ == "__main__":
    main()
