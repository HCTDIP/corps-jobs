```ruby
require 'railway'

reports = [
  { value: 7, title: "Frequent WebSocket disconnects affecting multiple independent clients" },
  { value: 5, title: "Builds on builder-uwqkzv crash in next build with 'invalid table size' since Oct 1 ~11:00 UTC" },
  { value: 4, title: "Server Performance Issue on Pro Plan – Project B Not Responding / Login Failing $30 5 replies 7m by" },
  { value: 4, title: "Selective outbound TCP/443 timeouts from sfo — private investigation requested $20 0 rep 数小时内, 竞争低" },
  { value: 4, title: "Frequent WebSocket disconnects affecting multiple independent clients" },
  { value: 4, title: "Safe SQLite WAL backup without unverifiable SSH host key" },
  { value: 4, title: "Node inspector opened and attached in api/worker without --inspect — is this a Railway f 竞争低, 提问·配置型" }
]

issues = reports.sort_by { |issue| -issue[:value] }

first_issue = issues.first
second_issue = issues[1] || {}
third_issue = issues[2] || {}
fourth_issue = issues[3] || {}
fifth_issue = issues[4] || {}
sixth_issue = issues[5] || {}
seventh_issue = issues[6] || {}
```