from curl_cffi import requests as cffi_requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

URL = "https://www.nairaland.com/"
SEEN_FILE = "seen_urls.json"

def get_seen_urls():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_seen_urls(urls):
    with open(SEEN_FILE, 'w') as f:
        json.dump(list(urls), f)

def fetch_frontpage_topics():
    # Use curl_cffi to impersonate a real Chrome browser's TLS fingerprint
    try:
        print(f"Fetching {URL} with curl_cffi (impersonating Chrome)...")
        # The impersonate parameter is the key
        response = cffi_requests.get(URL, impersonate="chrome110", timeout=30)
        response.raise_for_status()
        print(f"Successfully fetched! Status code: {response.status_code}")
    except Exception as e:
        print(f"ERROR fetching Nairaland: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    topics = []
    featured_cells = soup.find_all('td', class_='featured w')

    if not featured_cells:
        print("WARNING: Could not find the frontpage topic container. The layout might have changed or we are still being blocked.")
        return []

    for cell in featured_cells:
        for link in cell.find_all('a', href=True):
            href = link['href']
            if href.startswith('/') and len(href) > 2 and href[1].isdigit():
                full_url = "https://www.nairaland.com" + href
                title = link.get_text(strip=True)
                if title and len(title) > 3:
                    topics.append({
                        'title': title,
                        'link': full_url,
                        'pubDate': datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
                    })

    print(f"Found {len(topics)} raw links on the page.")
    unique_topics = []
    seen_in_batch = set()
    for t in topics:
        if t['link'] not in seen_in_batch:
            unique_topics.append(t)
            seen_in_batch.add(t['link'])
    return unique_topics

def main():
    seen_urls = get_seen_urls()
    new_topics = fetch_frontpage_topics()
    fresh_topics = []
    for topic in new_topics:
        if topic['link'] not in seen_urls:
            fresh_topics.append(topic)
            seen_urls.add(topic['link'])
    save_seen_urls(seen_urls)
    with open('news.json', 'w') as f:
        json.dump(fresh_topics, f, indent=2)
    print(f"Saved {len(fresh_topics)} new topics to news.json.")

if __name__ == "__main__":
    main()
