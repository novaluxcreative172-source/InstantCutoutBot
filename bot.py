import os
import io
import logging

from rembg import remove
from PIL import Image
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 I'm InstantCutoutBot.\n\n"
        "Send me any photo (or an image as a file, for full quality) and "
        "I'll send it back with the background removed as a transparent PNG."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Just send a photo or image file. I'll strip the background and "
        "reply with a PNG that has transparency where the background was.\n\n"
        "Tip: send as a 'file' (not compressed photo) if you want the "
        "original resolution preserved."
    )


async def remove_bg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text("⏳ Removing background...")

    try:
        if update.message.photo:
            tg_file = await update.message.photo[-1].get_file()
        elif update.message.document and update.message.document.mime_type and \
                update.message.document.mime_type.startswith("image/"):
            tg_file = await update.message.document.get_file()
        else:
            await status_msg.edit_text("Please send a photo or an image file (jpg/png/webp).")
            return

        img_bytes = bytes(await tg_file.download_as_bytearray())
        input_image = Image.open(io.BytesIO(img_bytes)).convert("RGBA")

        output_image = remove(input_image)

        buffer = io.BytesIO()
        output_image.save(buffer, format="PNG")
        buffer.seek(0)
        buffer.name = "cutout.png"

        await update.message.reply_document(
            document=buffer,
            filename="cutout.png",
            caption="✅ Done — background removed.",
        )
        await status_msg.delete()

    except Exception as e:
        logger.exception("Failed to remove background")
        await status_msg.edit_text(f"❌ Something went wrong: {e}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, remove_bg))

    logger.info("InstantCutoutBot starting (polling mode)...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
