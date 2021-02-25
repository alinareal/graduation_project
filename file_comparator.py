# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import difflib
import io
import os
from hashlib import md5
from typing import IO, AnyStr, List, Optional


class FileComparator(object):

    LINE_ENDING = "\n"

    def __init__(self):  # type: () -> None
        self.source1 = None  # type:  Optional[IO, None]
        self.source2 = None  # type: Optional[IO, None]
        self.report = None  # type: Optional[IO, None]

    @staticmethod
    def _get_file_hash(source, encoding):  # type: (IO, AnyStr) -> int
        hasher = md5()
        text = source.read().encode(encoding)
        hasher.update(text)
        hash_value = hasher.hexdigest()
        return hash_value

    def _write_report_block(self, message, param, sep="-", sep_num=200):
        # type: (AnyStr, AnyStr, AnyStr, int) -> None
        sep_line = sep * sep_num
        self.report.write(sep_line)
        self.report.write(self.LINE_ENDING)
        self.report.write(message.format(param))
        self.report.write(self.LINE_ENDING)
        self.report.write(sep_line)
        self.report.write(self.LINE_ENDING)

    def _process_file_content(self, diffs):  # type: (List[AnyStr]) -> int

        number_of_diffs = 0
        previous_code = ""
        line_num = 0

        for line in diffs:

            code = line[:2]
            line_num += 1

            if code == "- ":
                number_of_diffs += 1
            elif code == "+ " and previous_code in ("", "+ ", "  "):
                number_of_diffs += 1
            elif code == "+ " and previous_code in ("- ", "? "):
                line_num -= 1
            elif code == "? ":
                line_num -= 1

            if code != "  ":
                self.report.write("{line_num}: {line}\n".format(line_num=line_num, line=line.strip()))

            previous_code = code

        return number_of_diffs

    def _compare_files_by_hash(self, encoding):  # type: (AnyStr) -> int
        hash1 = self._get_file_hash(self.source1, encoding)
        hash2 = self._get_file_hash(self.source2, encoding)
        return 0 if hash1 == hash2 else 1

    def _compare_files_by_content(self, encoding):  # type: (AnyStr) -> int

        number_of_diffs = self._compare_files_by_hash(encoding)

        if number_of_diffs:
            self._write_report_block("Difference between files: {}.", self.source1.name)

            self.source1.seek(0)
            self.source2.seek(0)

            lines1 = self.source1.readlines()
            lines2 = self.source2.readlines()

            diffs = difflib.Differ().compare(lines1, lines2)
            number_of_diffs = self._process_file_content(diffs)

            self._write_report_block("Diffs for the file is {}:", str(number_of_diffs))
            self.report.write(self.LINE_ENDING * 2)

        return number_of_diffs

    def _process_files_diff(self, diff, names1, names2):
        # type: (set, List, List) -> None
        self.report.write("Various number of files during report creation!\n")
        self.report.write("Rejected files {number}:\n".format(number=len(diff)))
        for name in diff:
            self.report.write("{name}\n".format(name=name))
            if name in names1:
                names1.remove(name)
            if name in names2:
                names2.remove(name)

    @staticmethod
    def _check_names(names1, names2):
        # type: (AnyStr, AnyStr) -> bool
        if names1 != names2:
            warn_message = "Files should have the same names during comparing! {names1} <> {names2}"
            print(warn_message.format(names1=names1, names2=names2))
            print("Impossible to make difference report!")
            return False
        return True

    # TODO adding blocksize reading can be usefull in the future
    def create_report(self, path1, path2, report_path, encoding, folder_name_to_write=None):
        # type: (AnyStr, AnyStr, AnyStr, AnyStr, Optional[AnyStr]) -> Optional[int, None]
        """
            Create report with the full information about comparing of two datasets of files:
            - number of compared files
            - total diffs found
            - rejected files
            - if the files have diff - diff lines will be in the report

            Example:
            *******************************************************************************************************
            Encoding of files is shift-jis.
            *******************************************************************************************************
            Difference between files: payment...02_ZENGIN.txt.
            -------------------------------------------------------------------------------------------------------
            1: - 1111OTHID.COMPdesc1.COMP-FR1                          01060123DESC1.BB-FR1   456DESC2.BB-FR1
            1: ? ^
            1: + 2111OTHID.COMPdesc1.COMP-FR1                          01060123DESC1.BB-FR1   456DESC2.BB-FR1
            1: ? ^
            -------------------------------------------------------------------------------------------------------
            Diffs for the file is 1:
            -------------------------------------------------------------------------------------------------------

            *******************************************************************************************************
            Total files compared 3
            *******************************************************************************************************
            Total number of diffs is 2
            *******************************************************************************************************
        """
        total_diffs = 0

        names1 = sorted(os.listdir(path1))
        names2 = sorted(os.listdir(path2))

        files_diff = set(names1).symmetric_difference(set(names2))

        with io.open(report_path, "a+", encoding=encoding) as self.report:

            if folder_name_to_write is not None:
                self._write_report_block("Comparing of file from: {} directory.", folder_name_to_write, sep="*")

            self._write_report_block("Encoding of files: {}.", encoding, sep="*")

            if files_diff:
                self._process_files_diff(files_diff, names1, names2)
                total_diffs += len(files_diff)

            for name1, name2 in zip(names1, names2):

                if not self._check_names(name1, name2):
                    return

                file_path1 = os.path.join(path1, name1)
                file_path2 = os.path.join(path2, name2)

                with io.open(file_path1, "r", encoding=encoding) as self.source1:
                    with io.open(file_path2, "r", encoding=encoding) as self.source2:
                        total_diffs += self._compare_files_by_content(encoding)

            self._write_report_block("Total files compared: {}", str(len(names1)), sep="*")
            self._write_report_block("Total number of diffs: {}", str(total_diffs), sep="*")
            self.report.write(self.LINE_ENDING)

        print("Diff report was created: {report_path}".format(report_path=report_path))

        return total_diffs
