from file_parser import FileParser
from itertools import islice
from pathlib import Path

# Get csv file(s) path
data_folder = Path.cwd().parent
cars_csv_path = str(data_folder) + '/cars.csv'
personal_info_csv_path = str(data_folder) + '/personal_info.csv'


with FileParser(cars_csv_path) as data:
    for row in islice(data, 10):
        print(row)


with FileParser(personal_info_csv_path) as data:
    for row in islice(data, 10):
        print(row)
