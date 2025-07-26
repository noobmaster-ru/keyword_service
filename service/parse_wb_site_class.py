import aiohttp
import math
import asyncio
import random 

class ParseWbSiteClass:
    def __init__(self, SEMAPHORE):
        self.SEMAPHORE = SEMAPHORE

    async def parse_card(self, session: aiohttp.ClientSession, nm_id: str) -> int | str:
        async with self.SEMAPHORE:
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
                await asyncio.sleep(random.uniform(0.5, 1.5))  # перед запросом
                async with session.get(
                    "https://card.wb.ru/cards/v4/detail", params=params
                ) as resp:
                    if resp.content_type != "application/json":
                        text = await resp.text()
                        print("⚠️ НЕ JSON:", text[:500])  # чтобы увидеть, что пришло от WB
                        return {}

                    try:
                        data = await resp.json()
                    except Exception as e:
                        print(f"Ошибка при JSON-декодировании: {e}")
                        return {}
                    return data["products"][0]["sizes"][0]["price"]["product"]
            except Exception:
                return "Нет в наличии"

    async def parse_grade(
        self, session: aiohttp.ClientSession, nm_id: str
    ) -> int | str:
        async with self.SEMAPHORE:
            try:
                params = {"curr": "RUB"}
                headers = {
                    "accept": "*/*",
                    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTMyODA5NTAsInVzZXIiOiI1NDU3MDMyNiIsInNoYXJkX2tleSI6IjEzIiwiY2xpZW50X2lkIjoid2IiLCJzZXNzaW9uX2lkIjoiM2Y0MmQ1YTY5MDJiNDhlNjgyYjQwYmE0NDNkOTMwMmMiLCJ2YWxpZGF0aW9uX2tleSI6IjQzZTQxMWM1ZDExODBjZWMzMzFhZGU3Y2ZiNmM1ODM2NzFkYTE0Nzg3ZGYyNWVmNjk3ZjQ0MzU0ODgwOTFlMDEiLCJwaG9uZSI6ImlGenNjbHNSSW5IYWJtSEhuM2JoVGc9PSIsInVzZXJfcmVnaXN0cmF0aW9uX2R0IjoxNjc1MjA3MjY5LCJ2ZXJzaW9uIjoyfQ.j9wIg5qrJQ704rUBoGluS799qRoPMo5jAntv6oAnWeZG3ziD1dYR6Wusv-YE_InVoJP8IOpxdsODn5m2L7mrdCG-3YTl4wBz1MRRblvdxUpeBHiGZUHwE0t1bVDDpxv-NjcTVpjTnuAnvTXeMlciTJhnofkzO_Af6wHw-WpyKc-QMoiYb0qlY2qL1YKRMoQ4eTL6S4gvR5aBu-yL4i32tElhrCugn6sLKPjTpGuuzr6KLXflAolrLQ9nVNxX-R0CrMIm_PEiNo1sNFs19a2zTYg6cL9rDEK9L_JZbXcZQJTPkO7o4hTzb3bRp0zIoPnLGinZGmaHONeE2wNoZpxz8g",
                    "origin": "https://www.wildberries.ru",
                    "priority": "u=1, i",
                    "referer": f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx?targetUrl=SP",
                    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                    "sec-ch-ua-mobile": "?1",
                    "sec-ch-ua-platform": '"Android"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
                }
                await asyncio.sleep(random.uniform(0.5, 1.5))  # перед запросом
                async with session.get(
                    "https://user-grade.wildberries.ru/api/v5/grade",
                    params=params,
                    headers=headers,
                ) as resp:
                    if resp.content_type != "application/json":
                        text = await resp.text()
                        print("⚠️ НЕ JSON:", text[:500])  # чтобы увидеть, что пришло от WB
                        return {}

                    try:
                        data = await resp.json()
                    except Exception as e:
                        print(f"Ошибка при JSON-декодировании: {e}")
                        return {}
                    return data["payload"]["payments"][0]["full_discount"]
            except Exception:
                return "Нет в наличии"

    async def fetch_price(
        self, session: aiohttp.ClientSession, nm_id: str
    ) -> dict:
        full_discount = await self.parse_grade(session, nm_id)
        price = await self.parse_card(session, nm_id)

        if isinstance(full_discount, int) and isinstance(price, int):
            wallet_price = math.floor((price / 100) * (1 - full_discount / 100))
            return wallet_price
        else:
            return "Нет в наличии"
    
    async def parse_promo_position_first_page(
        self, session: aiohttp.ClientSession, query: str, articles: dict
    )-> dict:
        async with self.SEMAPHORE:
            headers = {
                'accept': '*/*',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTMyODA5NTAsInVzZXIiOiI1NDU3MDMyNiIsInNoYXJkX2tleSI6IjEzIiwiY2xpZW50X2lkIjoid2IiLCJzZXNzaW9uX2lkIjoiM2Y0MmQ1YTY5MDJiNDhlNjgyYjQwYmE0NDNkOTMwMmMiLCJ2YWxpZGF0aW9uX2tleSI6IjQzZTQxMWM1ZDExODBjZWMzMzFhZGU3Y2ZiNmM1ODM2NzFkYTE0Nzg3ZGYyNWVmNjk3ZjQ0MzU0ODgwOTFlMDEiLCJwaG9uZSI6ImlGenNjbHNSSW5IYWJtSEhuM2JoVGc9PSIsInVzZXJfcmVnaXN0cmF0aW9uX2R0IjoxNjc1MjA3MjY5LCJ2ZXJzaW9uIjoyfQ.j9wIg5qrJQ704rUBoGluS799qRoPMo5jAntv6oAnWeZG3ziD1dYR6Wusv-YE_InVoJP8IOpxdsODn5m2L7mrdCG-3YTl4wBz1MRRblvdxUpeBHiGZUHwE0t1bVDDpxv-NjcTVpjTnuAnvTXeMlciTJhnofkzO_Af6wHw-WpyKc-QMoiYb0qlY2qL1YKRMoQ4eTL6S4gvR5aBu-yL4i32tElhrCugn6sLKPjTpGuuzr6KLXflAolrLQ9nVNxX-R0CrMIm_PEiNo1sNFs19a2zTYg6cL9rDEK9L_JZbXcZQJTPkO7o4hTzb3bRp0zIoPnLGinZGmaHONeE2wNoZpxz8g',
                'origin': 'https://www.wildberries.ru',
                'priority': 'u=1, i',
                'referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%B1%D1%83%D1%82%D1%8B%D0%BB%D0%BA%D0%B0%20%D0%B4%D0%B5%D1%82%D1%81%D0%BA%D0%B0%D1%8F',
                'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
                'x-queryid': 'qid127909588174272377820250725134448',
                'x-userid': '54570326',
            }

            params = {
                'ab_testid': 'pfact_gr_1',
                'appType': '1',
                'curr': 'rub',
                'dest': '-446115',
                'hide_dtype': '14',
                'lang': 'ru',
                'page': '1',
                'query': query,
                'resultset': 'catalog',
                'sort': 'popular',
                'spp': '30',
                'suppressSpellcheck': 'false',
                'uclusters': '2',
                'uiv': '0',
                'uv': 'AQUAAQICAAEDAAoBAAIEAAMACco_P3C5Oj88vsc-50gRrVPE9ryaxvfC9jz0t064r0OtuGY9NbbFQalJlcWKslDEwzxJtPhDoMp4wxzE3rpWwR3FTkNfQ2Y1Wb01uv3EvMCEwAlI-EGcvSy_278bR_dCx8T3RdpEobiRSBZAWkL4P6I4AUHMRga8GDpzwwO9a8etQblEcD3IR1lEXL2HSVOxoa6APqfAlb7RxAa_UUeBQwvIDsKBwZXB1UAJRAnIHjgDN9hGuMa8QFpDbbxTwK_FNsEsvv0yjki2Qz5FbL11v6s55D49rnjGQ8elwZm0RkXov2NBiUB2OAI_C73EwRXEQcTgtNzBAr9IvOTBuESlRUoAN-wu-DKnMMEpEjTzAUge',
            }
            await asyncio.sleep(random.uniform(0.5, 1.5))  # перед запросом
            async with session.get(
                'https://search.wb.ru/exactmatch/ru/common/v14/search',
                params=params, 
                headers=headers
            ) as response:
                if response.content_type != "application/json":
                    text = await response.text()
                    print("⚠️ НЕ JSON:", text[:500])  # чтобы увидеть, что пришло от WB
                    return {}

                try:
                    data = await response.json()
                except Exception as e:
                    print(f"Ошибка при JSON-декодировании: {e}")
                    return {}
                
                products = data.get("products", [])
                if not products:
                    print("⚠️ Нет products в ответе от WB")
                    return articles
                promo_position = 0
                for product in products:
                    try:
                        log = product["log"]
                        articles[product["id"]] = {
                            "organic_position": log["position"],
                            "promo_position": log["promoPosition"],
                            "wb_wallet_price": await self.fetch_price(session, product["id"]),
                            "number_feedbacks": product["nmFeedbacks"],
                            "nmReviewRating": product["nmReviewRating"],
                            "name": product["name"],
                            "page": 1
                        }
                    except Exception as e:
                        print("promo_position = ",promo_position, product["id"],  "Нет log")
                        articles[product["id"]] ={
                            "organic_position": None,
                            "promo_position": promo_position,
                            "wb_wallet_price": await self.fetch_price(session, product["id"]),
                            "number_feedbacks": product["nmFeedbacks"],
                            "nmReviewRating": product["nmReviewRating"],
                            "name": product["name"],
                            "page": 1
                        }
                    promo_position += 1
                return articles
            
    async def parse_promo_position_page_number_(
        self, session: aiohttp.ClientSession, query: str, page_number: str, articles: dict
    ) -> dict:
        headers = {
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTM0NTM3NjIsInVzZXIiOiI1NDU3MDMyNiIsInNoYXJkX2tleSI6IjEzIiwiY2xpZW50X2lkIjoid2IiLCJzZXNzaW9uX2lkIjoiM2Y0MmQ1YTY5MDJiNDhlNjgyYjQwYmE0NDNkOTMwMmMiLCJ2YWxpZGF0aW9uX2tleSI6IjQzZTQxMWM1ZDExODBjZWMzMzFhZGU3Y2ZiNmM1ODM2NzFkYTE0Nzg3ZGYyNWVmNjk3ZjQ0MzU0ODgwOTFlMDEiLCJwaG9uZSI6ImlGenNjbHNSSW5IYWJtSEhuM2JoVGc9PSIsInVzZXJfcmVnaXN0cmF0aW9uX2R0IjoxNjc1MjA3MjY5LCJ2ZXJzaW9uIjoyfQ.Rgsc1kGVk3bDbHZEvt37fIZI2kI2iINfo9KvR7wupxojoqQ507HqKhrEcyIynDAVJ4ivXh66m_cbiH1Li8vXI3DGFEskzAgKLvoPxyRKxbvEqqi3D_6jQUmW2o-Hy4DCm3Ij56guZhVskj0-DL7VM-nx6hOpXWgnp13571FtT0kkG5bG-rYco7_CgmK9w0PPp-ElRLd7xjue3wE8y9XA7Rk-MS4U4ZqlW6H8odC_82Woa3fjEJOYeLlVLBNzH_6JIO4LENeEtNtmyfdv_HTDCfw7X7pHuj-OMIzPnjq5NDCh5vcqqyH4sR7qKTrahFjXm47hC3kLUXPUPUqy4vY7jA',
            'origin': 'https://www.wildberries.ru',
            'priority': 'u=1, i',
            'referer': f'https://www.wildberries.ru/catalog/0/search.aspx?page={page_number}&sort=popular&search=%D0%B1%D1%83%D1%82%D1%8B%D0%BB%D0%BA%D0%B0+%D0%B4%D0%B5%D1%82%D1%81%D0%BA%D0%B0%D1%8F',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
            'x-queryid': 'qid127909588174272377820250725142812',
            'x-userid': '54570326',
        }

        params = {
            'ab_testid': 'pfact_gr_1',
            'appType': '1',
            'curr': 'rub',
            'dest': '-446115',
            'hide_dtype': '14',
            'lang': 'ru',
            'page': page_number,
            'query': query,
            'resultset': 'catalog',
            'sort': 'popular',
            'spp': '30',
            'suppressSpellcheck': 'false',
            'uclusters': '2',
            'uiv': '0',
            'uv': 'AQUAAQICAAEDAAoBAAIEAAMACco_P3C5Oj88vsc-50gRrVPE9ryaxvfC9jz0t064r0OtuGY9NbbFQalJlcWKslDEwzxJtPhDoMp4wxzE3rpWwR3FTkNfQ2Y1Wb01uv3EvMCEwAlI-EGcvSy_278bR_dCx8T3RdpEobiRSBZAWkL4P6I4AUHMRga8GDpzwwO9a8etQblEcD3IR1lEXL2HSVOxoa6APqfAlb7RxAa_UUeBQwvIDsKBwZXB1UAJRAnIHjgDN9hGuMa8QFpDbbxTwK_FNsEsvv0yjki2Qz5FbL11v6s55D49rnjGQ8elwZm0RkXov2NBiUB2OAI_C73EwRXEQcTgtNzBAr9IvOTBuESlRUoAN-wu-DKnMMEpEjTzAUge',
        }
        async with self.SEMAPHORE:
            await asyncio.sleep(random.uniform(0.5, 1.5))  # перед запросом
            async with session.get(
                'https://search.wb.ru/exactmatch/ru/common/v14/search',
                params=params,
                headers=headers,
            ) as response:
                if response.content_type != "application/json":
                    text = await response.text()
                    print("⚠️ НЕ JSON:", text[:500])  # чтобы увидеть, что пришло от WB
                    return {}

                try:
                    data = await response.json()
                except Exception as e:
                    print(f"Ошибка при JSON-декодировании: {e}")
                    return {}
                products = data.get("products", [])
                if not products:
                    print("⚠️ Нет products в ответе от WB")
                    return articles
                promo_position = 0

                for product in products:
                    try:
                        log = product["log"]
                        articles[product["id"]] = {
                            "organic_position": log["position"],
                            "promo_position": log["promoPosition"],
                            "wb_wallet_price": await self.fetch_price(session, product["id"]),
                            "number_feedbacks": product["nmFeedbacks"],
                            "nmReviewRating": product["nmReviewRating"],
                            "name": product["name"],
                            "page": int(page_number)
                        }
                    except Exception as e:
                        print("promo_position = ", promo_position, product["id"],  "Нет log")
                        articles[product["id"]] ={
                            "organic_position": None,
                            "promo_position": promo_position,
                            "wb_wallet_price": await self.fetch_price(session, product["id"]),
                            "number_feedbacks": product["nmFeedbacks"],
                            "nmReviewRating": product["nmReviewRating"],
                            "name": product["name"],
                            "page": int(page_number)
                        }
                    promo_position += 1
                # with open(f"results/{query}_page{page_number}.json", "w", encoding="utf-8") as f:
                #     json.dump(page, f, indent=4, ensure_ascii=False)

                return articles