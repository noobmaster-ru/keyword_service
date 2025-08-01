import aiohttp
from typing import Union
from parse_module.parsing_features.tools import Tools

class ParseDescription:
    async def parse_description(self, session: aiohttp.ClientSession, nm_id: str) ->  Union[str, list[str]]:
        try:
            int_nm_id = int(nm_id)
            short_nm_id = int_nm_id // 100000

            basket = Tools.build_basket(short_nm_id)

            headers_for_parse_description = {
                'sec-ch-ua-platform': '"Android"',
                'Referer': f'https://www.wildberries.ru/catalog/{nm_id}/detail.aspx',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
                'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                'sec-ch-ua-mobile': '?1',
            }
            url_for_parse_description = f"https://basket-{basket}.wbbasket.ru/vol{short_nm_id}/part{int_nm_id // 1000}/{nm_id}/info/ru/card.json"
            async with session.get(url_for_parse_description,headers=headers_for_parse_description,) as response:
                data = await response.json()
                return data["description"], data["colors"] # возвращаем описание товара и список всех его размеров/цветов(нужно будет в парсинге цены parse_card)   
        except Exception as e:
            print("Error in parse_description")
            return "Error in parse_description"