import os

from file_reader import FileReader
from utils import create_json
from version_manager import VersionManager
from config import INDATA_FOLDER_PATH, OUTDATA_FOLDER_PATH, REPORT_NAME
import argparse
from file_comparator import FileComparator

stage1, stage2 = ('stage1', 'stage2',)

parser = argparse.ArgumentParser(description='Launcher for DDT.')
parser.add_argument('mode', help='launch mode', choices=(stage1, stage2,))
parser.add_argument('now_date', help='date in format %d-%m-%YT%H-%M-%S')


def _run_generation(outdata_files_path):
    os.makedirs(outdata_files_path)
    for infile_name in os.listdir(INDATA_FOLDER_PATH):
        infile_path = os.path.join(INDATA_FOLDER_PATH, infile_name)
        file_reader = FileReader(infile_path)
        file_reader.read_file()
        json_data = file_reader.general_information.convert_to_dict()
        json_path = os.path.join(outdata_files_path, infile_name.replace('.txt', '.json'))
        create_json(json_path, json_data)


def launch_stage1(now_date):
    with VersionManager() as version_manager:
        current_hash = version_manager.get_current_hash()
        outdata_files_path = os.path.join(OUTDATA_FOLDER_PATH, now_date, current_hash)
        _run_generation(outdata_files_path)


def launch_stage2(now_date):
    with VersionManager() as version_manager:
        previous_hash = version_manager.get_previous_hash()
        version_manager.go_to_previous_commit()
        outdata_files_path = os.path.join(OUTDATA_FOLDER_PATH, now_date, previous_hash)
        _run_generation(outdata_files_path)

        date_path = os.path.join(OUTDATA_FOLDER_PATH, now_date)

        folder_name1, folder_name2 = os.listdir(date_path)
        folder_path1, folder_path2 = os.path.join(date_path, folder_name1), os.path.join(date_path, folder_name2)
        report_path = os.path.join(date_path, REPORT_NAME)

        comparator = FileComparator()
        comparator.create_report(folder_path1, folder_path2, report_path, "utf-8")


if __name__ == "__main__":
    args = parser.parse_args()
    print("Launching mode: '{mode}'".format(mode=args.mode))
    if args.mode == stage1:
        launch_stage1(args.now_date)
    elif args.mode == stage2:
        launch_stage2(args.now_date)
    print("Done...")
