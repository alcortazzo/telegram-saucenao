# Made by @alcortazzo
# v0.5

import os
import time
import config
import logging
from telebot import TeleBot, types

from telegram_saucenao import media_processing
from telegram_saucenao import api_requests


bot = TeleBot(config.tgBotToken)


@bot.message_handler(commands=["start"])
def cmd_start(message):
    def send_messages():
        bot.send_message(
            message.chat.id,
            'This <a href="https://github.com/alcortazzo/telegram-saucenao"><b>open source</b></a> '
            'bot provides you with an interface to use <a href="https://saucenao.com/"><b>SauceNAO</b></a>`s '
            "reverse image search engine. \n\n<b>author: @alcortazzo</b>\n"
            '<b>donate <a href="https://telegra.ph/Donate-07-22-2">here</a></b>',
            parse_mode="HTML",
            disable_web_page_preview=True,
        )

    send_messages()


@bot.message_handler(content_types=["photo"])
def msg_media(message):
    def send_results(result):
        text_result = (
            f"<b>{result['name']}</b>\n\n"
            f"<b>Part:</b> {result['part']}\n"
            f"<b>Year:</b> {result['year']}\n"
            f"<b>Time:</b> {result['time']}\n"
        )

        markup = types.InlineKeyboardMarkup()
        buttons = []
        for url in result["urls"]:
            buttons.append(
                types.InlineKeyboardButton(text=f"{url[1]} - {url[2]}%", url=url[0])
            )
        markup.add(buttons[0])
        markup.row(buttons[1], buttons[2])

        bot.send_message(
            message.chat.id,
            text_result,
            parse_mode="HTML",
            reply_markup=markup,
            reply_to_message_id=message.id,
        )

    bot.send_chat_action(message.chat.id, "typing")

    file_name = str(int(time.time()))
    media_file = media_processing.MediaFile(bot, message, file_name)
    media_file.download_media()
    file = media_file.prepare_file()
    results = api_requests.ApiRequest(message.chat.id, file_name)
    results = results.get_result(file)
    send_results(results)
    delete_media(message.chat.id, file_name)


def delete_media(chat_id, filename):
    try:
        folders = os.listdir(f"./media/")
        files = []
        if str(chat_id) in folders:
            files = os.listdir(f"./media/{chat_id}/")
            if f"{filename}.jpg" in files:
                os.remove(f"./media/{chat_id}/{filename}.jpg")
    except Exception as ex:
        text = f"[{type(ex).__name__}] in delete_media(): {str(ex)}"
        logger.error(text)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler("dev.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as ex:
            text = f"[{type(ex).__name__}] in bot.polling(): {str(ex)}"
            logger.error(text)
            if type(ex).__name__ == "ConnectionError":
                time.sleep(3)
