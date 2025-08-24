import aiohttp
import asyncio
import json
from urllib.parse import quote

from parse_module.parsing_features.parse_price import ParsePrice
from parse_module.parsing_features.parse_photo import ParsePhoto
from parse_module.parsing_features.parse_description import ParseDescription
from parse_module.parsing_features.tools import Tools
from parse_module.parsing_features.parse_feedbacks import ParseFiveLastFeedback
from parse_module.parsing_features.parse_video import ParseVideo

from parse_module.parsing_features.parse_card import ParseDataCard


class ParseWbSiteClass(
    ParsePrice, ParsePhoto, ParseDescription, Tools, ParseFiveLastFeedback, ParseVideo, ParseDataCard
):
    def __init__(self):
        self.PARAMS_PARSE_PAGE_TEMPLATE = {
            "ab_testid": "pfact_gr_1",
            "ab_testing": "false",
            "appType": "1",
            "curr": "rub",
            "dest": "-446115",
            "hide_dtype": "14",
            "inheritFilters": "false",
            "lang": "ru",
            # required:  'page': page_number, 
            # required:  'query': query,
            "resultset": "catalog",
            "sort": "popular",
            "spp": "30",
            "suppressSpellcheck": "false",
            "uclusters": "2",
            "uiv": "0",
            'uv': 'AQUAAQIBAAICAAEEAAMDAAoACco_P3C5Oj88vsc-50gRrVPE9ryaxvfC9jz0t064r0OtuGY9NbbFQalJlcWKslDEwzxJtPhDoMp4wxzE3rpWwR3FTkNfQ2Y1Wb01uv3EvMCEwAlI-EGcvSy_278bR_dCx8T3RdpEobiRSBZAWkL4P6I4AUHMRga8GDpzwwO9a8etQblEcD3IR1lEXL2HSVOxoa6APqfAlb7RxAa_UUeBQwvIDsKBwZXB1UAJRAnIHjgDN9hGuMa8QFpDbbxTwK_FNsEsvv0yjki2Qz5FbL11v6s55D49rnjGQ8elwZm0RkXov2NBiUB2OAI_C73EwRXEQcTgtNzBAr9IvOTBuESlRUoyhgABTB437C74MqcwwSkS',
            #"uv": "AQUAAQICAAEDAAoBAAIEAAMACco_P3C5Oj88vsc-50gRrVPE9ryaxvfC9jz0t064r0OtuGY9NbbFQalJlcWKslDEwzxJtPhDoMp4wxzE3rpWwR3FTkNfQ2Y1Wb01uv3EvMCEwAlI-EGcvSy_278bR_dCx8T3RdpEobiRSBZAWkL4P6I4AUHMRga8GDpzwwO9a8etQblEcD3IR1lEXL2HSVOxoa6APqfAlb7RxAa_UUeBQwvIDsKBwZXB1UAJRAnIHjgDN9hGuMa8QFpDbbxTwK_FNsEsvv0yjki2Qz5FbL11v6s55D49rnjGQ8elwZm0RkXov2NBiUB2OAI_C73EwRXEQcTgtNzBAr9IvOTBuESlRUoAN-wu-DKnMMEpEjTzAUge",
        }
        self.HEADERS_PARSE_PAGE_TEMPLATE = {
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTU4ODEzNTMsInVzZXIiOiI1NDU3MDMyNiIsInNoYXJkX2tleSI6IjEzIiwiY2xpZW50X2lkIjoid2IiLCJzZXNzaW9uX2lkIjoiM2Y0MmQ1YTY5MDJiNDhlNjgyYjQwYmE0NDNkOTMwMmMiLCJ2YWxpZGF0aW9uX2tleSI6IjQzZTQxMWM1ZDExODBjZWMzMzFhZGU3Y2ZiNmM1ODM2NzFkYTE0Nzg3ZGYyNWVmNjk3ZjQ0MzU0ODgwOTFlMDEiLCJwaG9uZSI6ImlGenNjbHNSSW5IYWJtSEhuM2JoVGc9PSIsInVzZXJfcmVnaXN0cmF0aW9uX2R0IjoxNjc1MjA3MjY5LCJ2ZXJzaW9uIjoyfQ.DOJ_5xov3BiZh5ywNJJtRtlnFziv_Y3F6mMm7_iEkdPdAaWpbFoZVGgjw68n91tGuty3w6hwZsADNkM8dnzU-sfc31vnzqDqOybS4GKfjO53LIX8ZbPCrVjVPUlLder70aYad1luOUMaiKOYCmDlZ6rRJsGGhmFZN66GTGKTAv27GHFB7HVac-AvbuofE8Zt9zyv0zhQ6Jy_tPQT9m7Ac02GobiV5SLT-sbTjwzDTEV3UevFdVHzSCOScMB0uWtSKMnQJIGMdBajhnZtdy_2d3GXYPrta9xn19Luauugw5PwQ059qYM-8U2QdoRyzPNfM5M6nBVT-ibjjAqje8UgKQ',
            'origin': 'https://www.wildberries.ru',
            'priority': 'u=1, i',
            # 'referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%B1%D1%80%D1%8E%D0%BA%D0%B8',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'x-pow': '',
            'x-queryid': 'qid127909588174272377820250824145139',
            'x-userid': '54570326',
        }

    async def parse_data_nm_id(
        self,
        session: aiohttp.ClientSession,
        nm_id: str,
        articles: dict
    ) -> None:
        description, list_of_nm_ids = await self.parse_description(session, nm_id)

        # но пока оно грузилось, параллельно грузились отзывы
        feedback_task =  self.parse_last_five_feedbacks_rating(session, nm_id)
        data_card_task = self.parse_data_card(session, nm_id)

        data_card, data_feedbacks = await asyncio.gather(data_card_task, feedback_task)

        articles[nm_id] = { 
            "nm_id": nm_id,
            "price": data_card["price"],
            "nmFeedbacks": data_card["nmFeedbacks"],
            "nmReviewRating": data_card["nmReviewRating"],
            "five_last_feedbacks_rating": data_feedbacks[0],
            "text_of_last_feedbacks": {
                f"feedback_{i+1}": text for i, text in enumerate(data_feedbacks[1])
            },
            "rate_of_last_feedbacks": {
                f"rate_{i+1}": rate for i, rate in enumerate(data_feedbacks[2])
            },
            "link": f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx",
            "name": data_card["name"],
            "remains": data_card["remains"],
            "number_of_images": data_card["number_of_images"],
            "description": description,
        }

    async def build_data_nm_id_keyword(
        self,
        session: aiohttp.ClientSession,
        product: dict,
        page_number: int | str,
        promo_position: int,
    ) -> dict | None:
        try:
            nm_id = str(product["id"])
            organic_pos = product["log"].get("position", None)
            promo_pos = product["log"].get("promoPosition", promo_position)


            desc_task = self.parse_description(session, nm_id)
            feedback_task = self.parse_last_five_feedbacks_rating(session, nm_id)

            # ждем сначала описание, чтобы получить list_of_nm_ids
            description, list_of_nm_ids = await desc_task

            # но пока оно грузилось, параллельно грузились отзывы
            price_task = self.fetch_price(session, nm_id, list_of_nm_ids)
            price, data_feedbacks = await asyncio.gather(price_task, feedback_task)

            return {
                "nm_id": product["id"],
                "organic_position": organic_pos,
                "promo_position": promo_pos,
                "price": price,
                "nmFeedbacks": product.get("nmFeedbacks"),
                "nmReviewRating": product.get("nmReviewRating"),
                "five_last_feedbacks_rating": data_feedbacks[0],
                "text_of_last_feedbacks": {
                    f"feedback_{i+1}": {
                        "cons": text[0],
                        "text": text[1],
                        "pros": text[2]
                    } for i, text in enumerate(data_feedbacks[1])
                },
                "rate_of_last_feedbacks": {
                    f"rate_{i+1}": rate for i, rate in enumerate(data_feedbacks[2])
                },
                "page": int(page_number),
                "link": f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx",
                "name": product.get("name"),
                "remains": product["totalQuantity"],
                "number_of_images": product["pics"],
                "description": description,
            }
        except Exception:
            return None

    async def parse_first_page(
        self, session: aiohttp.ClientSession, keyword: str, articles: dict
    ) -> dict:
        try:
            headers = self.HEADERS_PARSE_PAGE_TEMPLATE.copy()
            encoded_word = quote(keyword)
            headers["referer"] = (
                f"https://www.wildberries.ru/catalog/0/search.aspx?search={encoded_word}"
            )

            params = self.PARAMS_PARSE_PAGE_TEMPLATE.copy()
            params["page"] = "1"
            params["query"] = keyword

            async with session.get(
                "https://search.wb.ru/exactmatch/ru/common/v18/search",
                params=params,
                headers=headers,
            ) as response:
                data_json = json.loads(
                    await response.text()
                )  # response.json() выдает error: 200, message='Attempt to decode JSON with unexpected mimetype: text/plain;
                products = data_json.get("products")

                promo_position = 0
                tasks = []
                for product in products:
                    tasks.append(
                        self.build_data_nm_id_keyword(session, product, 1, promo_position)
                    )
                    promo_position += 1
                results = await asyncio.gather(*tasks)
                articles.update({item["nm_id"]: item for item in results if item})
        except Exception as e:
            print(f"Eror in parse_first_page , {str(e)[:300]}")
            return {}

    async def parse_page_number_(
        self,
        session: aiohttp.ClientSession,
        keyword: str,
        page_number: str,
        articles: dict,
    ) -> dict:
        try:
            headers = self.HEADERS_PARSE_PAGE_TEMPLATE.copy()
            encoded_word = quote(keyword)
            headers["referer"] = (
                f"https://www.wildberries.ru/catalog/0/search.aspx?page={page_number}&sort=popular&search={encoded_word}"
            )

            params = self.PARAMS_PARSE_PAGE_TEMPLATE.copy()
            params["page"] = page_number
            params["query"] = keyword

            async with session.get(
                "https://search.wb.ru/exactmatch/ru/common/v18/search",
                params=params,
                headers=headers,
            ) as response:
                data_json = json.loads(
                    await response.text()
                )  # response.json() выдает error: 200, message='Attempt to decode JSON with unexpected mimetype: text/plain;
                products = data_json.get("products")
                promo_position = 0

                tasks = []
                for product in products:
                    tasks.append(
                        self.build_data_nm_id_keyword(
                            session, product, page_number, promo_position
                        )
                    )
                    promo_position += 1
                results = await asyncio.gather(*tasks)
                articles.update({item["nm_id"]: item for item in results if item})
        except Exception as e:
            print(f"Error in parse_page_number_ {str(e)[:300]}")
            return {}
