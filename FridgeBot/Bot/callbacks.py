import logging

from telegram.ext import Dispatcher, CommandHandler

from FridgeBot.configuration import TEMPERATURE_SENSOR, HUMIDITY_SENSOR


class Callbacks:
    @staticmethod
    def initialize_handlers(dispatcher: Dispatcher):
        dispatcher.add_handler(CommandHandler("start", Callbacks.start))
        dispatcher.add_handler(CommandHandler("help", Callbacks.help))
        dispatcher.add_handler(CommandHandler("status", Callbacks.status))
        dispatcher.add_error_handler(Callbacks.error)

    @staticmethod
    def start(update, context):
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
            update.message.reply_text("Failed to receive the temperature")

    @staticmethod
    def error(update, context):
        logging.warning('Update "%s" caused error "%s"', update, context.error)
