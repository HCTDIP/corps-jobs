```bash
# For SQLite WAL backup
railway config set --key wal-enabled true

# For Postgres PITR backup time
railway config set --key postgres-backup-time "03:00"

# For production application lag
railway config set --key postgres-log-level "info"

# For Postgres memory
railway config set --key postgres-memory "4g"

# For snapshot fetch
railway config set --key wal-enabled true

# For MongoDB Multi-Region Replica
railway config set --key atlas-multi-region true

# For TCP/443 timeouts
railway config set --key tcp-timeout 300

# For Node inspector
railway config set --key node-inspector true

# For Singapore ingress
railway config set --key api-timeout 30
```