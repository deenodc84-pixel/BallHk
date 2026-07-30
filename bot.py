import logging
import json
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Load token from config
try:
    from config import BOT_TOKEN
except ImportError:
    print("ERROR: config.py not found! Create it with BOT_TOKEN")
    sys.exit(1)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load mood data
try:
    with open("mood_data.json", "r") as f:
        MOOD_DATA = json.load(f)
    logger.info("Mood data loaded successfully")
except FileNotFoundError:
    logger.error("mood_data.json not found!")
    MOOD_DATA = {}
except json.JSONDecodeError:
    logger.error("Invalid JSON in mood_data.json!")
    MOOD_DATA = {}

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

# /vibe command
async def vibe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("😊 Happy", callback_data="happy")],
        [InlineKeyboardButton("😢 Sad", callback_data="sad")],
        [InlineKeyboardButton("😡 Angry", callback_data="angry")],
        [InlineKeyboardButton("😴 Tired", callback_data="tired")],
        [InlineKeyboardButton("🤔 Confused", callback_data="confused")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "How are you feeling right now? Pick an emoji:", 
        reply_markup=reply_markup
    )

# Handle callback
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    mood_map = {
        "happy": "😊",
        "sad": "😢",
        "angry": "😡",
        "tired": "😴",
        "confused": "🤔"
    }
    
    emoji = mood_map.get(query.data, "😊")
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
        response = "Oops! I don't recognize that mood. Try /vibe again."

    await query.edit_message_text(response, parse_mode="Markdown")

# Main function
def main() -> None:
    try:
        logger.info("Starting BallHk88BOT...")
        application = Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("about", about_command))
        application.add_handler(CommandHandler("vibe", vibe))
        application.add_handler(CallbackQueryHandler(button_callback))
        logger.info("Bot is running and polling...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
