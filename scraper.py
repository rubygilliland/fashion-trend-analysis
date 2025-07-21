import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HEADERS = {'User-Agent': 'Mozilla/5.0'}

# loads and reads data from Vogue website
def get_show_links_selenium(collection_url):
    print("Launching browser to get show links...")

    # launches web browser
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(collection_url)

    try:
        # all shows are listed as links in a sidebar on vogue website
        print("Waiting for sidebar to load...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'nav[data-testid="navigation"] ul'))
        )

        # finds amount of links using css structure used in vogue website
        links = driver.find_elements(By.CSS_SELECTOR, 'nav[data-testid="navigation"] ul li a')
        print(f"Total links found: {len(links)}")

        shows = []
        seen = set()

        # loops through all links found and gathers data from each article
        for link in links:
            href = link.get_attribute("href")

            if href and '/fashion-shows/' in href and href not in seen:

                # extract the last part of the URL as a fallback for the designer name
                name = href.split("/")[-1].replace("-", " ").title()
                full_url = href if href.startswith("http") else "https://www.vogue.com" + href

                shows.append({
                    'designer': name,
                    'url': full_url,
                    'image_url': None
                })

                seen.add(href)


        print(f"Found {len(shows)} valid designer shows.")
        return shows

    except Exception as e:
        print(f"Failed to load links: {e}")
        return []

    finally:
        driver.quit()

# scrapes the desired data for an individual show link
def scrape_show_page(show):
    url = show['url']
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')

    # title or collection name
    try:
        url_parts = url.split('/')
        season = url_parts[4].replace('-', ' ').title()
        collection_name = f"{show['designer']} {season}"
    except:
        collection_name = f"{show['designer']} Unknown Season"


    # show review article text
    try:
        review_div = soup.find('div', class_='article__body')
        review = review_div.text.strip() if review_div else 'N/A'
    except:
        review = 'N/A'

    # all show images
    image_urls = []
    try:
        images = soup.find_all('img')
        for img in images:
            src = img.get('src')
            if src and 'photos/' in src and 'runway' in src:
                image_urls.append(src)
    except:
        pass

    # each links data is organized by these sections and later saved to csv
    return {
        'designer': show['designer'],
        'collection_url': url,
        'cover_image': show['image_url'],
        'collection_name': collection_name,
        'review': review,
        'look_images': image_urls
    }

# iterates through all links and scrapes desired data for each one
def scrape_all_shows(show_links):
    all_data = []
    for i, show in enumerate(show_links):

        # displays what show is currently being scraped
        print(f"Scraping {i+1}/{len(show_links)}: {show['designer']}")

        try:
            show_data = scrape_show_page(show)
            all_data.append(show_data)

        except Exception as e:
            print(f"Error scraping {show['designer']}: {e}")

        # takes breaks to not alert vogue websites servers 
        time.sleep(1)  
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
    collection_url = "https://www.vogue.com/fashion-shows/spring-2025-ready-to-wear"
    show_links = get_show_links_selenium(collection_url)

    all_shows = scrape_all_shows(show_links)
    save_to_csv(all_shows, filename='data/spring_2025_shows.csv')

if __name__ == '__main__':
    main()

