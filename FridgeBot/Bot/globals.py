def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class BotWrapper:
    def __init__(self):
        self.bot = None

    def set_bot(self, bot):
        self.bot = bot
