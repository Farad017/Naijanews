import os
import json
import requests
import feedparser

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
RSS_URL = "https://farad017.github.io/Naijanews/feed.xml"
STATE_FILE = "posted_links.json"

# 🛑 SET TO True FOR TESTING, False FOR LIVE
TEST_MODE = True 

def load_posted_links():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_posted_links(links):
    with open(STATE_FILE, 'w') as f:
        json.dump(list(links), f)

def send_telegram_message(title, link):
    text = f"📰 **{title}**\n\n🔗 [Read on na1ra1and]({link})"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"Sent: {title[:50]}...")
    except Exception as e:
        print(f"Failed to send '{title}': {e}")

def main():
    posted = load_posted_links()
    feed = feedparser.parse(RSS_URL)
    new_count = 0

    # Iterate in reverse so the oldest new post is sent first
    for entry in reversed(feed.entries):
        link = entry.link
        if link not in posted:
            send_telegram_message(entry.title, link)
            posted.add(link)
            new_count += 1
            
            # If in test mode, break the loop after 1 message
            if TEST_MODE:
                print("Test Mode: Stopping after 1 message.")
                break

    if new_count > 0:
        save_posted_links(posted)
        print(f"Finished. Sent {new_count} new posts.")
    else:
        print("No new posts found.")

if __name__ == "__main__":
    main()
