import aiohttp
import asyncio
from itertools import islice
from parse_module.parse_wb_site_class import ParseWbSiteClass
import random

async def main(NUMBER_OF_PARSING: int):
    parser = ParseWbSiteClass()
    articles = {}
    tasks = []
    
    list_of_nm_ids = [336610351,370705367,320841700,178821810,38373915,317331382,335747622,282089238,263451037,168821425,190404344,439715063,238260682,260206735,341775996,326427852,340651182,133534984,175756038,314981655,460291942,213542584,411564822,293426836,155804420,397447782,252158498,293920469,86753919,173429746]
    random_nm_ids = random.sample(list_of_nm_ids, NUMBER_OF_PARSING)
    
    async with aiohttp.ClientSession() as session:
        for nm_id in random_nm_ids:
            tasks.append(parser.parse_data_nm_id(session, nm_id, articles))
        await asyncio.gather(*tasks)

    
        # фото и видео качаем ПАРАЛЛЕЛЬНО
        await asyncio.gather(
            parser.parse_photo(articles),
            parser.parse_video(articles)
        )
        return articles
