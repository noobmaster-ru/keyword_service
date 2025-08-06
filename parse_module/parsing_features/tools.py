class Tools:
    def __init__(self):
        pass

    def sort_key(self, item: dict):
        organic_pos = item[1]["organic_position"]
        return (organic_pos is None, organic_pos or 0)

    @staticmethod
    def build_basket_for_video(nm_id: int) -> str:
        vol_value = nm_id % 144
        if 0 <= vol_value <= 11:
            basket = "01"
        elif 12 <= vol_value <= 23:
            basket = "02"
        elif 24 <= vol_value <= 35:
            basket = "03"
        elif 36 <= vol_value <= 47:
            basket = "04"
        elif 48 <= vol_value <= 59:
            basket = "05"
        elif 60 <= vol_value <= 71:
            basket = "06"
        elif 72 <= vol_value <= 83:
            basket = "07"
        elif 84 <= vol_value <= 95:
            basket = "08"
        elif 96 <= vol_value <= 107:
            basket = "09"
        elif 108 <= vol_value <= 119:
            basket = "10"
        elif 120 <= vol_value <= 131:
            basket = "11"
        elif 132 <= vol_value <= 143:
            basket = "12"
        else:
            basket = "13"
        return basket, vol_value

    @staticmethod
    def build_basket(short_nm_id: int) -> str:
        # Определяем basket (сокращённый вариант через switch не работает!)
        if 0 <= short_nm_id <= 143:
            basket = "01"
        elif 144 <= short_nm_id <= 287:
            basket = "02"
        elif 288 <= short_nm_id <= 431:
            basket = "03"
        elif 432 <= short_nm_id <= 719:
            basket = "04"
        elif 720 <= short_nm_id <= 1007:
            basket = "05"
        elif 1008 <= short_nm_id <= 1061:
            basket = "06"
        elif 1062 <= short_nm_id <= 1115:
            basket = "07"
        elif 1116 <= short_nm_id <= 1169:
            basket = "08"
        elif 1170 <= short_nm_id <= 1313:
            basket = "09"
        elif 1314 <= short_nm_id <= 1601:
            basket = "10"
        elif 1602 <= short_nm_id <= 1655:
            basket = "11"
        elif 1656 <= short_nm_id <= 1919:
            basket = "12"
        elif 1920 <= short_nm_id <= 2045:
            basket = "13"
        elif 2046 <= short_nm_id <= 2189:
            basket = "14"
        elif 2190 <= short_nm_id <= 2405:
            basket = "15"
        # здесь вб добавил новые basket - пришло добавить (см в network:  banners.js -> Response)
        elif 2406 <= short_nm_id <= 2621:
            basket = "16"
        elif 2622 <= short_nm_id <= 2837:
            basket = "17"
        elif 2838 <= short_nm_id <= 3053:
            basket = "18"
        elif 3054 <= short_nm_id <= 3269:
            basket = "19"
        elif 3270 <= short_nm_id <= 3485:
            basket = "20"
        elif 3486 <= short_nm_id <= 3701:
            basket = "21"
        elif 3702 <= short_nm_id <= 3917:
            basket = "22"
        elif 3918 <= short_nm_id <= 4133:
            basket = "23"
        elif 4134 <= short_nm_id <= 4349:
            basket = "24"
        elif 4350 <= short_nm_id <= 4565:
            basket = "25"
        else:
            basket = "26"

        # если ошибка будет, то возможно вб новые basket добавил
        return basket
