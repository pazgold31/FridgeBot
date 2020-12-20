class IAction:
    def run(self) -> None:
        raise NotImplementedError

    def restart(self) -> None:
        raise NotImplementedError
