"""
Retrieve and process ingested feed data, adding some derived
fields and making the data suitable for import into MongoDB.
"""
from models import MongoCollection
from models import MyPickler as Ingestor
from myvars import KV_DIR, EXPORT_DIRECTORY
from json import dumps as jsondumps


def main() -> None:
    keyvals = Ingestor(KV_DIR)
    collection = MongoCollection(EXPORT_DIRECTORY)

    for symbol, feed in keyvals.items():
        if 'quandl_error' in feed.data:
            continue
        elif collection.has(feed.symbol):
            continue

        feed.add_variance()
        feed.add_natural_log()
        collection.add(feed.symbol, feed.data)
        print("Added {} to mongo.".format(symbol), flush=True)

    # tell the ingestor it can housekeep the ones we've put into mongo
    keyvals.done(collection.added)
    print("All done, added {} record{}.".
          format(len(collection.added),
                 '' if len(collection.added) == 1 else 's'))


if __name__ == '__main__':
    main()
