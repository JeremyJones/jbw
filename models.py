"""
models.py - models for the backend python engine test
"""
from requests import get as url_get
from json import loads as jsonloads
from shelve import open as openshelf
from time import sleep
from glob import glob
from os import unlink
from os import path
import signal
import pickle

from behaviours.variance import \
     set_variance_behaviour as default_variance_behaviour
from behaviours.natural_log import \
     set_natural_log_behaviour as default_natural_log_behaviour
from behaviours.mongo_add import \
     mongo_add_behaviour as default_mongo_add_behaviour


class Timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)


class Feed:
    classification = 'quandl.v3.WIKI'

    def __init__(self, symbol: str, url: str=None, data=None,
                 shelf=None, mongodb=None,
                 set_variance_behaviour=None,
                 set_natural_log_behaviour=None) -> None:
        self.symbol = symbol
        self.url = url
        self.data = data

        try:
            if type(self.data) is str:   # could be a dict already, or None
                self.data = jsonloads(self.data)
        except TypeError:
            pass

        if shelf is not None:
            self.restore(shelf)

        self._set_variance_behaviour = (set_variance_behaviour or
                                        default_variance_behaviour)

        self.set_variance_behaviour = self._set_variance_behaviour()

        self._set_natural_log_behaviour = (set_natural_log_behaviour or
                                           default_natural_log_behaviour)

        self.set_natural_log_behaviour = self._set_natural_log_behaviour()

    def __repr__(self) -> str:
        return 'Feed("{s}", "{u}", {d})'.format(
            s=self.symbol,
            u=self.url,
            d='"{}"'.format(self.data) if self.data else "None"
        )

    def restore(self, shelf=None) -> None:
        self.data = shelf.get(self.symbol)

    def _refresh_feed(self) -> None:
        self.data = url_get(self.url).json()

    def refresh(self) -> bool:
        try:
            with Timeout(seconds=10):
                self._refresh_feed()
        except TimeoutError:
            self.data = None
            return False
        else:
            return True

    def add_variance(self) -> None:
        self.set_variance_behaviour.set_variance(self)

    def add_natural_log(self) -> None:
        self.set_natural_log_behaviour.set_natural_log(self)


class Datastore:
    def get(self, key, default=None):
        return self.kv.get(key, default)

    def set(self, key, val):
        self.kv[key] = val

    def open(self) -> None:
        pass

    def finish(self) -> None:  # override this
        raise NotImplementedError


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


class MyPickler(Datastore):

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

    def items(self) -> tuple:
        """
        https://stackoverflow.com/questions/1698596/how-can-i-traverse-a-file-system-with-a-generator
        """
        for filename in glob('{}/*'.format(self.dir)):
            key = filename[len(self.dir) + 1:]
            yield key, self.get(key)

    def finish(self) -> None:
        pass


class DocumentStore:
    pass


class MongoCollection(DocumentStore):
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


class SymbolList:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.symbols = []

    def __len__(self) -> int:
        return len(self.symbols)

    def fill(self) -> None:
        with open(self.filename) as fh:
            for line in fh:
                if line.startswith('"Symbol"'):
                    continue
                elif line.startswith('"'):
                    symbol = line[1:line.index('"', 1)]
                    self.symbols.append(symbol)

    def next(self, sleep_time=0) -> tuple:
        if len(self) == 0:
            self.fill()

        for count, symbol in enumerate(self.symbols):
            if count > 0:
                sleep(sleep_time)
            yield count, symbol
