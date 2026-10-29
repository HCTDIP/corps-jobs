```yaml
# 配置Railway的网络设置
network:
  lisheng-production.up.railway.app:
    tcp_timeout: 30s
    edge_routing: enabled

# 优化Sentry模板请求的配置
sentry:
  template_request:
    enable: true
    cache_duration: 2h

# 保留无关阶段的配置
deploy:
  keep_unrelated_stages: true
```