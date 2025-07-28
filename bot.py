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
from aiogram.types import InputMediaPhoto,  FSInputFile
from aiogram.utils.chat_action import ChatActionSender

# from app.parse_module.main import parse_main
# from parse_module.service.parse_photo_by_nm_id import parse_photos
from parse_module.main import main as parse_main

async def send_photos(bot: Bot, chat_id: int, offset: int = 0, limit: int = 10):
    """
    Отправка группы фотографий из папки images/
    :param offset: начальный индекс
    :param limit: максимальное количество фото (не более 10)
    """
    image_folder = ".data/images"
    
    # Получаем список файлов с поддержкой сортировки
    image_files = sorted([
        f for f in os.listdir(image_folder) 
        if f.lower().endswith(('.webp')) # '.jpg', '.jpeg', '.png', 
    ])[offset:offset+limit]

    if not image_files:
        await bot.send_message(chat_id, "🖼 В папке нет изображений!")
        return

    async with ChatActionSender.upload_photo(chat_id=chat_id, bot=bot):
        media_group = []
        
        for i, filename in enumerate(image_files):
            file_path = os.path.join(image_folder, filename)
            
            # Используем FSInputFile для локальных файлов
            photo = FSInputFile(file_path)
            
            # Добавляем подпись только к первому изображению
            if i == 0:
                media_group.append(
                    InputMediaPhoto(
                        media=photo,
                        caption=f"📸 Первые фото артикулов {offset+1}-{offset+len(image_files)} из {len(os.listdir(image_folder))}"
                    )
                )
            else:
                media_group.append(InputMediaPhoto(media=photo))

        try:
            await bot.send_media_group(chat_id=chat_id, media=media_group)
        except Exception as e:
            await bot.send_message(
                chat_id,
                f"❌ Ошибка при отправке фото: {str(e)}"
            )

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

        try:
            start = time.time()
            result = await parse_main(keyword=keyword, NUMBER_OF_PARSING=NUMBER_OF_PARSING)
            exec_time = time.time() - start
            print("parse_main exec_time parse_main = ", exec_time)
        

            reply = "\u2705 Топ-20 товаров по запросу:\n"
            for nm_id, data in result.items():
                resp = f'<a href="{data["link"]}">{data["name"]}</a>'
                reply += (
                    f"\n{resp}\n"
                    f"{data['price']}₽ (СПП = 30%)\n"
                    f"{data['nmReviewRating']} ({data['nmFeedbacks']} отзывов) \n"
                    f"Органическая позиция: {data['organic_position']}\n"
                    f"Промо позиция: {data['promo_position']}\n"
                    f"Страница в поиске: {data['page']}\n"
                    f"Остатки: {data['remains']}\n"
                )
            reply += f"\nВремя обработки: {exec_time:.2f} сек\n"
           
            await message.answer(reply, parse_mode="HTML")
            print(f"выдал ответ пользователю {chat_id}, {keyword}\n")
            await message.answer("Обрабатываю фотографии")
            
            # list_of_nm_ids_and_number_of_images = []
            # for nm_id, data in result.items():
            #     list_of_nm_ids_and_number_of_images.append([nm_id, data["number_of_images"]])

            # list_of_nm_id = [item for item in result]
            # await parse_photos(list_of_nm_id)
            
            # await send_photos(bot, chat_id, 0, 10)
            # await send_photos(bot, chat_id, 10, 20)
        except Exception:
            await message.answer("\u274c Произошла ошибка при обработке запроса.")
            logging.exception("Ошибка при обработке запроса")

    await dp.start_polling(bot)


if __name__ == "__main__":
    load_dotenv()
    BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
    NUMBER_OF_PARSING = int(os.getenv("NUMBER_OF_PARSING"))
    shutil.rmtree(".data/images")
    os.makedirs(".data/images/", exist_ok=True)

    asyncio.run(main(BOT_TOKEN, NUMBER_OF_PARSING))
