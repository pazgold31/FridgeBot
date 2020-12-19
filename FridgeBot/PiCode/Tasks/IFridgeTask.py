class IFridgeTask:
    def can_run(self) -> bool:
        raise NotImplementedError

    def restart(self) -> None:
        raise NotImplementedError

    def is_finished(self) -> bool:
        raise NotImplementedError

    def run(self) -> None:
        raise NotImplementedError
