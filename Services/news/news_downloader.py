from datetime import datetime
from pydantic import BaseModel
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from typing import List, Tuple
from loguru import logger
import json


class News(BaseModel):
    """
    This is the data model for the news.
    """

    title: str
    published_at: datetime
    source: str

    # you can keep the url or other elements to get even deeper and do some filtering or whatever you need.

    def to_dict(self) -> dict:
        model_data = self.model_dump()
        model_data["published_at"] = self.published_at.isoformat()
        return {
            **model_data,
            "timestamp_ms": int(self.published_at.timestamp() * 1000),
        }


class NewsDownloader:
    URL = "https://cryptopanic.com/api/free/v1/posts/"

    def __init__(
        self,
        cryptopanic_api_key: str,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ):
        self.cryptopanic_api_key = cryptopanic_api_key

        # Setup retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        # Create session with retry strategy
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get_news(self) -> List[News]:
        """
        Fetches news from the API, following pagination until there are no more pages (next=null)
        """
        news = []
        url = self.URL + "?auth_token=" + self.cryptopanic_api_key

        while True:
            logger.debug(f"Fetching news from: {url}")
            batch_of_news, next_url = self._get_batch_of_news(url)
            news.extend(batch_of_news)
            logger.debug(f"Fetched {len(batch_of_news)} news items")

            if not batch_of_news:
                break
            if not next_url:
                logger.debug("No more pages to fetch (next=null)")
                break

            url = next_url

        # sort the news by published_at in ascending order
        news.sort(key=lambda x: x.published_at, reverse=False)
        logger.debug(f"Total news items fetched: {len(news)}")

        return news

    def _get_batch_of_news(self, url: str) -> Tuple[List[News], str]:
        """
        connects to the cryptopanic api and returns a one batch of news

        Args:
            url (str): the url to get the news from

        Returns:
            Tuple[List[News], str]: the news and the next url

        Raises:
            json.JSONDecodeError: If the response is not valid JSON
            KeyError: If the expected data structure is not found in the response
        """
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()

            # parse the response into a list of news
            news = [
                News(
                    title=news_item["title"],
                    published_at=news_item["published_at"],
                    source=news_item["domain"],
                )
                for news_item in data["results"]
            ]

            # extract the next url from the response
            next_url = data.get("next")

            return news, next_url

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            if e.response.status_code == 429:
                logger.warning("Rate limit exceeded. Backing off...")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Error connecting to server: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON response: {e}")
            raise
        except KeyError as e:
            logger.error(f"Unexpected response structure: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            raise


if __name__ == "__main__":
    from config import cryptopanic_config

    news_downloader = NewsDownloader(cryptopanic_config.api_key)
    news = news_downloader.get_news()
    logger.info(f"got {len(news)} news")
