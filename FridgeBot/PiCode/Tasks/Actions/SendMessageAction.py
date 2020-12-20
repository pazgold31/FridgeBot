import json
import logging

from FridgeBot.Bot.globals import BotWrapper
from FridgeBot.PiCode.Tasks.Actions.IAction import IAction


class SendMessageAction(IAction):
    def __init__(self, message: str, keys_file_path: str):
        self._message = message
        self._keys_file_path = keys_file_path

    def run(self) -> None:

        if not BotWrapper().bot:
            logging.error("Bot is not")
            raise RuntimeError

        with open(self._keys_file_path, "rt") as fh:
            chat_ids = json.load(fh)

        for chat_id in chat_ids:
            BotWrapper().bot.send_message(chat_id=chat_id, text=self._message)

    def restart(self) -> None:
        pass
