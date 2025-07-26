import os
import asyncio
import logging
import time
from dotenv import load_dotenv
from itertools import islice
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart

from parse_module import main as parse_main


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(message: Message):
        await message.answer(
            "Привет! Отправь мне поисковый запрос и я верну топ-5 товаров с Wildberries по органическим позициям."
        )

    @dp.message(F.text)
    async def handle_query(message: types.Message):
        query = message.text.strip()
        print("receive message:", query)

        await message.answer(
            f"🔍 Получена ключевая фраза: <b>{query}</b>\nПожалуйста, подождите, идёт обработка...\n",
            parse_mode="HTML",
        )

        try:
            start = time.time()
            result = await parse_main(query)
            exec_time = time.time() - start
            print("exec_time parse_main = ", exec_time)
            first_five = dict(islice(result.items(), 5))

            reply = "\u2705 Топ-5 товаров по запросу:\n"
            for nm_id, data in first_five.items():
                url = data["link"]
                text = data["name"]
                resp = f'<a href="{url}">{text}</a>'
                reply += (
                    f"\n{resp}\n"
                    f"{data['price']}₽ (СПП = 30%)\n"
                    f"{data['nmReviewRating']} ({data['nmFeedbacks']} отзывов) \n"
                    f"Органическая позиция: {data['organic_position']}\n"
                    f"Промо позиция: {data['promo_position']}\n"
                    f"Страница в поиске: {data['page']}\n"
                )
            reply += f"\nВремя обработки: {exec_time:.2f} сек\n"
            await message.answer(reply, parse_mode="HTML")
        except Exception:
            await message.answer("\u274c Произошла ошибка при обработке запроса.")
            logging.exception("Ошибка при обработке запроса")

    await dp.start_polling(bot)


if __name__ == "__main__":
    load_dotenv()
    BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
    asyncio.run(main())
