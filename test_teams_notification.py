import os
import requests

# GitHub Secrets から Webhook URL を取得
TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")

# 通知内容
message = {
    "text": "✅ Teams通知テスト成功！このメッセージが見えたら連携はOKです。"
}

# 通知送信
response = requests.post(TEAMS_WEBHOOK_URL, json=message)

# 結果を表示
print("ステータスコード:", response.status_code)
print("レスポンス:", response.text)
