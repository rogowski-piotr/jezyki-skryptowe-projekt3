from itertools import count
import re
import os
from subprocess import PIPE, run
import random

from numpy import size
from FileSystemElement import File


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

    def list_files(self, show_hidden=True, sort='extension', alphabetically=True):
        print(f'listing files from: {os.getcwd()}')
        cmd = 'ls -lhr'
        cmd += 'a' if show_hidden else ''
        cmd += '' if alphabetically else 'U'
        cmd += f' --sort={sort}'

        output = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        print(f'output: {output.stdout}')
        if (output.returncode != 0): raise Exception(f'\nCan not execute command: ls -lhra\nReason: {output.stderr}\n')
        files = self.convert_str_to_files(output.stdout.split('\n'))
        print(files)
        return files
        
#         mock1 = """total 92K
# -rwxrwxrwx 1 piotr piotr 1.1K Apr 28 19:24  FilesList.py
# -rwxrwxrwx 1 piotr piotr  617 Apr 23 21:21  FileSystemElement.py
# -rwxrwxrwx 1 piotr piotr 2.8K Apr 28 18:23  FileSystemService.py
# -rwxrwxrwx 1 piotr piotr 2.9K Apr 28 19:09  gui.py
# -rwxrwxrwx 1 piotr piotr   74 Apr 23 21:28  main.py
# -rwxrwxrwx 1 piotr piotr  72K Apr 25 11:42  Projekt3.docx
# drwxrwxrwx 1 piotr piotr  512 Apr 23 21:21  test_dir
# -rwxrwxrwx 1 piotr piotr 1.5K Apr 28 19:04  tmp.py
# drwxrwxrwx 1 piotr piotr  512 Apr 28 19:24  __pycache__
# -rwxrwxrwx 1 piotr piotr  162 Apr 28 18:31 '~$ojekt3.docx'
# """
#         mock2 = """
# total 300K
# drwxrwxrwx 1 piotr piotr  512 Apr 28 18:26  .
# drwxrwxrwx 1 piotr piotr  512 Apr 28 16:33  ..
# -rwxrwxrwx 1 piotr piotr  378 Nov 23 21:47  archiwizacja.bat
# -rwxrwxrwx 1 piotr piotr 1.3K Jul 19  2021 'Arduino IDE.lnk'
# -rwxrwxrwx 1 piotr piotr  282 Jul 19  2021  desktop.ini
# -rwxrwxrwx 1 piotr piotr 2.2K Feb 21 16:36  Discord.lnk
# -rwxrwxrwx 1 piotr piotr 2.1K Apr  3 18:33 'Docker Desktop.lnk'
# drwxrwxrwx 1 piotr piotr  512 Apr 28 18:04  file-browser-with-python-PyQt5-master
# -rwxrwxrwx 1 piotr piotr 4.0K Apr 28 18:04  file-browser-with-python-PyQt5-master.zip
# drwxrwxrwx 1 piotr piotr  512 Feb 23 12:37  game-udp-receiver
# drwxrwxrwx 1 piotr piotr  512 Apr 28 18:27  gui
# -rwxrwxrwx 1 piotr piotr 4.3K Apr 28 18:26  gui.zip
# drwxrwxrwx 1 piotr piotr  512 Apr 28 21:31  jezyki-skryptowe-projekt3
# drwxrwxrwx 1 piotr piotr  512 Apr 28 16:32  jezyki_skryptowe_3
# -rwxrwxrwx 1 piotr piotr 2.4K Jan 20 19:28 'Microsoft Teams.lnk'
# -rwxrwxrwx 1 piotr piotr  742 Jul 19  2021  OneDrive.lnk
# -rwxrwxrwx 1 piotr piotr 2.2K Apr 27 18:47  Postman.lnk
# drwxrwxrwx 1 piotr piotr  512 Apr 20 21:12 'program faktury'
# drwxrwxrwx 1 piotr piotr  512 Apr  4 20:27  system-benchmarking-microservices-spring-boot
# -rwxrwxrwx 1 piotr piotr 1021 Jul 19  2021 'Visual Studio Code.lnk'
# -rwxrwxrwx 1 piotr piotr  162 Sep 17  2021 '~$it-resume-TT-Norms.docx'
# -rwxrwxrwx 1 piotr piotr  162 Oct 24  2021 '~$stem akwizycji i przechowywania danych z urządzeń IoT.docx'
# -rwxrwxrwx 1 piotr piotr  162 Aug 11  2021 '~$wy Dokument programu Microsoft Word.docx'
# -rwxrwxrwx 1 piotr piotr 259K Oct 24  2021 '~WRL0003.tmp'
# """
#         if random.randint(0, 10) % 2:
#             return self.convert_str_to_files(mock2.split('\n'))
#         return self.convert_str_to_files(mock1.split('\n'))


    def goto_directory(self, file: File):
        current_path = os.getcwd()
        target_path = os.path.join(current_path, file.get_name(), '')
        print(f'changing directory to: {target_path}')
        os.chdir(target_path)

    def goto_path(self, path: str):
        os.chdir(path)
        print(f'changing directory to: {os.getcwd()}')

    def get_current_workspace(self):
        return os.getcwd()


if __name__ == "__main__":
    service = FileSystemService()

    service.goto_path('/mnt/c/Users/rogus/Desktop/Jezyki Skryptowe Projekt 3/test_dir')

    files = service.list_files()
    print(type(files))
    for i in files:
        print(i)

    service.goto_directory(files[4])

    current_workspace = service.get_current_workspace()
    print(current_workspace)

    service.goto_path('/mnt/c/Users/rogus/Desktop/Jezyki Skryptowe Projekt 3/test_dir')

    current_workspace = service.get_current_workspace()
    print(current_workspace)