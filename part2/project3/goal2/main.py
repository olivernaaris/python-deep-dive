from pathlib import Path
from datetime import datetime
from collections import namedtuple
from collections import defaultdict
from functools import partial

# Get csv file path
data_folder = Path.cwd().parent
file_name = str(data_folder) + '/' + 'nyc_parking_tickets_extract.csv'


# Read csv file and get the first line of the csv for column_name
def column_headers():
    with open(file_name) as f:
        column_headers = next(f).strip('\n').split(',')
        return column_headers


# Read the data in the file, we have to skip the first row in the file.
# Also, I have to use a with statement and the file name every time.
# To make life easier, I'm going to write a small utility function that will yield just the data rows from the file
def read_data():
    with open(file_name) as f:
        next(f)
        yield from f


# Function that will try to convert a value to an integer,
# or return some default if the value is missing or not an integer
def parse_int(value, *, default=None):
    try:
        return int(value)
    except ValueError:
        return default


# We need to do the same thing with dates. It looks like the dates are provided in M/D/YYYY format,
# so we'll use that to parse the date.
# We'll use the strptime function available in the datetime package.
def parse_date(value, *, default=None):
    data_format = '%m/%d/%Y'
    try:
        return datetime.strptime(value, data_format).date()
    except ValueError:
        return default


# String parser - we want to remove any potential leading and trailing spaces.
def parse_string(value, *, default=None):
    try:
        cleaned = value.strip()
        if not cleaned:
            return default
        else:
            return cleaned
    except ValueError:
        return default


# Read list of column_headers and create a new list of cleaned up column_names
column_names = [header.replace(' ', '_').lower() for header in column_headers()]
Ticket = namedtuple('Ticket', column_names)


# To make life easier, I'm going to create a tuple that contains the functions that should be called to clean up each field.
# The tuple positions will correspond to the fields in the data row.
# I'm also going to specify what the default value should be when there is a problem parsing the fields.
# To do this, I will use partials, because I still need a callable for each element of the column parser tuple.
# (Note that I could just as easily use a lambda as well instead of partials).
column_parsers = (parse_int,  # summons_number, default is None
                  parse_string,  # plate_id, default is None
                  partial(parse_string, default=''),  # state
                  partial(parse_string, default=''),  # plate_type
                  parse_date,  # issue_date, default is None
                  parse_int,  # violation_code
                  partial(parse_string, default=''),  # body type
                  parse_string,  # make, default is None
                  lambda x: parse_string(x, default='')  # description
                 )


# To parse each field in a row, I'll first separate the data fields into a list of values,
# then I'll apply the functions in column_parsers to the data in that list.
# To do that, I'm going to zip up the parser functions and the data,
# and use a comprehension to apply each function to it's corresponding data field
def parse_row(row, *, default=None):
    fields = row.strip('\n').split(',')
    # note that I'm using a list comprehension here,
    # since we'll need to iterate through the entire parsed fields
    # twice - one time to check if nothing is None
    # and another time to create the named tuple
    parsed_data = [func(field)
                   for func, field in zip(column_parsers, fields)]
    if all(item is not None for item in parsed_data):
        print(*parsed_data)
        return Ticket(*parsed_data)
    else:
        return default


# Let's create an iterator to easily iterate over the cleaned up and structured data in the file, skipping None rows
def parsed_data():
    for row in read_data():
        parsed = parse_row(row)
        if parsed:
            yield parsed


# What we want to do here is iterate through the file and keep a counter,
# for each make, of how many rows for that make was encountered.
# A good approach is to use a dictionary to keep track of the makes (as keys),
# and the value can be a counter that is initialized to 1 if the key (make) does not already exist,
# or incremented by 1 if it does.
def violation_counts_by_make():
    # Make use of a special type of dictionary called a defaultdict.
    # The way a defaultdict works, is that if you try to retrieve a non-existent key from the dictionary,
    # it will return a default value. It does need to know the data type to use for the default - so we should provide one.
    makes_counts = defaultdict(int)
    for data in parsed_data():
        makes_counts[data.vehicle_make] += 1

    return {make: cnt
            for make, cnt in sorted(makes_counts.items(),
                                    key=lambda t: t[1],
                                    reverse=True)
            }


print(violation_counts_by_make())
