import logging

from telegram.ext import Updater, MessageHandler, Filters

from FridgeBot.Bot.callbacks import Callbacks

BOT_TOKEN = "1484702411:AAHvOA7AI1_L8ZBHkPLGkfbbpHHeipnVnEw"

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def echo(update, context):
    """
    Echo the user message.
    """
    update.message.reply_text(update.message.text)


def error(update, context):
    """
    Log Errors caused by Updates.
    """
    logging.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """
    Start the bot.
    """
    updater = Updater(BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    Callbacks.initialize_handlers(dispatcher=dispatcher)

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
