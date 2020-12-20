class IFilter:
    def filter(self) -> bool:
        raise NotImplementedError

    def restart(self) -> None:
        raise NotImplementedError
