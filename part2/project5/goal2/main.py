from file_parser import parsed_data
from itertools import islice
from pathlib import Path

# Get csv file(s) path
data_folder = Path.cwd().parent

cars_csv_path = str(data_folder) + '/cars.csv'
personal_info_csv_path = str(data_folder) + '/personal_info.csv'

f_names = cars_csv_path, personal_info_csv_path
for f_name in f_names:
    with parsed_data(f_name) as data:
        for row in islice(data, 5):
            print(row)
    print('-------------------')
