from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_default_commands(bot): 
    commands = [
                BotCommand(command='start', description='Старт'),
                BotCommand(command='help', description='Вывести справку')
                # BotCommand(command='cardio', description='Добавить кардио тренировку')
                ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

