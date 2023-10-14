from aiogram import Bot, types, Dispatcher, executor

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nПришлите документ и я отвечу!")
    # регистрировать пришедших

@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def download_doc(message: types.Message):
    destination_dir=r"."
    # Скачивание в каталог с ботом с созданием подкаталогов по типу файла
    await message.document.download(destination_dir=destination_dir)
    await message.reply("Документ принят")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)