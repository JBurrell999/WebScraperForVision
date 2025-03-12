import requests
import os

API_KEY = 'f0fdc865b08ece101fdbad2c6e8686337cdcb5ff5f2b7c3560c52b6802ab18be'

SEARCH_QUERIES = [
    "exclusive interview",
    "keynote speech economics",
    "keynote speech tech",
    "fireside chat finance",
    "fireside chat economics",
    "panel discussion summit",
    "video podcast politics",
    "interview news",
    "breaking news world",
    ".edu",
]

OUTPUT_FILE = 'video_urls.txt'

# Toggle this to True to filter ONLY Creative Commons videos
FILTER_CREATIVE_COMMONS = True  

def search_youtube(query, api_key, num_results=22, creative_commons=False):
    urls = []
    api_url = f"https://serpapi.com/search.json?engine=youtube&search_query={query}&api_key={api_key}"

    # Creative Commons filter explicitly added if enabled
    if creative_commons:
        api_url += "&sp=EgIwAQ%253D%253D"

    response = requests.get(api_url)
    results = response.json().get('video_results', [])
    for result in results[:num_results]:
        urls.append(result['link'])
    return urls

def load_existing_urls(filepath):
    if not os.path.exists(filepath):
        return set()
    with open(filepath, 'r') as f:
        return set(line.strip() for line in f if line.strip())

def search_and_save(queries, api_key, creative_commons=False):
    existing_urls = load_existing_urls(OUTPUT_FILE)
    print(f"[INFO] {len(existing_urls)} existing URLs loaded.")

    new_urls = set()

    for query in queries:
        cc_status = " (Creative Commons)" if creative_commons else ""
        print(f"[INFO] Searching YouTube for '{query}'{cc_status}...")
        urls = search_youtube(query, api_key, creative_commons=creative_commons)
        new_urls.update(urls)

    unique_new_urls = new_urls - existing_urls

    with open(OUTPUT_FILE, 'a') as f:
        for url in unique_new_urls:
            f.write(url + '\n')

    print(f"[INFO] {len(unique_new_urls)} new URLs added.")
    print(f"[INFO] Total URLs in file: {len(existing_urls) + len(unique_new_urls)}")

if __name__ == "__main__":
    search_and_save(SEARCH_QUERIES, API_KEY, creative_commons=FILTER_CREATIVE_COMMONS)