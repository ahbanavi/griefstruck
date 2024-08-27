import logging
import os
import re

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename=".log",
)


async def replace_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.channel_post.caption
    if not message_text:
        logging.warning("No caption found in the message")
        return

    # if message name contains @motreb_downloader_bot, replace it with username
    if "@motreb_downloader_bot" in message_text:
        message_text = message_text.replace("@motreb_downloader_bot", "🆔 @" + update.effective_chat.username)

        # if start of a line starts with #ar_, add 🧑‍🎤 emoji before it
        message_text = re.sub(r"(^|\n)#ar_", r"\1🧑‍🎤 #ar_", message_text)
        # #tr_ to 🎵
        message_text = re.sub(r"(^|\n)#tr_", r"\1🎵 #tr_", message_text)
        # #al_ to 📀
        message_text = re.sub(r"(^|\n)#al_", r"\1📀 #al_", message_text)
        # remove the line that starts with #pl_
        message_text = re.sub(r"(^|\n)#pl_.*\n", "\n", message_text)
    else:
        # just replace everything with id
        message_text = "🆔 @" + update.effective_chat.username

    await context.bot.edit_message_caption(
        chat_id=update.effective_chat.id,
        message_id=update.channel_post.message_id,
        caption=message_text,
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TG_BOT_TOKEN")).build()
    caption_handler = MessageHandler(
        filters.AUDIO & filters.ChatType.CHANNEL & (~filters.COMMAND), replace_caption
    )

    application.add_handler(caption_handler)

    application.run_webhook(
        listen=os.getenv("WEBHOOK_HOST", "127.0.0.1"),
        port=os.getenv("WEBHOOK_PORT", 80),
        webhook_url=os.getenv("WEBHOOK_URL"),
        secret_token=os.getenv("WEBHOOK_SECRET_TOKEN", None),
        allowed_updates=["channel_post"],
    )
