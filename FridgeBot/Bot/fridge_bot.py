import logging
import threading

from telegram.ext import Updater

from FridgeBot.Bot.callbacks import Callbacks
from FridgeBot.Bot.task_executor import execute_forever

BOT_TOKEN = "1484702411:AAHvOA7AI1_L8ZBHkPLGkfbbpHHeipnVnEw"

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO,
                    handlers=[logging.FileHandler("/tmp/fridgelog"), logging.StreamHandler()])


def main():
    """
    Start the bot.
    """
    updater = Updater(BOT_TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    Callbacks.initialize_handlers(dispatcher=dispatcher)

    threading.Thread(target=execute_forever).start()

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
