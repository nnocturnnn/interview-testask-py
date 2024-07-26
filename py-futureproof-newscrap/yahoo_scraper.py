from datetime import datetime, timedelta
from news_scraper import NewsScraper
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from logger_visitor import LoggerVisitor
from typing import List, Generator
import asyncio
import time
import aiohttp
from misc import (
    download_image,
    count_phrase_occurrences,
    check_for_money,
    convert_relative_time_to_datetime,
)

WAIT_TIME = 10

class YahooScraper(NewsScraper):
    def __init__(
        self, driver_path: str, search_phrase: str, category: str, months: int, visitor: LoggerVisitor
    ):
        super().__init__(
            driver_path, search_phrase, category, months, "https://news.yahoo.com/", visitor
        )
        self.base_search_url = self.generate_url_for_period(search_phrase, months)

    def generate_url_for_period(self, search_phrase: str, months: int) -> str:
        base_search_url = f"https://news.search.yahoo.com/search;?p={search_phrase}&pz=10&bct=0&xargs=0"
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30 * months)
        
        start_date_str = start_date.strftime('%Y%m%d')
        end_date_str = end_date.strftime('%Y%m%d')
        
        url = f"{base_search_url}&bt={start_date_str}&et={end_date_str}"
        return url

    def search_news(self) -> None:
        self.visitor.log("Navigating to Yahoo News Search")
        self.driver.get(self.base_search_url)

    def scroll_and_collect_articles(self) -> Generator[WebElement, None, None]:
        collected_articles = 0
        page_number = 1
        max_articles = 10
        
        while collected_articles < max_articles:
            self.driver.get(f"{self.base_search_url}&b={page_number}")
            self.visitor.log(f"Loading page {page_number}")
            
            time.sleep(2)
            new_articles =  self.driver.find_elements(By.CSS_SELECTOR, "div.dd.NewsArticle")
            if not new_articles:
                self.visitor.log("No more articles found. Ending scraping.")
                break
            for article in new_articles:
                yield article
                collected_articles += 1
                if collected_articles >= max_articles:
                    break
            
            if collected_articles < max_articles:
                page_number += 10  

    async def process_news_items(self, session: aiohttp.ClientSession) -> None:
        tasks: List[asyncio.Task] = []
        for article in self.scroll_and_collect_articles():
            try:
                title_element = article.find_element(By.CSS_SELECTOR, "h4.s-title a")
                title = title_element.text
                description = article.find_element(By.CSS_SELECTOR, "p.s-desc").text
                img_element = article.find_element(By.CSS_SELECTOR, "img.s-img")
                img_url = img_element.get_attribute("src")
                time_element = article.find_element(By.CSS_SELECTOR, "span.s-time")
                
                self.visitor.log(f"Queueing article for processing: {title}")
                print(title, img_url, time_element)
                tasks.append(
                    self.process_single_item(session, title, description, img_url, time_element)
                )
            except Exception as e:
                self.visitor.log(f"Error processing article: {e}", level="error")

        await asyncio.gather(*tasks)

    async def process_single_item(
        self,
        session: aiohttp.ClientSession,
        title: str,
        description: str,
        img_url: str,
        time_element: WebElement
    ) -> None:
        date = time_element.text
        self.visitor.log(f"Processing article: {title}")
        date = convert_relative_time_to_datetime(date)
        phrase_count = count_phrase_occurrences(description, self.search_phrase)
        contains_money = check_for_money(description)

        filename = await download_image(session, img_url)
        self.sheet.append([title, date, description, filename, phrase_count, contains_money])