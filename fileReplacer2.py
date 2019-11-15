#! python3
# fileReplacer1.py - Replaces all of the files with the same name

import os
import sys
import shutil
import argparse
import pprint
import re

'''
    command filename_identifier -a new_replacement_file_path* -t target_dir -f
    command filename_identifier -u (if _identifier not found, use _base)
    command -s (display current file being used)
    command -ls (list the files)
    command -h or --h (shows options)
'''

prepender = '2_'
repo_name = 'repo'
default_dir = r'' # TODO add default target dir



def main():
    parser = add_arguments()
    args = parser.parse_args()

    # just used to clear initial sub_folders
    if args.clear:
        validateFilePath(args.t)
        clear_sub_folders(args.t, args.clear)
        sys.exit()

    if args.s:
        validateFilePath(args.t)
        print(get_current(args.t))
        sys.exit()
    elif args.l:
        validateFilePath(args.t)
        pprint.pprint(get_file_list(args.t))
        sys.exit()

    if args.FileName is None:
        sys.exit('A filename must be supplied')
    else:
        final_file_name = generate_final_filename(args.FileName)

    # adds the replacement file in the repo, and replaces the file in
    # all sub-folders if -f flag is checked
    if args.add:

        # verify file paths are valid
        replacement_file_path = os.path.abspath(args.add)
        target_dir = os.path.abspath(args.t)
        validateFilePaths(replacement_file_path, target_dir)

        copyFileToRepo(replacement_file_path, target_dir, final_file_name)

        if args.f:
            replaceFileInSubDirs(final_file_name, target_dir)

    if args.update:
        target_dir = os.path.abspath(args.t)
        validateFilePath(target_dir)

        replaceFileInSubDirs(final_file_name, target_dir)


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


def replaceFileInSubDirs(final_file_name, target_dir):
    # gets a list of all the direct subdirectories in target dir
    sub_dirs = os.listdir(target_dir)

    # remove repo folder from list
    sub_dirs.remove('repo')

    # grab file path from repo
    repo_file_list = os.listdir(os.path.join(target_dir, repo_name))
    replacement_file_path = ''

    for file in repo_file_list:
        if re.search('^' + final_file_name + r'\..*', file):
            replacement_file_path = os.path.join(target_dir, repo_name, file)

    # replacement_file_path = os.path.join(target_dir, repo_name, final_file_name)

    # if not os.path.exists(replacement_file_path):
    if replacement_file_path is '':
        sys.exit('File not found in repo')

    for folder in sub_dirs:
        sub_dir_path = os.path.join(target_dir, folder)
        if os.path.isdir(sub_dir_path):
            sub_dir_files = os.listdir(sub_dir_path)
            # remove previous file file
            for file in sub_dir_files:
                if re.search('^' + prepender + '.*', file):
                    os.remove(os.path.join(sub_dir_path, file))
            # add file from repo to every sub_dir
            shutil.copy2(replacement_file_path, sub_dir_path)

    set_current(target_dir, final_file_name)


def add_arguments():
    parser = argparse.ArgumentParser(description="File replacer")
    parser.version = '2.0'

    # main functionality
    parser.add_argument('FileName', metavar='filename', nargs='?')
    parser.add_argument('-a', '--add')
    parser.add_argument('-u', '--update', action='store_true')
    parser.add_argument('-t', metavar='target_directory', default=get_default_directory())

    # utility options
    parser.add_argument('-s', action='store_true')
    parser.add_argument('-f', action='store_false')
    parser.add_argument('-l', action='store_true')
    parser.add_argument('-c', '--clear')
    parser.add_argument('-v', '--version', action='version')

    return parser


def copyFileToRepo(replacement_file_path, target_dir, final_file_name):
    # ensure the repo exists
    repo_dir = os.path.join(target_dir, repo_name)
    validateFilePath(repo_dir)
    splitter = '.'

    extension = replacement_file_path.split(splitter)[1]

    shutil.copy2(replacement_file_path, os.path.join(repo_dir, final_file_name + splitter + extension))


def get_current(target_dir):
    with open(os.path.join(target_dir, repo_name, 'config.txt'), 'r') as config:
        data = config.readlines()
        current = data[1]
    return current


def set_current(target_dir, current_file_name):
    with open(os.path.join(target_dir, repo_name, 'config.txt'), 'w') as config:
        config.write(target_dir + '\n')
        config.write(current_file_name)


def get_file_list(target_dir):
    return os.listdir(os.path.join(target_dir, repo_name))


def get_default_directory():
    return default_dir


def generate_final_filename(file_name):
    final_file_name = file_name

    # if no identifier was supplied, the _base identifier is added
    if '_' not in file_name:
        final_file_name += '_base'

    # adds the prepender to the filename
    final_file_name = prepender + final_file_name

    return final_file_name


def clear_sub_folders(target_dir, prev_prepender):
    sub_dirs = os.listdir(target_dir)
    sub_dirs.remove('repo')
    for folder in sub_dirs:
        sub_dir_path = os.path.join(target_dir, folder)
        if os.path.isdir(sub_dir_path):
            sub_dir_files = os.listdir(sub_dir_path)
            # remove previous file file
            for file in sub_dir_files:
                if re.search('^' + prev_prepender + '.*', file):
                    os.remove(os.path.join(sub_dir_path, file))

if __name__ == "__main__":
    main()
