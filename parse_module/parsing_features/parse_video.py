import asyncio

from parse_module.parsing_features.tools import Tools


class ParseVideo:
    def __init__(self):
        pass

    async def parse_video(self, articles: dict):
        tasks = [self._parse_video(articles[key]) for key in articles]
        await asyncio.gather(*tasks)

    async def _parse_video(self, article: dict):
        nm_id = int(article["nm_id"])
        basket, vol_value = Tools.build_basket_for_video(nm_id)
        m3u8_url = f"https://videonme-basket-{basket}.wbbasket.ru/vol{vol_value}/part{nm_id // 10000}/{nm_id}/hls/1440p/index.m3u8"
        article["link_to_video"] = m3u8_url

