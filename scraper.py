from bs4 import BeautifulSoup
import pandas as pd
import time, requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_show_links_selenium(collection_url):
    print("Launching browser to get show links...")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(collection_url)
    shows, seen = [], set()

    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # light scroll to trigger any lazy content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.8)
        driver.execute_script("window.scrollTo(0, 0);")

        base_path = urlparse(collection_url).path.rstrip("/")
        base_origin = "https://www.vogue.com"

        # search broadly, then refine to links under the collection path.
        candidates_css = [
            f'a[href^="{base_path}/"]',
            f'a[href^="{base_origin}{base_path}/"]',
            'nav[data-testid="navigation"] ul li a',
            'a[class^="SummaryItemHedLink"]',
            'a.card-article-link',

            # final catch-all
            'a[href*="/fashion-shows/"]',  
        ]

        total_found = 0

        # finds amount of links using css structure used in vogue website
        for css in candidates_css:
            elems = driver.find_elements(By.CSS_SELECTOR, css)
            if not elems:
                continue
            total_found += len(elems)

            for a in elems:
                href = a.get_attribute("href")
                if not href:
                    continue

                full = urljoin(base_origin, href)
                path = urlparse(full).path

                # keep only links under THIS collection (e.g., /fashion-shows/mexico-fall-2025/...)
                if not (path.startswith(base_path + "/")):
                    continue
                if full in seen:
                    continue

                # prefer visible text, then <h3 data-testid="SummaryItemHed">, then URL slug.
                name = (a.text or "").strip()
                if not name:
                    try:
                        name = a.find_element(By.CSS_SELECTOR, 'h3[data-testid="SummaryItemHed"]').text.strip()
                    except Exception:
                        name = path.split("/")[-1].replace("-", " ").title()

                # try to grab a thumbnail if present.
                img_url = None
                try:
                    img_url = a.find_element(By.TAG_NAME, "img").get_attribute("src")
                except Exception:
                    pass

                shows.append({"designer": name, "url": full, "image_url": img_url})
                seen.add(full)

        print(f"Total anchors scanned: {total_found}")
        print(f"Found {len(shows)} valid designer shows.")
        return shows

    except Exception as e:
        print(f"Failed to collect show links: {e}")
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

    try:
        # Find the <img> tag
        all_images = soup.find_all("img", class_="ResponsiveImageContainer-eNxvmU cfBbTk responsive-image__image")
        img_tag = all_images[3]

        # Grab the URL
        if img_tag and soup.find_all():
            # Either the main src
            cover_image = img_tag.get("src")
            
    except:
        cover_image = None

    # return organized data
    return {
        'designer': show['designer'],
        'collection_url': url,
        'cover_image': cover_image,
        'collection_name': collection_name,
        'review': review,
    }


# iterates through all links and scrapes desired data for each one
def scrape_all_shows(show_links, progress_callback=None):
    all_data = []
    for i, show in enumerate(show_links):
        
        # displays what show is currently being scraped
        print(f"Scraping {i+1}/{len(show_links)}: {show['designer']}")

        try:
            show_data = scrape_show_page(show)

            if progress_callback:
                progress_callback(i+1, len(show_links), show_data['designer'], show_data['cover_image'])

            all_data.append(show_data)

        except Exception as e:
            print(f"Error scraping {show['designer']}: {e}")

        # takes randomized breaks to not alarm vogue websites servers 
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
        })
    df = pd.DataFrame(flat_data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def run_scraper_for_season(season_string, progress_callback=None):
    season_path = f"data/{season_string.replace('-', '_')}_shows.csv"
    collection_url = f"https://www.vogue.com/fashion-shows/{season_string}"

    show_links = get_show_links_selenium(collection_url)

    all_shows = scrape_all_shows(show_links, progress_callback=progress_callback)
    save_to_csv(all_shows, season_path)
    return season_path



