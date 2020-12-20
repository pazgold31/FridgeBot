import json
import logging

from telegram.ext import Dispatcher, CommandHandler

from FridgeBot.configuration import TEMPERATURE_SENSOR, HUMIDITY_SENSOR, OPENING_SWITCH, KEYS_FILE_PATH, FAN_A, FAN_B, \
    UV_LIGHT_RELAY
from FridgeBot.version import __version__


class Callbacks:
    @staticmethod
    def initialize_handlers(dispatcher: Dispatcher):
        dispatcher.add_handler(CommandHandler("start", Callbacks.start))
        dispatcher.add_handler(CommandHandler("help", Callbacks.help))
        dispatcher.add_handler(CommandHandler("status", Callbacks.status))
        dispatcher.add_handler(CommandHandler("door", Callbacks.door))
        dispatcher.add_handler(CommandHandler("uv", Callbacks.uv))
        dispatcher.add_handler(CommandHandler("fans", Callbacks.fans))
        dispatcher.add_handler(CommandHandler("version", Callbacks.version))
        dispatcher.add_error_handler(Callbacks.error)

    @staticmethod
    def start(update, context):
        chat_key = update.message.chat.id
        with open(KEYS_FILE_PATH, "rt") as fh:
            parsed_json = json.load(fh)

        if chat_key not in parsed_json:
            parsed_json.append(chat_key)

            with open(KEYS_FILE_PATH, "wt") as fh:
                json.dump(parsed_json, fh)

        update.message.reply_text('FridgeBot at your service!')

    @staticmethod
    def help(update, context):
        update.message.reply_text('/start - Register to the bot\n'
                                  '/status - presents the status of the fridge\n'
                                  '/door - presents the status of the door\n'
                                  '/fans - control the fans\n'
                                  '/uv - control the uv light\n'
                                  '/version - shows the version\n')

    @staticmethod
    def version(update, context):
        update.message.reply_text('FridgeBot v{}'.format(__version__))

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
    def fans(update, context):
        try:
            args = context.args
            if "on" == args[0].lower():
                FAN_A.forward(255)
                FAN_B.forward(255)
                update.message.reply_text("Turned Fans on")
            elif "off" == args[0].lower():
                FAN_A.stop()
                FAN_B.stop()
                update.message.reply_text("Turned Fans off")
            else:
                update.message.reply_text("Invalid option {}".format(args[0]))
        except Exception:
            logging.exception("Received exception in fans callback")
            update.message.reply_text("Failed to process fans command")

    @staticmethod
    def uv(update, context):
        try:
            args = context.args
            if "on" == args[0].lower():
                UV_LIGHT_RELAY.on()
                update.message.reply_text("Turned UV light on")
            elif "off" == args[0].lower():
                UV_LIGHT_RELAY.off()
                update.message.reply_text("Turned UV light off")
            else:
                update.message.reply_text("Invalid option {}".format(args[0]))
        except Exception:
            logging.exception("Received exception in uv callback")
            update.message.reply_text("Failed to process uv command")

    @staticmethod
    def error(update, context):
        logging.warning('Update "%s" caused error "%s"', update, context.error)
