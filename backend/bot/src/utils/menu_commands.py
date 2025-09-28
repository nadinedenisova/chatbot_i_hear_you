from aiogram.types import BotCommand

from utils.texts import TEXTS


async def set_main_commands(bot):
    """Устанавливает команды бота, которые будут видны в меню Telegram."""

    main_menu_commands = [
        BotCommand(command='/start',
                   description=TEXTS['start_command']),
        BotCommand(command='/help',
                   description=TEXTS['help_command']),
    ]

    await bot.set_my_commands(main_menu_commands)
