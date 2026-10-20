```bash
# Set the backup time to 03:00 UTC using a cron job
crontab -e
# Add this line:
@daily 0 3 * * * /usr/bin/pg_start_planner && /usr/bin/pg_stop_planner
```