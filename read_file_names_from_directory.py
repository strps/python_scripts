#This script will read all the files names in a directory and append them to array.

import os
import pprint
import re
import sys

def read_file_names_from_directory(directory):
    files = os.listdir(directory)
    return files

files_name_list = read_file_names_from_directory("C:/Users/csrst/source/repos/DualSYS/sql")

regex = re.compile(r"V[.\d]+__")

def filter_files():
    filtered_files = []
    for file in files_name_list:
        if regex.match(file):
            filtered_files.append( file)
            
    return filtered_files

filtered_files = filter_files()

from typing import List

list_of_files: List[str] = []

count = 0
for file in filtered_files:
    count += 1
    for file_2 in filtered_files:
        if(regex.sub("", file) == regex.sub("", file_2)):
            print(file_2 + " is equal to " + file + "||" + regex.sub("", file) + "||" + regex.sub("", file_2))
            list_of_files.append(file_2)
            # filtered_files.remove(file_2)

print("="*40)
print(list_of_files)



