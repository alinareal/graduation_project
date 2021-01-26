import os

from file_reader import FileReader
from utils import create_json
from version_manager import VersionManager
from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%d-%m-%YT%H-%M-%S")
version_obj = VersionManager()
commit_hash = version_obj.git('rev-parse HEAD')
outdata_folder = 'outdata'
json_path = os.path.join('outdata', dt_string, commit_hash)
dirName = '{outdata_folder}/{dt_string}/{commit_hash}'.format(outdata_folder=outdata_folder, dt_string=dt_string,
                                                              commit_hash=commit_hash)
sample = FileReader()
entries = os.listdir('indata/')

with VersionManager() as version_manager:
    os.makedirs(dirName)
    for entry in entries:
        sample.set_file_path('indata', entry)
        sample_obj = sample.read_file()
        json_data = sample.general_information.convert_to_dict()
        json_path = os.path.join(dirName, entry.strip('.txt') + '.json')
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