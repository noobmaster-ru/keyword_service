import aiohttp
import math


class ParsePrice:
    def __init__(self):
        pass

    # надо переписать будет - иногда может некорректно работать из-за размера/цвета: неизвестно какой у артикула будет
    async def parse_card(
        self, session: aiohttp.ClientSession, nm_id: str, list_of_nm_ids: list
    ) -> int | str:
        try:
            nm = "".join([f"{item};" for item in list_of_nm_ids])
            params = {
                "appType": "1",
                "curr": "rub",
                "dest": "-446115",
                "spp": "30",
                "hide_dtype": "14",
                "ab_testing": "false",
                "lang": "ru",
                "nm": nm,
            }
            async with session.get(
                "https://card.wb.ru/cards/v4/detail", params=params
            ) as resp:
                data = await resp.json()
                products = data["products"]
                for product in products:
                    if int(product["id"]) == int(nm_id):
                        sizes = product["sizes"]
                        for size in sizes:
                            if "price" in size:
                                return size["price"]["product"]
                return "Error in parse_card"
                # return data["products"][0]["sizes"][0]["price"]["product"]
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

    async def fetch_price(
        self, session: aiohttp.ClientSession, nm_id: str, list_of_nm_ids: list
    ) -> dict:
        full_discount = await self.parse_grade(session, nm_id)
        price = await self.parse_card(session, nm_id, list_of_nm_ids)

        if isinstance(full_discount, int) and isinstance(price, int):
            wallet_price = math.floor((price / 100) * (1 - full_discount / 100))
            return wallet_price
        else:
            return "Нет в наличии"
