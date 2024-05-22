import logging
import os
import re

from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename=".log",
)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.channel_post.caption
    if not message_text:
        logging.warning("No caption found in the message")
        return

    # if message name contains @motreb_downloader_bot, replace it with 'grief_stuck'
    message_text = message_text.replace("@motreb_downloader_bot", "🆔 @grief_struck")

    # if start of a line starts with #ar_, add 🧑‍🎤 emoji before it
    message_text = re.sub(r"(^|\n)#ar_", r"\1🧑‍🎤 #ar_", message_text)
    # #tr_ to 🎵
    message_text = re.sub(r"(^|\n)#tr_", r"\1🎵 #tr_", message_text)
    # #al_ to 📀
    message_text = re.sub(r"(^|\n)#al_", r"\1📀 #al_", message_text)
    # remove the line that starts with #pl_
    message_text = re.sub(r"(^|\n)#pl_.*\n", "\n", message_text)

    await context.bot.edit_message_caption(
        chat_id=update.effective_chat.id,
        message_id=update.channel_post.message_id,
        caption=message_text,
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TG_BOT_TOKEN")).build()
    echo_handler = MessageHandler(
        filters.AUDIO & filters.ChatType.CHANNEL & (~filters.COMMAND), echo
    )

    application.add_handler(echo_handler)

    application.run_polling()
