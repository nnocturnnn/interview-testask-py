import re
import aiohttp
from bs4 import BeautifulSoup
from openpyxl import Workbook, worksheet
import os
from typing import Optional
from datetime import datetime, timedelta


async def download_image(session: aiohttp.ClientSession, img_url: str) -> Optional[str]:
    try:
        async with session.get(img_url) as response:
            response.raise_for_status()
            filename = os.path.basename(img_url)
            with open(filename, "wb") as file:
                file.write(await response.read())
        return filename
    except aiohttp.ClientError as e:
        print(f"Error downloading image: {e}")
        return None


def count_phrase_occurrences(text: str, phrase: str) -> int:
    combined_text = text.lower()
    return combined_text.count(phrase.lower())


def check_for_money(text: str) -> bool:
    money_pattern = re.compile(r"\$\d+(\.\d{1,2})?|USD|\d+ dollars", re.IGNORECASE)
    return bool(money_pattern.search(text))


def setup_excel_sheet(workbook: Workbook) -> worksheet:
    sheet = workbook.active
    sheet.append(
        [
            "Title",
            "Date",
            "Description",
            "Image Filename",
            "Phrase Count",
            "Contains Money",
        ]
    )
    return sheet


def save_to_excel(workbook: Workbook, file_path: str) -> None:
    workbook.save(file_path)


async def get_article_date(session: aiohttp.ClientSession, url: str) -> str:
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.text()
            soup = BeautifulSoup(content, "html.parser")
            date_tag = soup.find("time")
            if date_tag:
                return date_tag.get("datetime")
            else:
                return "Date not found"
    except aiohttp.ClientError as e:
        print(f"Error fetching article date: {e}")
        return "Failed to retrieve the webpage"
    

def convert_relative_time_to_datetime(relative_time: str) -> Optional[datetime]:
    now = datetime.now()
    match = re.match(r"(\d+)\s*(minute|hour|day|week|month|year)s?\s*ago", relative_time, re.IGNORECASE)
    if not match:
        return relative_time
    
    quantity = int(match.group(1))
    unit = match.group(2).lower()

    delta_dict = {
        "minute": timedelta(minutes=quantity),
        "hour": timedelta(hours=quantity),
        "day": timedelta(days=quantity),
        "week": timedelta(weeks=quantity),
        "month": timedelta(days=30 * quantity),
        "year": timedelta(days=365 * quantity) 
    }

    if unit not in delta_dict:
        raise ValueError("The time unit is not recognized.")

    delta = delta_dict[unit]
    return now - delta