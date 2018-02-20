"""
models.py - models for the backend python engine test
"""
from glob import glob
from os import unlink
from os import path
import pickle
from behaviours.mongo_add import \
     mongo_add_behaviour as default_mongo_add_behaviour
from modelz.Timeout import Timeout
from modelz.Sleeper import Sleeper
from modelz.Datastore import Datastore
# from modelz.Shelf import Shelf


class SymbolList(Sleeper):
    def __init__(self, filename) -> None:
        self.filename = filename

    def next(self, sleep_time=0) -> tuple:
        with open(self.filename) as fh:
            counter = -1
            for line in fh:
                self.sleep(sleep_time)
                counter += 1
                if line.startswith('"Symbol"'):
                    continue
                elif line.startswith('"'):
                    symbol = line[1:line.index('"', 1)]
                    yield counter, symbol


class MyPickler(Datastore, Sleeper):

    def __init__(self, dirname) -> None:
        self.dir = dirname

    def _make_filename(self, key) -> str:
        return '{}/{}'.format(self.dir, key)

    def get(self, key, default=None) -> object:
        try:
            val = pickle.load(open(self._make_filename(key), "rb"))
        except FileNotFoundError:
            return default
        else:
            return val

    def set(self, key, val) -> None:
        pickle.dump(val, open(self._make_filename(key), "wb"))

    def done(self, keyin) -> None:
        pass

    def _disabled_done(self, keyin) -> None:
        if type(keyin) is list:
            for key in keyin:
                unlink('{}/{}'.format(self.dir, key))
        else:
                unlink('{}/{}'.format(self.dir, keyin))

    def items(self, sleep_time=0) -> tuple:
        # https://stackoverflow.com/questions/1698596/how-can-i-traverse-a-file-system-with-a-generator

        for filename in glob('{}/*'.format(self.dir)):
            self.sleep(sleep_time)
            key = filename[len(self.dir) + 1:]
            yield key, self.get(key)

    def finish(self) -> None:
        pass


class MongoCollection:
    def __init__(self,
                 export_directory=None,
                 mongo_add_behaviour=None) -> None:

        self.added = []

        self._mongo_add_behaviour = (mongo_add_behaviour or
                                     default_mongo_add_behaviour)
        self.mongo_add_behaviour = self._mongo_add_behaviour()

        if export_directory:
            self.export_directory = export_directory

    def add(self, idvalue, doc) -> None:
        self.mongo_add_behaviour.add(self, idvalue, doc)
        self.added.append(idvalue)

    def added(self) -> list:
        return self.added

    def has(self, key) -> bool:
        return path.exists('{}/{}.json'.
                           format(self.export_directory,
                                  key))


class DocumentStore(MongoCollection):
    pass
