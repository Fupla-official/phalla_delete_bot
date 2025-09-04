import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import datetime

# --- Configuration ---
TOKEN = "8485363687:AAGS83mef3QgQysm57bCeyaIHo4RCo1eO0Y"  # Make sure your real token is here


# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! I can now delete links and join/leave messages in groups."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message when the command /help is issued."""
    await update.message.reply_text(
        "Commands: /start, /help, /time. I also auto-delete links and service messages in groups if I am an admin.")


async def time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the current date and time."""
    now = datetime.datetime.now()
    formatted_time = now.strftime("%A, %d %B %Y, %I:%M %p")
    await update.message.reply_text(f"The current time is:\n{formatted_time}")


# --- Special Action Handlers ---

async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Deletes messages that contain a URL."""
    message = update.message
    print(f"Link detected from {message.from_user.username}. Deleting message...")
    await message.delete()


# --- NEW FUNCTION ---
async def delete_service_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Deletes new chat member and left chat member messages."""
    print("Join/Leave service message detected. Deleting...")
    await update.message.delete()


# --- Message Handlers ---

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


# --- Main Bot Logic ---
def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("time", time))

    # Register special action handlers
    application.add_handler(MessageHandler(filters.Entity("url"), delete_links))

    # --- ADD THIS NEW HANDLER ---
    application.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS | filters.StatusUpdate.LEFT_CHAT_MEMBER,
                       delete_service_messages))

    # Register message handler for echoing (this should be last)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot
    print("Bot is running... Press Ctrl-C to stop.")
    application.run_polling()


if __name__ == "__main__":

    main()
