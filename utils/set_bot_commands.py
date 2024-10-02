from aiogram.types import BotCommand, BotCommandScopeDefault

cmds_list = [
        ['start', 'Старт'],
        ['cardio', 'Добавить кардио тренировку'],
        ['climb', 'Добавить лазательную тренировку']
]

async def set_default_commands(bot): 
    bot_cmds = []
    for i in range(0, len(cmds_list)):
        bot_cmds.append(BotCommand(command=cmds_list[i][0], description=cmds_list[i][1]))

    await bot.set_my_commands(bot_cmds, BotCommandScopeDefault())

