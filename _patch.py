#!/usr/bin/env python3
"""把手机版 bounty_scan.py 补成云端版（改路径 + 从 env 读 key + 落报告/机读摘要）。"""
import pathlib, re

P = pathlib.Path("/var/minis/workspace/corps-jobs/jobs/bounty_scan.py")
s = P.read_text()

# 1) 路径云端化
s = s.replace('STATE = "/var/minis/workspace/bounty-hunt/external_state.json"',
              'import pathlib\n'
              'ROOT = pathlib.Path(__file__).resolve().parents[1]\n'
              'STATE = os.environ.get("BOUNTY_STATE") or str(ROOT / "state" / "external_state.json")\n'
              'REPORTS = pathlib.Path(os.environ.get("BOUNTY_REPORTS") or ROOT / "reports")')

# 2) key 优先从环境变量（GitHub Secret）读
s = s.replace('''    env = "/var/minis/workspace/superteam/.env"
    key = None
    if os.path.exists(env):''',
              '''    key = os.environ.get("SUPERTEAM_API_KEY")
    env = "/var/minis/workspace/superteam/.env"
    if not key and os.path.exists(env):''')

# 3) main -> 捕获输出 + 落盘报告 + 机读摘要
s = s.replace("def main():", "def _main():", 1)
s += '''

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
    m = re.search(r"开放任务:\\s*(\\d+).*?本轮新增:\\s*(\\d+)", open_line)
    new_items, in_new = [], False
    for l in text.splitlines():
        if l.startswith("🆕"): in_new = True; continue
        if in_new:
            if l.startswith("  $"): new_items.append(l.strip())
            elif not l.strip(): in_new = False
    top = [l.strip() for l in text.splitlines() if re.match(r"^  \\$\\d", l)]
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
'''
s = s.replace("import json, os, urllib.request, datetime",
              "import json, os, re, urllib.request, datetime", 1)
P.write_text(s)
print("patched:", P, len(s), "bytes")
