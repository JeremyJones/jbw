from secretvars import API_KEY

FEED_URL = ("https://www.quandl.com" +
            "/api/v3/datasets/WIKI/" +
            "{symbol}.json?api_key=%s" % API_KEY)

SYMBOLS_CSV = 'symbollist.csv'
FEED_FETCH_SLEEP = 2
SHELF_FILE = 'feeds'
KV_DIR = '_kv'
EXPORT_DIRECTORY = 'datajson'
