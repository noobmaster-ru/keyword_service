import aiohttp
import asyncio
from itertools import islice
import json
from parse_module.parse_wb_site_class import ParseWbSiteClass


async def main(keyword: str, NUMBER_OF_PARSING: int):
    # SEMAPHORE = asyncio.Semaphore(100)  # можно поставить 20 или 50
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

        # парсим ПЕРВОЕ фото и ОПИСАНИЕ только для первых NUMBER_OF_PARSING артикулов отсортированных
        await parser.parse_photo(result_answer_parsing)

        with open(
            f".data/result_answer_parsing_{keyword}.json", "w", encoding="utf-8"
        ) as f:
            json.dump(result_answer_parsing, f, indent=4, ensure_ascii=False)
        return result_answer_parsing
