```yaml
n8n:
  selfHosted:
    env:
      NODE_OPTIONS: --max-old-space-size=4096
      N8N_DB: sqlite:///:memory: 
      N8N_LOG_LEVEL: info
    ports:
      selfHosted: 5601
```

```yaml
name: Check DLopen for Python
description: 确保Python能够正确加载共享库
trigger: manually
actions:
  - name: Check ldd for Python
    executor: bash
    inputs: []
    outputs: []
    code: |
      ldd $(which python3) | grep -q 'not found' || true
  - name: Check ldconfig cache
    executor: bash
    inputs: []
    outputs: []
    code: |
      ldconfig -p | grep $(which python3) || true
  - name: Check LD_LIBRARY_PATH
    executor: bash
    inputs: []
    outputs: []
    code: |
      echo $LD_LIBRARY_PATH
  - name: Check permissions
    executor: bash
    inputs: []
    outputs: []
    code: |
      ls -l $(which python3) | grep 'lrwxrwxrwx'
```