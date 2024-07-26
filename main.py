from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import re
import logging
import os
from collections import defaultdict

# Replace with your actual bot token
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Admin and user IDs (replace with actual admin IDs)
ADMIN_IDS = [123456789]  # Replace with actual admin IDs

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define regex patterns for spam and NSFW content
NSFW_PATTERNS = [r'\b(nsfw|porn|adult|sex|xxx)\b']  # Add more patterns as needed
SPAM_KEYWORDS = [r'\b(sale|free|win|money|prize)\b']  # Add more patterns as needed

# Anti-spam settings
MESSAGE_LIMIT = 5
TIME_WINDOW = 60
user_message_count = defaultdict(list)
spam_warnings = defaultdict(int)

# Admin Commands

def pin(update: Update, context: CallbackContext):
    if update.message.from_user.id in ADMIN_IDS:
        if update.message.chat.type in ['group', 'supergroup']:
            if context.args:
                message_id = int(context.args[0])
                try:
                    context.bot.pin_chat_message(chat_id=update.message.chat_id, message_id=message_id)
                    update.message.reply_text(f'📌 Message {message_id} has been pinned. 📌')
                except Exception as e:
                    update.message.reply_text(f'❌ Failed to pin message: {e} ❌')
                    logger.error(f'Failed to pin message {message_id}: {e}')
            else:
                update.message.reply_text('❓ Please provide a message ID to pin. ❓')
        else:
            update.message.reply_text('🚫 This command can only be used in groups. 🚫')
    else:
        update.message.reply_text('🚫 You are not authorized to use this command. 🚫')

def unpin(update: Update, context: CallbackContext):
    if update.message.from_user.id in ADMIN_IDS:
        if update.message.chat.type in ['group', 'supergroup']:
            if context.args:
                message_id = int(context.args[0])
                try:
                    context.bot.unpin_chat_message(chat_id=update.message.chat_id, message_id=message_id)
                    update.message.reply_text(f'📍 Message {message_id} has been unpinned. 📍')
                except Exception as e:
                    update.message.reply_text(f'❌ Failed to unpin message: {e} ❌')
                    logger.error(f'Failed to unpin message {message_id}: {e}')
            else:
                update.message.reply_text('❓ Please provide a message ID to unpin. ❓')
        else:
            update.message.reply_text('🚫 This command can only be used in groups. 🚫')
    else:
        update.message.reply_text('🚫 You are not authorized to use this command. 🚫')

def group_status(update: Update, context: CallbackContext):
    if update.message.from_user.id in ADMIN_IDS:
        chat = update.message.chat
        admins = [member.user.full_name for member in context.bot.get_chat_administrators(chat_id=chat.id)]
        pinned_message = chat.pinned_message.text if chat.pinned_message else 'No pinned message'
        
        status_text = (
            f"📊 *Group Status* 📊\n"
            f"🏷 *Name:* {chat.title}\n"
            f"🆔 *ID:* {chat.id}\n"
            f"📝 *Description:* {chat.description if chat.description else 'No description'}\n"
            f"👥 *Members:* {context.bot.get_chat_members_count(chat_id=chat.id)}\n"
            f"👮 *Admins:* {', '.join(admins)}\n"
            f"📌 *Pinned Message:* {pinned_message}"
        )
        
        update.message.reply_text(status_text, parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text('🚫 You are not authorized to use this command. 🚫')

def start(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton("📊 Group Status", callback_data='feature_group_status')],
        [InlineKeyboardButton("⏰ Set Daily Reminder", callback_data='feature_set_daily_reminder')]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text('🎉 Hello! I am your advanced group management bot. 🎉\nChoose an option:', reply_markup=reply_markup)

def ping(update: Update, context: CallbackContext):
    update.message.reply_text('🔄 Pong! 🔄')

def help_command(update: Update, context: CallbackContext):
    help_text = (
        '📝 *Available Commands:*\n'
        '/ping - Check bot responsiveness\n'
        '/help - Get this help message\n'
        '/userinfo - Get user information\n'
    )
    update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

def user_info(update: Update, context: CallbackContext):
    user = update.message.from_user
    chat = update.message.chat
    user_info_text = (
        f"👤 *User Info* 👤\n"
        f"🏷 *Name:* {user.full_name}\n"
        f"🆔 *ID:* {user.id}\n"
        f"💬 *Username:* {user.username if user.username else 'N/A'}\n"
        f"🗣 *Chat:* {chat.title}\n"
    )
    update.message.reply_text(user_info_text, parse_mode=ParseMode.MARKDOWN)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('ping', ping))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('userinfo', user_info))
    
    dispatcher.add_handler(CommandHandler('pin', pin))
    dispatcher.add_handler(CommandHandler('unpin', unpin))
    dispatcher.add_handler(CommandHandler('groupstatus', group_status))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
  
