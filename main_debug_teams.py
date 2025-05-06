import feedparser
import requests
import csv
import time
import os

# --- APIキーの取得 ---
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")

def translate(text):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": "JA"
    }
    response = requests.post(url, data=params)
    if response.status_code != 200:
        print(f"Translation error: {response.status_code}, {response.text}")
        return "翻訳に失敗しました"
    return response.json()["translations"][0]["text"]

def send_teams_notification(lines):
    if not lines:
        print("⚠️ 通知する内容がありません（linesが空です）")
        return

    message = "**📢 本日の生成AI論文（最新5件）**\n" + "\n".join(lines)
    payload = {"text": message}

    print("📤 Teams通知の送信を開始します...")
    print("Webhook URL:", TEAMS_WEBHOOK_URL[:40] + "...（省略）")
    print("送信内容:
", message)

    response = requests.post(TEAMS_WEBHOOK_URL, json=payload)

    print("Teamsレスポンス:", response.status_code, response.text)

    if response.status_code != 200:
        print(f"❌ Teams通知エラー: {response.status_code}")
    else:
        print("✅ Teams通知成功")

# --- ArXivから論文取得 ---
query = "generative+ai"
url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending"
feed = feedparser.parse(url)

# --- CSV出力と通知用テキストの構築 ---
output_file = "arxiv_generative_ai.csv"
lines = []

with open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Summary (EN)", "Summary (JA)", "Published", "Link"])
    for i, entry in enumerate(feed.entries):
        ja_summary = translate(entry.summary[:1000])
        writer.writerow([entry.title, entry.summary, ja_summary, entry.published, entry.link])
        lines.append(f"🧠 **{entry.title}**\n{ja_summary[:100]}...")
        time.sleep(1)

# --- Teamsに通知送信 ---
send_teams_notification(lines)

print(f"✅ CSVファイルとTeams通知を完了しました: {output_file}")
