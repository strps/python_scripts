# A script that takes a path and a list of files in the path to append with themselves.
#
# The script should be able to take a path and a list of files in the path to append with themselves.
#

import os
import sys


"""
    Append files content into a output file
    :param path: path to the directory
    :param files: list of files to append
    :param output_file_name: name of output file
    :param output_file_directory: directory of output file
    :return: None
"""
def append_files(directory , files, output_file_name="output.sql", output_file_directory=None, add_file_name_header=True):

    if output_file_directory is None:
        output_file_directory = directory 
    
    with open(os.path.join(output_file_directory, output_file_name), "w", encoding="utf-8") as output_file:
        for file in files:
            with open(os.path.join(directory, file), "r", encoding="utf-8") as f:
                data = f.read()
                output_file.write(data)


# if __name__ == "__main__":
#     path = sys.argv[1]
#     files = sys.argv[2:]
#     append_files(path, files)

out_dir = "C:/Users/csrst/source/repos/DualSYS/sql"
dir = "C:/Users/csrst/source/repos/DualSYS/sql"
files = [
    "V10__adding_information_province_canton.sql", 
    "V11__adding_sanjose_district_information.sql",
    "V12__adding_alajuela_district_information.sql",
    "V13__adding_cartago_district_information.sql",
    "V14__adding_heredia_district_information.sql",
    "V15__adding_guanacaste_district_information.sql",
    "V16__adding_puntarenas_district_information.sql",
    "V17__adding_limon_district_information.sql"
    ]
append_files(dir, files, output_file_directory=out_dir)
