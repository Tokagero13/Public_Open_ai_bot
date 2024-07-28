import os
from typing import Final
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()
# Telegram Token and botname
TOKEN: Final = os.getenv("TELEGRAM_TOKEN")
BOT_USERNAME: Final = os.getenv('TELEGRAM_BOT_USERNAME')
INSTRUCTIONS: Final = os.getenv("INSTRUCTIONS")

# Define states for the conversation
FIRST_NAME, LAST_NAME, ADDRESS, PICKUP_TIME, PACKAGING_CHOICE, NOTE, DELIVERY_TIME = range(7)

# Define a dictionary to store user data
user_data = {}

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Please enter your first name:")
    return FIRST_NAME

def get_first_name(update: Update, context: CallbackContext) -> int:
    user_data['first_name'] = update.message.text
    update.message.reply_text("Please enter your last name:")
    return LAST_NAME

def get_last_name(update: Update, context: CallbackContext) -> int:
    user_data['last_name'] = update.message.text
    update.message.reply_text("Please enter your address:")
    return ADDRESS

def get_address(update: Update, context: CallbackContext) -> int:
    user_data['address'] = update.message.text
    update.message.reply_text("Please enter your pickup time:")
    return PICKUP_TIME

def get_pickup_time(update: Update, context: CallbackContext) -> int:
    user_data['pickup_time'] = update.message.text
    update.message.reply_text("Please enter your packaging choice:")
    return PACKAGING_CHOICE

def get_packaging_choice(update: Update, context: CallbackContext) -> int:
    user_data['packaging_choice'] = update.message.text
    update.message.reply_text("Please enter any additional notes:")
    return NOTE

def get_note(update: Update, context: CallbackContext) -> int:
    user_data['note'] = update.message.text
    update.message.reply_text("Please enter your delivery time:")
    return DELIVERY_TIME

def get_delivery_time(update: Update, context: CallbackContext) -> int:
    user_data['delivery_time'] = update.message.text
    update.message.reply_text("Thank you! Here is the information you provided:")
    for key, value in user_data.items():
        update.message.reply_text(f"{key}: {value}")
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Operation canceled.")
    return ConversationHandler.END

def main() -> None:
    updater = Updater.update_queue("TOKEN")
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST_NAME: [MessageHandler(filters.text & ~filters.command, get_first_name)],
            LAST_NAME: [MessageHandler(filters.text & ~filters.command, get_last_name)],
            ADDRESS: [MessageHandler(filters.text & ~filters.command, get_address)],
            PICKUP_TIME: [MessageHandler(filters.text & ~filters.command, get_pickup_time)],
            PACKAGING_CHOICE: [MessageHandler(filters.text & ~filters.command, get_packaging_choice)],
            NOTE: [MessageHandler(filters.text & ~filters.command, get_note)],
            DELIVERY_TIME: [MessageHandler(filters.text & ~filters.command, get_delivery_time)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
