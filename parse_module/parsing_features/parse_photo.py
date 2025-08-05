import aiohttp
import asyncio
from parse_module.parsing_features.tools import Tools


class ParsePhoto:
    def __init__(self):
        pass

    async def parse_photo(self, articles: dict):
        tasks = []
        for index, key in enumerate(articles):
            tasks.append(self._parse_photo(articles[key]))
        await asyncio.gather(*tasks)

    # основу кода функции взял с https://github.com/Duff89/wildberries_parser/blob/master/parser.py
    async def _parse_photo(
        self, article: dict
    ):
        try:
            nm_id = int(article["nm_id"])
            short_nm_id = nm_id // 100000

            basket = Tools.build_basket(short_nm_id)

            link_url_all_photos = "".join(
                [
                    f"https://basket-{basket}.wbbasket.ru/vol{short_nm_id}/part{nm_id // 1000}/{nm_id}/images/big/{i}.webp;"
                    for i in range(1, article["number_of_images"] + 1)
                ]
            )
            article["link_to_photos"] = link_url_all_photos
        except Exception as e:
            print(f"❌ Error downloading photo for {article.get('nm_id')}: {e}")
