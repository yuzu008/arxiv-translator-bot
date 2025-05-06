import feedparser
import requests
import csv
import time
import os

# DeepL APIキー（GitHub Secrets から取得）
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

def translate(text):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": "JA"
    }
    response = requests.post(url, data=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return "Error: Translation failed"
    return response.json()["translations"][0]["text"]

# ArXiv APIで生成AI関連論文を取得
query = "generative+ai"
url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending"
feed = feedparser.parse(url)

# CSV出力
output_file = "arxiv_generative_ai.csv"
with open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Summary (EN)", "Summary (JA)", "Published", "Link"])
    for entry in feed.entries:
        ja_summary = translate(entry.summary[:1000])
        writer.writerow([entry.title, entry.summary, ja_summary, entry.published, entry.link])
        time.sleep(1)

print(f"✅ CSV file saved: {output_file}")
