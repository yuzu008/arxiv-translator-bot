import os
import requests

TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")

message = {
    "text": "✅ Teams通知テスト成功！このメッセージが見えたら連携はOKです。"
}

response = requests.post(TEAMS_WEBHOOK_URL, json=message)

print("ステータスコード:", response.status_code)
print("レスポンス:", response.text)
