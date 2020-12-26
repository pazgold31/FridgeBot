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
            parsed_json = json.load(fh)

        for client_dict in parsed_json:
            if not client_dict["silent"]:
                BotWrapper().bot.send_message(chat_id=client_dict["chatid"], text=self._message)

    def restart(self) -> None:
        pass
