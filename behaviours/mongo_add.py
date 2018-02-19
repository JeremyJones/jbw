from datetime import datetime as dt
from json import dumps as jsondumps


class mongo_add_behaviour:
    def add(self, docstore, idvalue, document) -> None:

        try:
            docstore.export_directory
        except TypeError:
            raise RuntimeError("No directory for Mongo files")

        export_filename = '{dir}/{filename}.json'.\
                          format(dir=docstore.export_directory,
                                 filename=idvalue)

        with open(export_filename, 'w') as f:
            f.write(jsondumps(document))
