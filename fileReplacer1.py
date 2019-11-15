#! python3
# fileReplacer1.py - Replaces all of the files with the same name

import os
import sys
import shutil
import argparse


# TODO 1) create a process for adding new files 2) create a process for using a previously added file
# TODO have to have the files be sorted (maybe prepended with 2_?)


'''
    logic flows:
    new file
        1) place in repo
            i) rename to 2_{name}_{identifier} (use _base for identifier if none supplied)
            
        2) delete all files in sub folders prepended with {prepender} (2_ is default)
        
        3) place new file in all sub folders
            i) version where sub folders aren't updated?
            
    use old file
        1) identify replacement file
        
        2) delete all files in sub folders prepended with {prepender} (2_ is default)
        
        3) place new file in all sub folders

    naming conventions:

    command -n new_replacement_file_path* new_file_name* target_dir replace_flag(if exists)
    command -u file_in_repo_name file_in_repo_idenifier(if not found, use _base)
    command -s(shows current file being used)
    command -h or --help (shows options)
    
'''

def main():
    # ensure that at least a replacement file is passed
    if len(sys.argv) < 2:
        sys.exit("A file to be replace existing file must be supplied")

    replacement_file = os.path.abspath(sys.argv[1])

    # if no target dir is specified, a default value will be used
    if len(sys.argv) < 3:
        # TODO: add default target directory
        target_dir = ""

	# TODO add target dir
    else:
        target_dir = os.path.abspath(sys.argv[2])

    validateFilePaths(replacement_file, target_dir)

    replaceFileInSubDirs(replacement_file, target_dir)


def validateFilePaths(replacement_file, target_dir):
    # ensures file paths exist
    validateFilePath(replacement_file)
    validateFilePath(target_dir)

    # ensures replacement file is file, target_dir is a directory
    if not os.path.isfile(replacement_file):
        sys.exit("{} is not a valid file")

    if not os.path.isdir(target_dir):
        sys.exit("{} is not a valid target directory")


def validateFilePath(filepath):
    if not os.path.exists(filepath):
        sys.exit("{} is not a valid filepath".format(filepath))


def removeFileIfExists(dir_path, file_name):
    extension_list = ['jpg', 'png', 'jpeg', 'jpf', 'txt', '.csv', '.pdf']
    file_path_without_extension = os.path.abspath(os.path.join(dir_path, file_name))

    for extension in extension_list:
        file_to_remove = '{}.{}'.format(file_path_without_extension, extension)
        if os.path.exists(file_to_remove):
            os.remove(file_to_remove)


def replaceFileInSubDirs(replacement_file, target_dir):
    # gets a list of all the direct subdirectories in target dir
    sub_dirs = os.listdir(target_dir)
    # needed for
    os.chdir(target_dir)

    for dir in sub_dirs:
        # grabs base file name - extension
        file_name = os.path.basename(replacement_file)
        # gets the filepath of the file to replace in the sub directory
        full_file_path = os.path.join(target_dir, dir, file_name)

        # reomving old files from sub directory
        removeFileIfExists(dir, file_name.split(".")[0])

        # paste the new replacement file in the subdirectory
        shutil.copy2(replacement_file, dir)

if __name__ == "__main__":
    main()