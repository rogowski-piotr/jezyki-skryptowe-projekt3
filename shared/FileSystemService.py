from itertools import count
import re
import os
from subprocess import PIPE, run
import random
from numpy import size
from shared.FileSystemElement import File


class FileSystemService:
    def __init__(self):
        self.REGEX_CONVERT = re.compile(("^(?P<type>[-|b|c|d|l|n|p|s])"
                                         "(?P<permissions>[-|r|w|x]{9})\s+"
                                         "(?P<hard_links>[0-9]+)\s+"
                                         "(?P<owner>[a-zA-Z]+)\s+"
                                         "(?P<group>[a-zA-Z]+)\s+"
                                         "(?P<size>[0-9]+[,|.]*[0-9]*K*)\s*"
                                         "(?P<date>\S+\s*\d+\s\d+:\d+)\s+"
                                         "(?P<name>.*$)"))

    # Pobranie informacji o plikach w podanej ścieżce
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

    # Wykonanie komendy 'ls' z parametrami
    def list_files(self, show_hidden=True, sort='extension', alphabetically=True):
        cmd = 'ls -lhr'
        cmd += 'a' if show_hidden else ''
        cmd += '' if alphabetically else 'U'
        cmd += f' --sort={sort}'

        output = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        if (output.returncode != 0):
            raise Exception(f'\nCNie można wykonać operacji: "ls -lhra".\nPowód: {output.stderr}.\n')
        files = self.convert_str_to_files(output.stdout.split('\n'))
        return files
  
    # Przejście do katalogu
    def goto_directory(self, file: File):
        current_path = os.getcwd()
        target_path = os.path.join(current_path, file.get_name(), '')
        os.chdir(target_path)

    # Przejście do podanej ścieżki bezwzględnej
    def goto_path(self, path: str):
        try:
            os.chdir(path)
            return 0
        except FileNotFoundError:
            return -1

    # Pobranie aktualnej ścieżki
    def get_current_workspace(self):
        return os.getcwd()

    # Dodawanie nowego pliku
    def add_new_file(self, path, file_name):
        self.goto_path(path)
        cmd = f'touch {file_name}'
        output = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        if output.returncode != 0:
            raise ValueError(cmd, output.stderr[:-1])
            
    # Dodawanie nowego katalogu
    def add_new_dir(self, path, name):
        self.goto_path(path)
        cmd = f'mkdir {name}'
        output = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        if output.returncode != 0:
            raise ValueError(cmd, output.stderr[:-1])
           
    # Zmiana nazwy pliku/kataologu
    def change_name(self, path, old_name, new_name):
        self.goto_path(path)
        cmd = f"mv {path}/{old_name} {path}/{new_name}"
        output = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        if output.returncode != 0: 
            raise ValueError(cmd, output.stderr[:-1])

    # Usuwanie pliku/katalogu
    def delete(self, path, name, file_type):
        self.goto_path(path)
        cmd = f"rm {path}/{name}"
        if file_type == 'd':
            cmd += ' -rf'
        output = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        if output.returncode != 0: 
            raise ValueError(cmd, output.stderr[:-1])
