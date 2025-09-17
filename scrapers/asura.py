from .template import BaseScraper # Import the base class
import requests
from bs4 import BeautifulSoup
import re # Regular expressions for parsing chapter numbers

class AsuracomicScraper(BaseScraper):
    """
    Scraper for the Asuracomic.net website.
    """
    def get_latest_chapter(self, series_url: str) -> dict:
        try:
            # 1. Fetch the HTML content of the page.
            response = requests.get(series_url, timeout=10)
            response.raise_for_status()
            
            # 2. Parse the HTML with BeautifulSoup.
            soup = BeautifulSoup(response.text, 'html.parser')

            # 3. Find the series title.
            # The title is in an <h1> tag.
            title_tag = soup.find('h1')
            if not title_tag:
                return None
            series_title = title_tag.get_text(strip=True)

            # 4. Find the latest chapter link.
            # The latest chapter link is a specific <a> tag within the "Chapter List" section.
            # We locate the container with the chapter list first.
            chapter_list_div = soup.find('div', class_='grid md:grid-cols-2 lg:grid-cols-3')
            
            if not chapter_list_div:
                print(f"Could not find chapter list div for {series_url}")
                return None
            
            # The latest chapter link is the first <a> tag in this container.
            latest_chapter_link = chapter_list_div.find('a')
            
            if not latest_chapter_link:
                print(f"Could not find latest chapter link for {series_url}")
                return None
            
            chapter_url = latest_chapter_link.get('href')
            chapter_text = latest_chapter_link.get_text(strip=True)

            # 5. Extract the chapter number.
            # Use a regular expression to find the number in the URL itself,
            # which is more reliable than scraping the text.
            # The URL format is `.../chapter/75`
            match = re.search(r'chapter/(\d+)', chapter_url)
            if not match:
                # Fallback to text parsing if URL format changes
                match = re.search(r'\b(\d+)\b', chapter_text)
                if not match:
                    print(f"Could not find chapter number in URL or text for {series_url}")
                    return None
            
            chapter_number = int(match.group(1))

            return {
                "title": series_title,
                "chapter_number": chapter_number,
                "chapter_url": chapter_url
            }

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {series_url}: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred for {series_url}: {e}")
            return None