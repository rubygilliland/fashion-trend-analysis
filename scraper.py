import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


BASE_URL = 'https://www.vogue.com'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
COLLECTION_URL = BASE_URL + '/fashion-shows/spring-2026-ready-to-wear'

def get_show_links(collection_url):
    response = requests.get(collection_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')

    shows = []

    # 🔹 First: Highlighted shows (already working)
    highlight_cards = soup.find_all('a', attrs={'data-testid': 'SummaryItemSimple'})

    # 🔹 Second: Latest shows (new selector)
    latest_cards = soup.find_all('a', attrs={'data-recirc-pattern': 'summary-item'})

    all_cards = highlight_cards + latest_cards
    print(f"Found {len(all_cards)} total show links.")

    for card in all_cards:
        href = card.get('href')
        if not href or '/fashion-shows/' not in href:
            continue

        h3 = card.find('h3')
        if h3 is None:
            print("Skipping due to missing <h3> in:")
            print(card.prettify())  # ← this prints the entire HTML block
            continue

        designer = h3.text.strip()
        full_url = BASE_URL + href

        shows.append({
            'designer': designer,
            'url': full_url,
            'image_url': None
        })



    return shows


def scrape_show_page(show):
    url = show['url']
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')

    # Title or collection name
    try:
        url_parts = url.split('/')
        season = url_parts[4].replace('-', ' ').title()
        collection_name = f"{show['designer']} {season}"

    except:
        title = 'N/A'

    # Review text (usually near the top or in a review section)
    try:
        review_div = soup.find('div', class_='article__body')
        review = review_div.text.strip() if review_div else 'N/A'
    except:
        review = 'N/A'

    # All look images (not just the cover)
    image_urls = []
    try:
        images = soup.find_all('img')
        for img in images:
            src = img.get('src')
            if src and 'photos/' in src and 'runway' in src:
                image_urls.append(src)
    except:
        pass

    return {
        'designer': show['designer'],
        'collection_url': url,
        'cover_image': show['image_url'],
        'collection_name': collection_name,
        'review': review,
        'look_images': image_urls
    }

def scrape_all_shows(show_links):
    all_data = []
    for i, show in enumerate(show_links):
        print(f"Scraping {i+1}/{len(show_links)}: {show['designer']}")
        show_data = scrape_show_page(show)
        all_data.append(show_data)
        time.sleep(1)  # Be polite to Vogue's servers
    return all_data

def save_to_csv(data, filename='fashion_shows.csv'):
    flat_data = []
    for entry in data:
        flat_data.append({
            'Designer': entry['designer'],
            'Collection Name': entry['collection_name'],
            'URL': entry['collection_url'],
            'Cover Image': entry['cover_image'],
            'Review': entry['review'],
            'Num Looks': len(entry['look_images']),
            'Look Image URLs': ', '.join(entry['look_images'])  # You can also save this separately
        })
    df = pd.DataFrame(flat_data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    collection_url = 'https://www.vogue.com/fashion-shows/spring-2026-ready-to-wear'
    #show_links = get_show_links(collection_url)
    show_links = get_show_links(collection_url)
    all_shows = scrape_all_shows(show_links)
    #all_shows = scrape_all_shows(show_links[:3])  # Only scrape first 3
    save_to_csv(all_shows, filename='data/spring_2026_shows.csv')

if __name__ == '__main__':
    main()

