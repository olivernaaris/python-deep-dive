from pathlib import Path

data_folder = Path.cwd().parent

file_name = str(data_folder) + '/' + 'nyc_parking_tickets_extract.csv'

with open(file_name) as f:
    for _ in range(10):
        print(next(f))
