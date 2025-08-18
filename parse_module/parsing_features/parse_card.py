import aiohttp
import math
import asyncio
import json

class ParseDataCard:
    def __init__(self):
        pass
    
    async def parse_data_card(
        self, session: aiohttp.ClientSession, nm_id: str
    ) -> dict:
        full_discount_task = self.parse_discount(session, nm_id)
        data_card_task = self.parse_other_data_card(session, nm_id)
        

        full_discount, data_card = await asyncio.gather(full_discount_task, data_card_task) 
        if isinstance(full_discount, int) and isinstance(data_card["price"], int):
            wallet_price = math.floor((data_card["price"] / 100) * (1 - full_discount / 100))
            data_card["price"] = wallet_price
        else:
            data_card["price"] = "Нет в наличии"
        return data_card

    
    async def parse_discount(
        self, session: aiohttp.ClientSession, nm_id: str
    ) -> int | str:
        try:
            params = {"curr": "RUB"}
            headers = {
                'accept': '*/*',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NTU0NTA0OTgsInVzZXIiOiI1NDU3MDMyNiIsInNoYXJkX2tleSI6IjEzIiwiY2xpZW50X2lkIjoid2IiLCJzZXNzaW9uX2lkIjoiM2Y0MmQ1YTY5MDJiNDhlNjgyYjQwYmE0NDNkOTMwMmMiLCJ2YWxpZGF0aW9uX2tleSI6IjQzZTQxMWM1ZDExODBjZWMzMzFhZGU3Y2ZiNmM1ODM2NzFkYTE0Nzg3ZGYyNWVmNjk3ZjQ0MzU0ODgwOTFlMDEiLCJwaG9uZSI6ImlGenNjbHNSSW5IYWJtSEhuM2JoVGc9PSIsInVzZXJfcmVnaXN0cmF0aW9uX2R0IjoxNjc1MjA3MjY5LCJ2ZXJzaW9uIjoyfQ.WRVNYHJHJG0hCDwIjKd9uV470t0heNRnnueRen6yieUHgKpXJI4PkY6RvHcCnzDo2FMF7943kgAWNQvVzCkRn24Bhu-hVGNgu_cGNMRxTrTs8UdRcfL_m_dgzaOdeito6vHGJ1kTA-8iFYrhGhugfb0kFA1JvQ2XD1U6Kn8emWHkxLkEui_HHrk9RSQT6egq0KdRcjqHQIy9q4cTtJVwb7wXPPSOVqTT6qXP1Cm3nXuM7gLZWVJw3C2DiaAQz7ep_xjEPMVZLaZJ0xW_avrIb0Jns_vW80KNXk3zSwEDZ5kZcFygvPiz1r1I0dKHOme7Dkrs3WdPfOZttv7SNG24jA',
                'origin': 'https://www.wildberries.ru',
                'priority': 'u=1, i',
                'referer': f'https://www.wildberries.ru/catalog/{nm_id}/detail.aspx?targetUrl=SP',
                'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            }

            async with session.get(
                "https://user-grade.wildberries.ru/api/v5/grade",
                params=params,
                headers=headers,
            ) as resp:
                data = await resp.json()
                return data["payload"]["payments"][0]["full_discount"]
        except Exception:
            return "Нет в наличии"
    
    # надо переписать будет - иногда может некорректно работать из-за размера/цвета: неизвестно какой у артикула будет
    async def parse_other_data_card(
        self, session: aiohttp.ClientSession, nm_id: str
    ) -> int | str:
        try:
            params = {
                "appType": "1",
                "curr": "rub",
                "dest": "-446115",
                "spp": "30",
                "ab_testing": "false",
                "lang": "ru",
                "nm": nm_id,
            }
            async with session.get(
                "https://card.wb.ru/cards/v4/detail", params=params
            ) as resp:
                data = await resp.json()
                product = data["products"][0]
                remains = product["totalQuantity"]
                number_of_images = product["pics"]
                nm_feedbacks = product["nmFeedbacks"]
                nm_review_rating = product["nmReviewRating"]
                name = product["name"]

                try:
                    price = product["sizes"][0]["price"]["product"]
                except Exception as e:
                    price = "Нет в наличии"
                return {
                    "price": price,
                    "nmFeedbacks": nm_feedbacks,
                    "nmReviewRating": nm_review_rating,
                    "name": name,
                    "remains": remains,
                    "number_of_images": number_of_images
                }
        except Exception:
            return None


