```json
{
  "bounties": [
    {
      "id": "12345",
      "title": "iOS clients lose connection after upload",
      "description": "iOS clients lose the connection right after upload; backend completes every request.",
      "category": "Configuration",
      "points": 4,
      "status": "Available",
      "answer": {
        "description": "iOS客户端在上传后立即失去连接，可能与上传过程中的连接问题或后台处理请求有关。建议检查上传过程中的网络连接情况，确保上传完成后连接稳定。同时，确认后台在处理请求时的响应情况，排除可能的延迟或超时问题。可以尝试重启设备或检查网络设置，以解决连接问题。",
        "steps": [
          "检查上传过程中的网络连接稳定性。",
          "确认后台在处理请求时的响应情况。",
          "建议重启设备或检查网络设置。"
        ]
      }
    }
  ]
}
```