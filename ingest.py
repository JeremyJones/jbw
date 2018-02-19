"""
Ingest a web-based data service and store in a key/value datastore.
"""

from models import Feed, SymbolList
from models import MyPickler as Ingestor
from vars import (SYMBOLS_CSV, FEED_URL, KV_DIR,
                  FEED_FETCH_SLEEP)


def main() -> None:
    kv = Ingestor(KV_DIR)
    symlist = SymbolList(SYMBOLS_CSV)

    for _, symbol in symlist.next(FEED_FETCH_SLEEP):
        f = Feed(symbol, url=FEED_URL.format(symbol=symbol))
        f.refresh()
        kv.set(symbol, f)

    kv.finish()


if __name__ == '__main__':
    main()
