import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import easyocr
import io
import numpy as np
from PIL import Image

# Токен бота
API_TOKEN = 'ВАШ ТОКЕН'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Установка уровня логгирования
logging.basicConfig(level=logging.INFO)

# Инициализация EasyOCR
reader = easyocr.Reader(['en', 'ru'])

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    await message.answer("Привет! Отправьте мне изображение, на котором нужно найти текст.")

# Обработчик изображений
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def process_photo(message: types.Message):
    try:
        # Загрузка фотографии
        file_id = message.photo[-1].file_id
        file = await bot.download_file_by_id(file_id)
        file_bytes = file.read()
        photo = io.BytesIO(file_bytes)
        img = Image.open(photo)

        # Распознавание текста
        result = reader.readtext(np.array(img))

        # Подготовка ответа
        recognized_text = '\n'.join([entry[1] for entry in result])

        if recognized_text:
            await message.answer(f"Распознанный текст на изображении:\n{recognized_text}", parse_mode=ParseMode.MARKDOWN)
        else:
            await message.answer("Текст не найден на изображении.")
    except Exception as e:
        # Логирование ошибки
        logging.error(f"Error during text recognition: {str(e)}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
