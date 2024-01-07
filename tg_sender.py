import loguru
from aiogram import Bot, Dispatcher, types
from loguru import logger

token = ''

bot = Bot(token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


async def make_post(header, content_text, image):
    logger.debug('make_post()')
    await bot.send_photo('@playfree_mailer', photo=image)
    await bot.send_message('@playfree_mailer', header + content_text, parse_mode='HTML')


async def make_post_img(header, content_text, image):
    await bot.send_photo('@playfree_mailer', photo=image, caption=header + content_text, parse_mode='HTML')


async def make_post_without_img(header, content_text):
    logger.debug('make_post_without_img()')
    await bot.send_message('@playfree_mailer', header + content_text, parse_mode='HTML')
