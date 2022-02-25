from pathlib import Path
from parse_utils import parse_date

# Get csv file(s) path
data_folder = Path.cwd().parent

# Files
fname_personal = str(data_folder) + '/personal_info.csv'
fname_employment = str(data_folder) + '/employment.csv'
fname_vehicles = str(data_folder) + '/vehicles.csv'
fname_update_status = str(data_folder) + '/update_status.csv'
fnames = fname_personal, fname_employment, fname_vehicles, fname_update_status

# Parsers
personal_parser = (str, str, str, str, str)
employment_parser = (str, str, str, str)
vehicle_parser = (str, str, str, int)
update_status_parser = (str, parse_date, parse_date)
parsers = personal_parser, employment_parser, vehicle_parser, update_status_parser

# Named Tuple Names
personal_class_name = 'Personal'
employment_class_name = 'Employment'
vehicle_class_name = 'Vehicle'
update_status_class_name = 'UpdateStatus'
class_names = personal_class_name, employment_class_name, vehicle_class_name, update_status_class_name

# Field Inclusion/Exculsion
personal_fields_copress = [True, True, True, True, True]
employment_fields_compress = [True, True, True, False]
vehicle_fields_compress = [False, True, True, True]
update_status_fields_compress = [False, True, True]
compress_fields = (personal_fields_copress,
                   employment_fields_compress,
                   vehicle_fields_compress,
                   update_status_fields_compress)
