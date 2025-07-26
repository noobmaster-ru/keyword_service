import aiohttp 
import asyncio

from service.parse_wb_site_class import ParseWbSiteClass


def sort_key(item):
    organic_pos = item[1]["organic_position"]
    # Если organic_position None, возвращаем очень большое число, чтобы элемент попал в конец
    return (organic_pos is None, organic_pos if organic_pos is not None else 0)

async def main(keyword: str):
    articles = {}
    SEMAPHORE = asyncio.Semaphore(2000)
    parser = ParseWbSiteClass(SEMAPHORE)
    async with aiohttp.ClientSession() as session:
        articles = await parser.parse_first_page(session, keyword, articles)
        for page_number in ['2', '3', '4']:
            articles = await parser.parse_page_number_(session, keyword, page_number, articles)

    return dict(sorted(articles.items(), key=sort_key)) # сортировка по возврастанию organic_position
    