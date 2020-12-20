import logging
import time

from FridgeBot.configuration import Tasks


def execute_forever():
    while True:
        for task in Tasks:
            try:
                if task.can_run():
                    Tasks.execute(task)
            except Exception:
                logging.exception("Task Failed with exception")

        time.sleep(0.5)
