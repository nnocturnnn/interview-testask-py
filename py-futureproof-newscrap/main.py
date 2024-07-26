import asyncio
from logger_visitor import LoggerVisitor
from yahoo_scraper import YahooScraper

if __name__ == "__main__":
    driver_path = "/opt/homebrew/bin/chromedriver"
    search_phrase = "example search phrase"
    category = "example category"
    months = 1

    visitor = LoggerVisitor()
    scraper = YahooScraper(driver_path, search_phrase, category, months, visitor)
    asyncio.run(scraper.run())
