# -*- coding: utf-8 -*-
import os
import subprocess

from typing import AnyStr


class VersionManager(object):
    REPO_PATH = os.getcwd()

    def __init__(self):
        self.current_branch = None

    def __enter__(self):
        self.current_branch = self.git('branch --show-current')
        return self

    def __exit__(self, type, value, traceback):
        self.git('checkout {current_branch}'.format(current_branch=self.current_branch))

    @staticmethod
    def git(command, tool="git"):  # type: (AnyStr, AnyStr) -> AnyStr
        execution_command = " ".join((tool, "-C {}".format(VersionManager.REPO_PATH), command))
        print("{tool} executed command is '{command}'.".format(tool=tool, command=execution_command))
        process = subprocess.Popen(execution_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        execution_result, error = process.communicate()
        execution_result = execution_result.decode(encoding='UTF-8').strip('\n')

        message = "Result of {tool} command execution is '{execution_result}'."
        print(message.format(tool=tool, execution_result=execution_result))

        if process.returncode == 1:
            print("Error during {tool} command execution is '{error}'".format(tool=tool, error=error))
            raise EnvironmentError

        return execution_result

    def go_to_previous_commit(self):
        commit_hash = self.git('log -1 --skip 1 --format=format:"%H"').strip('"')
        self.go_to_any_commit(commit_hash)

    def go_to_any_commit(self, commit_hash):
        self.git('checkout {commit_hash}'.format(commit_hash=commit_hash))

    def go_to_current_commit(self):
        commit_hash = self.git('log --pretty=format:"%h" -1').strip('"')
        self.go_to_any_commit(commit_hash)
