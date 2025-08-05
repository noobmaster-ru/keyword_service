import aiohttp
from parse_module.parsing_features.tools import Tools
from typing import Union


class ParseFiveLastFeedback:
    def __init__(self):
        pass

    @staticmethod
    def get_list_of_feedback_data(nm_id: str, feedbacks_list: list) -> list:
        summa_feedbacks_rating = 0
        count = 0
        text_of_feedback = ""
        rate_of_feedback = ""
        for index, feedback in enumerate(feedbacks_list):
            product_valuation = feedback["productValuation"]
            feedback_nm_id = feedback["nmId"]
            if int(feedback_nm_id) == int(nm_id) and count < 5:
                summa_feedbacks_rating += int(product_valuation)
                if text_of_feedback == "":
                    text_of_feedback = (
                        feedback.get("text")
                        or feedback.get("cons")
                        or feedback.get("pros")
                    )
                    rate_of_feedback = product_valuation
                count += 1
                if count > 4:
                    break
        return [summa_feedbacks_rating / 5, text_of_feedback, rate_of_feedback]

    async def parse_last_five_feedbacks_rating(
        self, session: aiohttp.ClientSession, nm_id: str
    ) -> Union[float, str]:
        try:
            int_nm_id = int(nm_id)
            short_nm_id = int_nm_id // 100000
            basket = Tools.build_basket(short_nm_id)
            headers = {
                "accept": "*/*",
                "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "cache-control": "no-cache",
                "origin": "https://www.wildberries.ru",
                "pragma": "no-cache",
                "priority": "u=1, i",
                "referer": f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx",
                "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            }
            async with session.get(
                f"https://basket-{basket}.wbbasket.ru/vol{str(int_nm_id // 100000)}/part{str(int_nm_id // 1000)}/{str(nm_id)}/info/ru/card.json",
                headers=headers,
            ) as response:
                data = await response.json()
                imt_id = data["imt_id"]
                try:
                    headers = {
                        "accept": "*/*",
                        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                        "origin": "https://www.wildberries.ru",
                        "priority": "u=1, i",
                        "referer": f"https://www.wildberries.ru/catalog/{str(nm_id)}/feedbacks?imtId={str(imt_id)}",
                        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                        "sec-ch-ua-mobile": "?0",
                        "sec-ch-ua-platform": '"macOS"',
                        "sec-fetch-dest": "empty",
                        "sec-fetch-mode": "cors",
                        "sec-fetch-site": "cross-site",
                        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
                    }

                    async with session.get(
                        f"https://feedbacks1.wb.ru/feedbacks/v2/{imt_id}",
                        headers=headers,
                    ) as resp:
                        data = await resp.json()
                        feedbacks_list = data["feedbacks"]
                        return self.get_list_of_feedback_data(nm_id, feedbacks_list)
                except Exception:
                    headers = {
                        "accept": "*/*",
                        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                        "origin": "https://www.wildberries.ru",
                        "priority": "u=1, i",
                        "referer": f"https://www.wildberries.ru/catalog/{nm_id}/detail.aspx",
                        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                        "sec-ch-ua-mobile": "?0",
                        "sec-ch-ua-platform": '"macOS"',
                        "sec-fetch-dest": "empty",
                        "sec-fetch-mode": "cors",
                        "sec-fetch-site": "cross-site",
                        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
                    }
                    async with session.get(
                        f"https://feedbacks2.wb.ru/feedbacks/v2/{imt_id}",
                        headers=headers,
                    ) as resp:
                        data = await resp.json()
                        feedbacks_list = data["feedbacks"]
                        return self.get_list_of_feedback_data(nm_id, feedbacks_list)
        except Exception as e:
            print("Error in parse_last_five_feedbacks_rating", str(e))
