import csv
from collections import namedtuple
from contextlib import contextmanager


@contextmanager
def parsed_data(f_name):
    f = open(f_name, 'r')
    try:
        dialect = csv.Sniffer().sniff(f.read(1000))
        f.seek(0)
        reader = csv.reader(f, dialect)
        headers = map(lambda x: x.lower(), next(reader))
        nt = namedtuple('Data', headers)
        yield (nt(*row) for row in reader)
    finally:
        f.close()
