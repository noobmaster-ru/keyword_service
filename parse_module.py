import aiohttp
import asyncio
from itertools import islice

from service.parse_wb_site_class import ParseWbSiteClass


async def main(keyword: str):
    SEMAPHORE = asyncio.Semaphore(100)
    parser = ParseWbSiteClass(SEMAPHORE)
    articles = {}
    tasks = []
    async with aiohttp.ClientSession() as session:
        tasks.append(parser.parse_first_page(session, keyword, articles))
        tasks.append(parser.parse_page_number_(session, keyword, "2", articles))
        tasks.append(parser.parse_page_number_(session, keyword, "3", articles))
        await asyncio.gather(*tasks)
        result = dict(
            sorted(articles.items(), key=parser.sort_key) # сортировка по возврастанию organic_position
        ) 
        return dict(islice(result.items(), 20))

