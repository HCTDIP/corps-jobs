# corps-jobs — 重活上云的执行机

**为什么存在**：军团所有 Agent 都跑在**一部 iPhone 上的 iSH** 里 —— 单核、内存紧、
App 一重启定时任务就全灭（已发生两次）。本仓把**重复、重、必须按时跑**的活搬到
GitHub Actions（多核、免费额度、不受手机生死影响），手机侧只负责**读结果**。

## 托管任务

| 任务 | 文件 | 频率 | 产物 |
|---|---|---|---|
| 外部赏金雷达（Superteam 等，真人出钱平台） | `jobs/bounty_scan.py` | 每 6 小时 | `reports/bounty-<时间戳>.md` · `reports/latest.md` · `reports/latest.json` |

产物自动 commit 回本仓 —— 手机侧 `git pull` 或直接读 raw URL，**本机不跑任何扫描代码**：

```sh
curl -s https://raw.githubusercontent.com/HCTDIP/corps-jobs/main/reports/latest.json
```

## 用法

- **手动补跑**：Actions → `bounty-scan` → Run workflow
- **开启 agent 专属端点**（拿隐藏的 AGENT_ONLY 任务）：Settings → Secrets and variables → Actions → 新增 `SUPERTEAM_API_KEY`；未设置时脚本优雅跳过并在报告注明

## 设计原则（沿用 2026-09-23 尽调教训）

- 只要**真人出钱**的平台，不要 agent 自嗨圈
- Superteam 的 `GLOBAL` 标签**不可信** → 看 `sponsor.chapter`
- **低竞争优先**（提交数少的排前）
- 只报**新出现的差异**（`state/external_state.json` 提交回仓，跨运行保持）

## 加新任务的规矩

1. 脚本放 `jobs/`，**只用标准库**（云端 runner 干净，装依赖是额外失败面）
2. 状态写 `state/`、产物写 `reports/`（都会被提交回仓库）
3. workflow 要有 `permissions: contents: write` + `concurrency` 防重入
4. 结果必须写进 `$GITHUB_STEP_SUMMARY` —— 打开 Actions 页面就能读
