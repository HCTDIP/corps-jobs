```json
{
  "baseUrl": "https://app.typebot.io/bots/123456",
  "suppressWelcome": true,
  "bot": {
    "command": "typebot",
    "config": "config.json"
  }
}

# Docker configuration
version: '3.8'
services:
  postgres-ssl:
    image: postgres-ssl:16
    environment:
      - POSTGRES_DB=your_database
      - POSTGRES_USER=your_user
      - POSTGRES_PASSWORD=your_password
    ports:
      - "5432:5432"
    volumes:
      - postgresql_volume:/var/lib/postgresql/data
volumes:
  postgresql_volume:

# PostgreSQL configuration
$PostgreSQL {
  listen_addresses = '*'
  port = 5432
  ssl = true
  ssl_cert_file = '/var/lib/postgresql/data/server.crt'
  ssl_key_file = '/var/lib/postgresql/data/server.key'
  logging:
    log_directory = 'pg_log'
    log_file = 'postgresql.log'
    log_rotation_size = 10MB
    log_truncate_on_rotation = true
}
```