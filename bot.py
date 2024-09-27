import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.register_routers import register_routers
from utils.set_bot_commands import set_default_commands

# Инициализация бота и диспетчера
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print('You have forgot to set BOT_TOKEN')
    quit()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Регистрация хендлеров
register_routers(dp)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print('Bot started!')
    await dp.start_polling(bot)  # Стартуем лонг-поллинг
    await set_default_commands(bot)

if __name__ == '__main__':
    asyncio.run(main())  # Запускаем асинхронно

