import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler

from core import config
from database.connection import initialize_database
from tg import handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def run():
    application = ApplicationBuilder().token(config.API_TOKEN).build()
    application.add_handler(CommandHandler('start', handlers.start_poll))
    application.add_handler(CallbackQueryHandler(handlers.button_poll))
    application.add_handler(CommandHandler('help', handlers.help))
    application.add_handler(CommandHandler('questions', handlers.show_questions))
    application.add_handler(CommandHandler('answers', handlers.show_answers))
    from telegram.ext import filters
    application.add_handler(MessageHandler(filters.TEXT, handlers.hello))
    application.run_polling()

if __name__ == '__main__':
    initialize_database()
    run()
