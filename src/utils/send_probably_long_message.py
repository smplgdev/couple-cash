import asyncio
import logging

from aiogram.exceptions import AiogramError

logger = logging.getLogger(__name__)


def split_string(input_string: str, max_length: int = 4096):
    parts = input_string.split('\n')
    result = []
    current_chunk = ''

    for part in parts:
        if len(current_chunk) + len(part) + (1 if current_chunk else 0) > max_length:
            if current_chunk:
                result.append(current_chunk)
            current_chunk = part
        else:
            if current_chunk:
                current_chunk += '\n'
            current_chunk += part

    if current_chunk:
        result.append(current_chunk)

    return result


async def send_probably_long_message(bot, chat_id, text, **kwargs) -> bool:
    # Now supports only text messages
    if len(text) < 4096:
        try:
            await bot.send_message(chat_id, text)
        except AiogramError as e:
            logger.error(e)
            return False
    else:
        for text_chunk in split_string(text):
            try:
                await bot.send_message(chat_id, text_chunk, **kwargs)
            except AiogramError as e:
                logger.error(e)
                return False
            await asyncio.sleep(0.1)
