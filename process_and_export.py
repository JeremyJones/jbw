"""
Retrieve and process ingested feed data, adding some derived fields and making the data suitable for import into MongoDB.
"""
from models import MongoCollection
from models import MyPickler as Ingestor
from vars import KV_DIR, EXPORT_DIRECTORY
from json import dumps as jsondumps


def main() -> None:
    keyvals = Ingestor(KV_DIR)
    mongo = MongoCollection(EXPORT_DIRECTORY)

    for symbol, feed in keyvals.items():
        if 'quandl_error' in feed.data:
            # raise RuntimeWarning("Feed failure for symbol {}".
            #                      format(feed.symbol))
            print("Skipping {}".format(symbol), flush=True)
            continue

        feed.add_variance()
        feed.add_natural_log()
        mongo.add(feed.symbol, feed.data)
        print("Added {}".format(symbol), flush=True)

    # tell the ingestor it can housekeep the ones we've put into mongo
    keyvals.done(mongo.added)
    print("All done.")


if __name__ == '__main__':
    main()
