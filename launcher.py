import os

from file_reader import FileReader
from utils import create_json
from version_manager import VersionManager
from datetime import datetime
from config import INDATA_FOLDER_PATH, OUTDATA_FOLDER_PATH

now = datetime.now()
dt_string = now.strftime("%d-%m-%YT%H-%M-%S")


sample = FileReader()
entries = os.listdir(INDATA_FOLDER_PATH)

with VersionManager() as version_manager:
    current_hash = version_manager.get_current_hash()
    outdata_files_path = os.path.join(OUTDATA_FOLDER_PATH, dt_string, current_hash)
    os.makedirs(outdata_files_path)
    for entry in entries:
        sample.set_file_path(INDATA_FOLDER_PATH, entry)
        sample_obj = sample.read_file()
        json_data = sample.general_information.convert_to_dict()
        json_path = os.path.join(outdata_files_path, entry.strip('.txt') + '.json')
        create_json(json_path, json_data)


# import argparse
# parser = argparse.ArgumentParser(description='Add some integers.')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='interger list')
# parser.add_argument('--sum', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')
# args = parser.parse_args()
# print(args.sum(args.integers))
