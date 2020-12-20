import json
import logging

from telegram.ext import Dispatcher, CommandHandler

from FridgeBot.configuration import TEMPERATURE_SENSOR, HUMIDITY_SENSOR, OPENING_SWITCH, KEYS_FILE_PATH


class Callbacks:
    @staticmethod
    def initialize_handlers(dispatcher: Dispatcher):
        dispatcher.add_handler(CommandHandler("start", Callbacks.start))
        dispatcher.add_handler(CommandHandler("help", Callbacks.help))
        dispatcher.add_handler(CommandHandler("status", Callbacks.status))
        dispatcher.add_handler(CommandHandler("door", Callbacks.door))
        dispatcher.add_error_handler(Callbacks.error)

    @staticmethod
    def start(update, context):
        chat_key = update.message.chat.id
        with open(KEYS_FILE_PATH, "rt") as fh:
            parsed_json = json.load(fh)

        if chat_key not in parsed_json:
            parsed_json.append(chat_key)

            with open(KEYS_FILE_PATH, "wt") as fh:
                json.dump(fh, parsed_json)

        update.message.reply_text('FridgeBot at your service!')

    @staticmethod
    def help(update, context):
        # TODO: add actual help
        update.message.reply_text('/status - presents the status of the fridge')

    @staticmethod
    def status(update, context):
        try:
            temperature = TEMPERATURE_SENSOR.get()
            humidity = HUMIDITY_SENSOR.get()
            update.message.reply_text(
                'The current temperature is {temperature:.2f}C and humidity is {humidity:.1f}%'.format(
                    temperature=temperature, humidity=humidity))
        except Exception:
            logging.exception("Received exception in status callback")
            update.message.reply_text("Failed to receive the temperature and humidity")

    @staticmethod
    def door(update, context):
        try:
            update.message.reply_text("The door is {}".format("closed" if OPENING_SWITCH.is_clicked() else "open"))
        except Exception:
            logging.exception("Received exception in door callback")
            update.message.reply_text("Failed to receive the door status")

    @staticmethod
    def error(update, context):
        logging.warning('Update "%s" caused error "%s"', update, context.error)
