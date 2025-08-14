import aiohttp
import asyncio
from itertools import islice
from parse_module.parse_wb_site_class import ParseWbSiteClass


async def main(keyword: str, NUMBER_OF_PARSING: int):
    parser = ParseWbSiteClass()
    articles = {}
    tasks = []
    async with aiohttp.ClientSession() as session:
        tasks.append(parser.parse_first_page(session, keyword, articles))
        tasks.append(parser.parse_page_number_(session, keyword, "2", articles))
        tasks.append(parser.parse_page_number_(session, keyword, "3", articles))
        await asyncio.gather(*tasks)

        result = dict(
            sorted(
                articles.items(), key=parser.sort_key
            )  # сортировка по возврастанию organic_position
        )
        result_answer_parsing = dict(islice(result.items(), NUMBER_OF_PARSING))

    
        # фото и видео качаем ПАРАЛЛЕЛЬНО
        await asyncio.gather(
            parser.parse_photo(result_answer_parsing),
            parser.parse_video(result_answer_parsing)
        )
        return result_answer_parsing
