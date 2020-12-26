import logging
import time

from FridgeBot.configuration import Tasks


def execute_forever():
    failures = {}
    while True:
        for task in Tasks:
            try:
                if task.can_run():
                    Tasks.execute(task)
            except Exception:
                try:
                    failures[task] += 1
                except KeyError:
                    failures[task] = 1
                except Exception:
                    logging.exception("Unknown exception caught on failures handle")

                if failures[task] < 5 or failures[task] % 10 == 0:
                    logging.exception("Task Failed with exception")

        time.sleep(0.5)
