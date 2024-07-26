from abc import ABC, abstractmethod
from typing import Optional, Generator
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from openpyxl import Workbook, worksheet
from logger_visitor import LoggerVisitor
import aiohttp
from misc import (
    setup_excel_sheet,
    save_to_excel,
)

class NewsScraper(ABC):
    def __init__(
        self,
        driver_path: str,
        search_phrase: str,
        category: str,
        months: int,
        base_url: str,
        visitor: LoggerVisitor
    ):
        self.driver_path: str = driver_path
        self.search_phrase: str = search_phrase
        self.category: str = category
        self.months: int = months
        self.driver: Optional[webdriver.Chrome] = None
        self.base_url: str = base_url
        self.workbook: Workbook = Workbook()
        self.sheet: worksheet.Worksheet = setup_excel_sheet(self.workbook)
        self.visitor = visitor

    def setup_driver(self) -> None:
        self.visitor.log("Setting up driver")
        options: webdriver.ChromeOptions = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            },
        )

    def close_driver(self) -> None:
        if self.driver:
            self.visitor.log("Closing driver")
            self.driver.quit()

    @abstractmethod
    def search_news(self) -> None:
        pass

    @abstractmethod
    def scroll_and_collect_articles(self) -> Generator[WebElement, None, None]:
        pass

    @abstractmethod
    async def process_news_items(self, session: aiohttp.ClientSession) -> None:
        pass

    @abstractmethod
    async def process_single_item(
        self,
        session: aiohttp.ClientSession,
        title: str,
        description: str,
        img_url: str,
        article_url: str,
    ) -> None:
        pass

    async def run(self) -> None:
        self.setup_driver()
        try:
            self.visitor.log("Starting news search")
            self.search_news()
            async with aiohttp.ClientSession() as session:
                await self.process_news_items(session)
        finally:
            self.close_driver()
        save_to_excel(self.workbook, "news_data.xlsx")
        self.visitor.log("Data saved to news_data.xlsx")
