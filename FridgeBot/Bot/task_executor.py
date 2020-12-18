import time

from FridgeBot.configuration import Tasks


def execute_forever():
    while True:
        for task in Tasks:
            if task.can_run():
                task.run()
                Tasks.execute(task)

        time.sleep(0.5)
