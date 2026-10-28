import requests

# This is your SnagFlow Cloudflare URL
FEED_URL = "https://snagflow-rss-bridge.agbontan2003.workers.dev/feed?id=ec79eabb-648c-4dad-8558-6fbe12926c5a"

def main():
    print(f"Downloading feed from: {FEED_URL}")
    
    try:
        response = requests.get(FEED_URL, timeout=15)
        response.raise_for_status()
        
        # Save the XML directly to feed.xml
        with open('feed.xml', 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print("Successfully updated feed.xml!")
        
    except Exception as e:
        print(f"ERROR downloading feed: {e}")

if __name__ == "__main__":
    main()
