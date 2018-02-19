Butterwire
==========

The web-based data service is quandl.


Using the Ingestor
------------------

The ingestor is run with `python ingestor.py`

Note that the file secretvars.py must exist in your directory containing a defined variable called `API_KEY`.

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

