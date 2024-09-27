from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.start_kb import start_kb

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Приветствую! Что желаете?', reply_markup=start_kb())