from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.start_kb import start_kb
from utils.logger import logger
from utils.set_bot_commands import cmds_list

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    logger.info(f'/start from {message.from_user.first_name} {message.from_user.last_name}')
    mes = (
        "Привет!\n"
        "Я бот для записи твоих тренировок и других активностей в КАиС МГТУ\n"
        "Вот команды для взаимодействия со мной:\n")
    for cmd in cmds_list:
        mes += f"/{cmd[0]} – {cmd[1]}\n"
    await message.answer(mes)
