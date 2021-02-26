import os

from file_reader import FileReader
from utils import create_json
from version_manager import VersionManager
from datetime import datetime
from config import INDATA_FOLDER_PATH, OUTDATA_FOLDER_PATH
import argparse

now = datetime.now()
dt_string = now.strftime("%d-%m-%YT%H-%M-%S")
stage1, stage2 = ('stage1', 'stage2',)

parser = argparse.ArgumentParser(description='Launcher for DDT.')
parser.add_argument('mode', help='launch mode', choices=(stage1, stage2,))



def _run_generation(outdata_files_path):
    os.makedirs(outdata_files_path)
    for infile_name in os.listdir(INDATA_FOLDER_PATH):
        infile_path = os.path.join(INDATA_FOLDER_PATH, infile_name)
        file_reader = FileReader(infile_path)
        file_reader.read_file()
        json_data = file_reader.general_information.convert_to_dict()
        json_path = os.path.join(outdata_files_path, infile_name.replace('.txt', '.json'))
        create_json(json_path, json_data)


def launch_stage1():
    with VersionManager() as version_manager:
        current_hash = version_manager.get_current_hash()
        outdata_files_path = os.path.join(OUTDATA_FOLDER_PATH, dt_string, current_hash)
        _run_generation(outdata_files_path)


def launch_stage2():
    with VersionManager() as version_manager:
        previous_hash = version_manager.get_previous_hash()
        version_manager.go_to_previous_commit()
        outdata_files_path = os.path.join(OUTDATA_FOLDER_PATH, dt_string, previous_hash)
        _run_generation(outdata_files_path)


if __name__ == "__main__":
    # args = parser.parse_args()
    # print("Launching mode: '{mode}'".format(mode=args.mode))
    # if args.mode == stage1:
    #     launch_stage1()
    # elif args.mode == stage2:
    #     launch_stage2()
    # print("Done...")
    launch_stage1()
