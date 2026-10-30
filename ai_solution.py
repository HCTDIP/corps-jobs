```
1. 🆕 Production deployment resolves DOCKERFILE service as RAILPACK and fails at BUILD_IMAGE
   查看构建日志，确认是否有Dockerfile语法错误或资源限制：
   ```bash
   railway logs --level=DEBUG
   ```
   如果Dockerfile语法正确，建议增加资源配额。

2. 🆕 Sudden DNS issue on production system $20 2 replies 7m by upd
   检查DNS记录和配置：
   ```bash
   railway dns records
   ```
   如果有解析问题，建议重新加载DNS配置。

3. [+5] Official CPU/RAM limit write, readback and reconciliation contract for Hobby $10 0 repli
   确认配额设置是否正确：
   ```bash
   railway config
   ```
   核对合同条款以确认配额。

4. [+4] Preserve unrelated staged changes during a service-specific API deployment
   在特定API部署中，使用以下命令保留不相关的阶段变更：
   ```bash
   railway deploy --stage=your-stage-name
   ```
   或选择性保留变更。

5. [+4] How to securely obtain a PostgreSQL public root CA without SSH?
   使用以下curl命令获取证书：
   ```bash
   curl https://railway.app/your-app-id/postgres/root/ca
   ```
   适用于需要获取CA证书的情况。

```