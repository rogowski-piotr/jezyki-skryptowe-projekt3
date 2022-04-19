import re
import os
from subprocess import PIPE, run

from numpy import size
from FileSystemElement import File


class FileSystemService:
    def __init__(self):
        self.REGEX_CONVERT = re.compile(("^(?P<type>[-|b|c|d|l|n|p|s])"
                                         "(?P<permissions>[-|r|w|x]{9})\s+"
                                         "(?P<hard_links>[0-9]+)\s+"
                                         "(?P<owner>[a-zA-Z]+)\s+"
                                         "(?P<group>[a-zA-Z]+)\s+"
                                         "(?P<size>[0-9]+)\s+"
                                         "(?P<date>\S+\s\d+\s\d+:\d+)\s+"
                                         "(?P<name>.*$)"))

    def convert_str_to_files(self, files_str: list):
        files = []
        for file_str in files_str:
            try:
                resultSearch = self.REGEX_CONVERT.search(file_str)
                files.append(File(
                    resultSearch.group('type'),
                    resultSearch.group('permissions'),
                    resultSearch.group('hard_links'),
                    resultSearch.group('owner'),
                    resultSearch.group('group'),
                    resultSearch.group('size'),
                    resultSearch.group('date'),
                    resultSearch.group('name')))
            except: pass
        return files

    def list_files(self, show_hidden=False, sort='none', alphabetically=True):
        cmd = 'ls -lhr'
        cmd += 'a' if show_hidden else ''
        cmd += '' if alphabetically else 'U'
        cmd += f' --sort={sort}'
        print(cmd)
        output = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        if (output.returncode != 0): raise Exception(f'\nCan not execute command: ls -lhra\nReason: {output.stderr}\n')
        return self.convert_str_to_files(output.stdout.split('\n'))

    def goto_directory(self, file: File):
        current_path = os.getcwd()
        target_path = os.path.join(current_path, file.get_name(), '')
        os.chdir(target_path)

    def goto_path(self, path: str):
        os.chdir(path)

    def get_current_workspace(self):
        return os.getcwd()


if __name__ == "__main__":
    service = FileSystemService()

    service.goto_path('/mnt/c/Users/rogus/Desktop/Jezyki Skryptowe Projekt 3/test_dir')

    files = service.list_files()
    for i in files:
        print(i)

    service.goto_directory(files[4])

    current_workspace = service.get_current_workspace()
    print(current_workspace)

    service.goto_path('/mnt/c/Users/rogus/Desktop/Jezyki Skryptowe Projekt 3/test_dir')

    current_workspace = service.get_current_workspace()
    print(current_workspace)