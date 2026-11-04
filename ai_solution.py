```yaml
dns:
  check_dns_record:
    record_type: A
    domain: example.com
    expected_value: 192.168.1.1
    if empty:
      return error: DNS记录未找到。
    else:
      check if the value is correct.

  check_cname_record:
    domain: example.com
    if any:
      check if there are any CNAME records.
      if yes:
        return note: CNAME记录已存在，可能影响A记录的设置。
```