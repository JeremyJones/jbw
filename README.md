Butterwire
==========

Assumptions
-----------

1. Python 3.6.
1. An API key for the web-based data service quandl is available.


Installation
------------

After cloning the repository, change into the repo directory and do the following.

1. Create a file `secretvars.py` which defines a Python variable called `API_KEY` with your quandl API key.
1. Optionally create a file `symbollist.csv` where the first field in each line is a symbol to retrieve.
1. Create the directories `_kv` and `datajson` 


Using the Ingestor
------------------

The ingestor is run with `python ingestor.py`

Note that the file `secretvars.py` must exist in your directory containing a defined variable called `API_KEY`.

The data will be consumed from quandl and stored in a key/value datastore.


Using the Processor/Exporter
----------------------------

To process and export the data run `python process_and_export.py`

The data will be retrieved from the key/value datastore, updated with variance and natural log information, and then stored in MongoDB-compatible JSON format.


Behaviours
----------

Several of the behaviours are encapsulated into interchangeable elements, so that they can be modified in future without affecting the core code. They are:

1. Calculation of Variance from Average Price
1. Calculation of Natural Log
1. Export into MongoDB

Issues
------

1. Many
1. The file `models.py` is too long

