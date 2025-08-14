import os
import shutil
import asyncio
import logging
import time
from dotenv import load_dotenv
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
from parse_module.main import main as parse_main

from aiogram.types import FSInputFile


async def main(BOT_TOKEN, NUMBER_OF_PARSING):
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(message: Message):
        await message.answer(
            "Привет! Отправь мне поисковый запрос и я верну топ-5 товаров с Wildberries по органическим позициям."
        )

    @dp.message(F.text)
    async def handle_query(message: types.Message):
        keyword = message.text.strip()
        chat_id = message.chat.id
        print("\nreceive message:", keyword)

        await message.answer(
            f"🔍 Получена ключевая фраза: <b>{keyword}</b>\nПожалуйста, подождите, идёт обработка...\n",
            parse_mode="HTML",
        )
        # очищаем данные по прошлому запросу
        if os.path.exists(".data"):
            shutil.rmtree(".data")
        os.makedirs(".data", exist_ok=True)
        try:
            start = time.time()
            result = await parse_main(
                keyword=keyword, NUMBER_OF_PARSING=NUMBER_OF_PARSING
            )
            exec_time = time.time() - start
            print("parse_main exec_time parse_main = ", exec_time)

            reply = (
                f"\u2705 Топ-{NUMBER_OF_PARSING} товаров по запросу: <b>{keyword}</b>\n"
            )
            await message.answer(reply, parse_mode="HTML")
            reply = ""
            for nm_id, data in result.items():
                resp = f'<a href="{data["link"]}">{data["name"]}</a>'
                reply += (
                    f"\n{resp}\n"
                    f"{data['price']}₽ (СПП = 30%)\n"
                    f"{data['nmReviewRating']} ({data['nmFeedbacks']} отзывов) \n"
                    f"Рейтинг последних 5 отзывов: {data['five_last_feedbacks_rating']} \n"
                    f"Органическая позиция: {data['organic_position']}\n"
                    f"Промо позиция: {data['promo_position']}\n"
                    f"Страница в поиске: {data['page']}\n"
                    f"Остатки: {data['remains']}\n"
                    f"Cсылка на фото(на первое): {data['link_to_photos'].split(';')[0]}\n"
                    f"\nОписание: {data['description'][:100]}...\n"
                    f"\nТекст последнего отзыва (Оценка {data['rate_of_last_feedback']}): {data['text_of_last_feedback'][:100]}...\n"
                )

                sent_message = await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=data["link_to_photos"].split(";")[0],
                    caption=reply,
                    parse_mode="HTML",
                )
                video = FSInputFile(f".data/video_{nm_id}.mp4")

                if data["link_to_video"] != "":
                    await message.answer_video(
                        video=video,
                        caption="Дарю❤️",
                        reply_to_message_id=sent_message.message_id,
                    )
                reply = ""
            reply = f"\nВремя обработки: {exec_time:.2f} сек\n"

            await message.answer(reply, parse_mode="HTML")
            print(f"выдал ответ пользователю {chat_id}, {keyword}\n")

        except Exception:
            await message.answer("\u274c Произошла ошибка при обработке запроса.")
            logging.exception("Ошибка при обработке запроса")

    await dp.start_polling(bot)


if __name__ == "__main__":
    load_dotenv()
    BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
    NUMBER_OF_PARSING = int(os.getenv("NUMBER_OF_PARSING"))
    print("bot launched!")

    asyncio.run(main(BOT_TOKEN, NUMBER_OF_PARSING))
