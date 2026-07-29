import logging
import json
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Load mood data
with open("mood_data.json", "r") as f:
    MOOD_DATA = json.load(f)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_text = (
        f"Hey {user.first_name}! 👋\n\n"
        "I'm **BallHk88BOT** – your daily mood booster!\n"
        "Type /vibe to take a quick emoji quiz and get a motivational quote tailored to your mood.\n"
        "Type /help to see all commands."
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "📌 **Available Commands:**\n"
        "/start - Welcome message\n"
        "/vibe - Start the mood quiz\n"
        "/help - Show this menu\n"
        "/about - Learn about this bot\n\n"
        "Just type /vibe and pick an emoji – I'll do the rest!"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# /about command
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    about_text = (
        "🌟 **About BallHk88BOT**\n\n"
        "I'm a simple bot created to spread positivity.\n"
        "I don't store personal data, I don't spam, and I don't sell anything.\n"
        "Just good vibes, one emoji at a time.\n\n"
        "Made with ☕ and care."
    )
    await update.message.reply_text(about_text, parse_mode="Markdown")

# /vibe command – sends an inline keyboard with emojis
async def vibe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("😊 Happy", callback_data="😊")],
        [InlineKeyboardButton("😢 Sad", callback_data="😢")],
        [InlineKeyboardButton("😡 Angry", callback_data="😡")],
        [InlineKeyboardButton("😴 Tired", callback_data="😴")],
        [InlineKeyboardButton("🤔 Confused", callback_data="🤔")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("How are you feeling right now? Pick an emoji:", reply_markup=reply_markup)

# Handle the callback from the inline keyboard
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    emoji = query.data
    mood_info = MOOD_DATA.get(emoji)

    if mood_info:
        mood = mood_info["mood"]
        quote = mood_info["quote"]
        response = (
            f"You picked {emoji} – that means you're feeling **{mood}**.\n\n"
            f"💬 Here's your quote:\n*\"{quote}\"*\n\n"
            "Remember: This too shall pass. Keep going!"
        )
    else:
        response = "Oops! I don't recognize that emoji. Try /vibe again."

    await query.edit_message_text(response, parse_mode="Markdown")

# Main function
def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("vibe", vibe))
    app.add_handler(CallbackQueryHandler(button_callback))

    # Start the bot (polling)
    app.run_polling()
    logger.info("Bot is running...")

if __name__ == "__main__":
    main()
