import aiohttp
import math
import asyncio
import json


class ParseWbSiteClass:
    def __init__(self, SEMAPHORE: asyncio.Semaphore):
        self.SEMAPHORE = SEMAPHORE
        self.PARAMS_PARSE_PAGE_TEMPLATE = {
            "ab_testid": "pfact_gr_1",
            "appType": "1",
            "curr": "rub",
            "dest": "-446115",
            "hide_dtype": "14",
            "lang": "ru",
            # required:  'page': page_number, required
            # required:  'query': query,
            "resultset": "catalog",
            "sort": "popular",
            "spp": "30",
            "suppressSpellcheck": "false",
            "uclusters": "2",
            "uiv": "0",
            "uv": "AQUAAQICAAEDAAoBAAIEAAMACco_P3C5Oj88vsc-50gRrVPE9ryaxvfC9jz0t064r0OtuGY9NbbFQalJlcWKslDEwzxJtPhDoMp4wxzE3rpWwR3FTkNfQ2Y1Wb01uv3EvMCEwAlI-EGcvSy_278bR_dCx8T3RdpEobiRSBZAWkL4P6I4AUHMRga8GDpzwwO9a8etQblEcD3IR1lEXL2HSVOxoa6APqfAlb7RxAa_UUeBQwvIDsKBwZXB1UAJRAnIHjgDN9hGuMa8QFpDbbxTwK_FNsEsvv0yjki2Qz5FbL11v6s55D49rnjGQ8elwZm0RkXov2NBiUB2OAI_C73EwRXEQcTgtNzBAr9IvOTBuESlRUoAN-wu-DKnMMEpEjTzAUge",
        }
        self.HEADERS_PARSE_PAGE_TEMPLATE = {
            "accept": "*/*",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTM0NTM3NjIsInVzZXIiOiI1NDU3MDMyNiIsInNoYXJkX2tleSI6IjEzIiwiY2xpZW50X2lkIjoid2IiLCJzZXNzaW9uX2lkIjoiM2Y0MmQ1YTY5MDJiNDhlNjgyYjQwYmE0NDNkOTMwMmMiLCJ2YWxpZGF0aW9uX2tleSI6IjQzZTQxMWM1ZDExODBjZWMzMzFhZGU3Y2ZiNmM1ODM2NzFkYTE0Nzg3ZGYyNWVmNjk3ZjQ0MzU0ODgwOTFlMDEiLCJwaG9uZSI6ImlGenNjbHNSSW5IYWJtSEhuM2JoVGc9PSIsInVzZXJfcmVnaXN0cmF0aW9uX2R0IjoxNjc1MjA3MjY5LCJ2ZXJzaW9uIjoyfQ.Rgsc1kGVk3bDbHZEvt37fIZI2kI2iINfo9KvR7wupxojoqQ507HqKhrEcyIynDAVJ4ivXh66m_cbiH1Li8vXI3DGFEskzAgKLvoPxyRKxbvEqqi3D_6jQUmW2o-Hy4DCm3Ij56guZhVskj0-DL7VM-nx6hOpXWgnp13571FtT0kkG5bG-rYco7_CgmK9w0PPp-ElRLd7xjue3wE8y9XA7Rk-MS4U4ZqlW6H8odC_82Woa3fjEJOYeLlVLBNzH_6JIO4LENeEtNtmyfdv_HTDCfw7X7pHuj-OMIzPnjq5NDCh5vcqqyH4sR7qKTrahFjXm47hC3kLUXPUPUqy4vY7jA",
            "origin": "https://www.wildberries.ru",
            "priority": "u=1, i",
            # required:  'referer': f'https://www.wildberries.ru/catalog/0/search.aspx?page={page_number}&sort=popular&search=%D0%B1%D1%83%D1%82%D1%8B%D0%BB%D0%BA%D0%B0+%D0%B4%D0%B5%D1%82%D1%81%D0%BA%D0%B0%D1%8F',
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
            "x-queryid": "qid127909588174272377820250725142812",
            "x-userid": "54570326",
        }

    def sort_key(self, item: dict):
        organic_pos = item[1]["organic_position"]
        return (organic_pos is None, organic_pos or 0)

    async def parse_card(self, session: aiohttp.ClientSession, nm_id: str) -> int | str:
        try:
            params = {
                "appType": "1",
                "curr": "rub",
                "dest": "-446115",
                "spp": "30",
                "hide_dtype": "14",
                "ab_testing": "false",
                "lang": "ru",
                "nm": nm_id,
            }
            async with session.get(
                "https://card.wb.ru/cards/v4/detail", params=params
            ) as resp:
                data = await resp.json()
                return data["products"][0]["sizes"][0]["price"]["product"]
        except Exception:
            return "Нет в наличии"

    async def parse_grade(
        self, session: aiohttp.ClientSession, nm_id: str
    ) -> int | str:
        try:
            params = {"curr": "RUB"}
            headers = self.HEADERS_PARSE_PAGE_TEMPLATE.copy()
            del headers["x-queryid"]
            del headers["x-userid"]
            headers["referer"] = (
                f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx?targetUrl=SP"
            )

            async with session.get(
                "https://user-grade.wildberries.ru/api/v5/grade",
                params=params,
                headers=headers,
            ) as resp:
                data = await resp.json()
                return data["payload"]["payments"][0]["full_discount"]
        except Exception:
            return "Нет в наличии"

    async def fetch_price(self, session: aiohttp.ClientSession, nm_id: str) -> dict:
        full_discount = await self.parse_grade(session, nm_id)
        price = await self.parse_card(session, nm_id)

        if isinstance(full_discount, int) and isinstance(price, int):
            wallet_price = math.floor((price / 100) * (1 - full_discount / 100))
            return wallet_price
        else:
            return "Нет в наличии"

    async def build_article(
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

            price = await self.fetch_price(session, nm_id)

            return {
                "id": product["id"],
                "organic_position": organic_pos,
                "promo_position": promo_pos,
                "price": price,
                "nmFeedbacks": product.get("nmFeedbacks"),
                "nmReviewRating": product.get("nmReviewRating"),
                "page": int(page_number),
                "link": f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx",
                "name": product.get("name"),
                "remains": product["wh"]
            }
        except Exception:
            return None

    async def parse_first_page(
        self, session: aiohttp.ClientSession, keyword: str, articles: dict
    ) -> dict:
        async with self.SEMAPHORE:
            try:
                headers = self.HEADERS_PARSE_PAGE_TEMPLATE.copy()
                headers["referer"] = (
                    "https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%B1%D1%83%D1%82%D1%8B%D0%BB%D0%BA%D0%B0%20%D0%B4%D0%B5%D1%82%D1%81%D0%BA%D0%B0%D1%8F"
                )

                params = self.PARAMS_PARSE_PAGE_TEMPLATE.copy()
                params["page"] = "1"
                params["query"] = keyword

                async with session.get(
                    "https://search.wb.ru/exactmatch/ru/common/v14/search",
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
                            self.build_article(session, product, 1, promo_position)
                        )
                        promo_position += 1
                    results = await asyncio.gather(*tasks)
                    articles.update({item["id"]: item for item in results if item})
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
        async with self.SEMAPHORE:
            try:
                headers = self.HEADERS_PARSE_PAGE_TEMPLATE.copy()
                headers["referer"] = (
                    f"https://www.wildberries.ru/catalog/0/search.aspx?page={page_number}&sort=popular&search=%D0%B1%D1%83%D1%82%D1%8B%D0%BB%D0%BA%D0%B0+%D0%B4%D0%B5%D1%82%D1%81%D0%BA%D0%B0%D1%8F"
                )

                params = self.PARAMS_PARSE_PAGE_TEMPLATE.copy()
                params["page"] = page_number
                params["query"] = keyword

                async with session.get(
                    "https://search.wb.ru/exactmatch/ru/common/v14/search",
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
                            self.build_article(
                                session, product, page_number, promo_position
                            )
                        )
                        promo_position += 1
                    results = await asyncio.gather(*tasks)
                    articles.update({item["id"]: item for item in results if item})
            except Exception as e:
                print(f"Error in parse_page_number_ {str(e)[:300]}")
                return {}
