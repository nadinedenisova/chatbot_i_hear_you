from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from core.settings import settings


class TelegramBot:
    def __init__(self, token: str):
        self.bot = Bot(
            token=token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
        )

    async def send_message(self, user_id: int, text: str):
        await self.bot.send_message(user_id, text)


def get_telegram_bot():
    return TelegramBot(token=settings.bot_token)
