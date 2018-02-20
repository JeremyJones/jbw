from modelz.Datastore import Datastore
from shelve import open as openshelf


class Shelf(Datastore):
    def __init__(self, shelf=None) -> None:
        self.kv_file = shelf
        self._open()

    def _open(self) -> None:
        self.kv = openshelf(self.kv_file)

    def finish(self) -> None:
        self.kv.close()

    def items(self) -> tuple:
        for key, val in self.kv.items():
            yield key, val
