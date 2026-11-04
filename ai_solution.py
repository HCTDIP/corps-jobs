To address the three issues, here are the bash code snippets:

1. Flushing the DNS cache:
```bash
sudo systemd-resolve --flush-caches
```

2. Adjusting the flow settings for Edge (Hikari):
```bash
# Increase max concurrent streams
curl --http2 http://your-railway-url.com
```

3. Checking and configuring SSH in Railway:
```bash
railway config
```

These commands should help resolve each of the mentioned issues.