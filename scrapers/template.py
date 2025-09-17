import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

# The ABC (Abstract Base Class) and @abstractmethod decorator ensure
# that any class that inherits from BaseScraper must implement this method.
# This enforces a standard structure for all scrapers.

class BaseScraper(ABC):
    """
    A template for creating a new web scraper for a scanlation website.
    
    This abstract class defines the required methods for a scraper.
    To create a new scraper, inherit from this class and implement
    the 'get_latest_chapter' method.
    """

    @abstractmethod
    def get_latest_chapter(self, series_url: str) -> dict:
        """
        Retrieves the URL and chapter number of the latest chapter
        for a given manga series.

        Args:
            series_url: The full URL of the manga series on the scanlation site.
            
        Returns:
            A dictionary with the following structure:
            {
                "title": "Series Title",
                "chapter_number": 123,
                "chapter_url": "https://example.com/series/title/chapter-123"
            }
            Returns None if the information cannot be found.
        """
        pass