import datetime
import os
import sys
from abc import ABC

from loguru import logger
from notifiers.logging import NotificationHandler

from data.config import TG_TOKEN, TG_ID, SEND_NOTIFICATIONS


class Logger(ABC):
    def __init__(self) -> None:
        self.logger = logger
        self.logger.remove()
        
        logger_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "  # Зеленый цвет для времени
            "<level><bold>{level: <8}</bold></level> | "   # Жирный текст уровня лога
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "  # Имя модуля, функция и строка
            "<level>{message}</level>"  # Сообщение с уровнем
        )
        self.logger.add(sys.stdout, format=logger_format)
        date = datetime.datetime.now(datetime.UTC).date()
        self.logger.add(
            f"./logs/{date}.log",
            rotation="100 MB",
            level="DEBUG",
            format=logger_format,
        )

        if SEND_NOTIFICATIONS:
            tg_handler = NotificationHandler(
                "telegram", defaults={"token": TG_TOKEN, "chat_id": TG_ID}
            )
            self.logger.add(tg_handler, level="SUCCESS", format=logger_format)

    def __getattr__(self, name):
        return getattr(self.logger, name)


logger = Logger()
