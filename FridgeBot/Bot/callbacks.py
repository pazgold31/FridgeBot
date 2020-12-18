from telegram.ext import Dispatcher, CommandHandler


class Callbacks:
    @staticmethod
    def initialize_handlers(dispatcher: Dispatcher):
        dispatcher.add_handler(CommandHandler("start", Callbacks.start))
        dispatcher.add_handler(CommandHandler("help", Callbacks.help))
        dispatcher.add_error_handler(Callbacks.error)

    @staticmethod
    def start(update, context):
        update.message.reply_text('You just started the conversation!')

    @staticmethod
    def help(update, context):
        # TODO: add actual help
        update.message.reply_text('Here is some help:')

    @staticmethod
    def error(update, context):
        pass