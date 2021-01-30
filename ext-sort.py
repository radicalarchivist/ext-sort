#!/usr/bin/env python3
"""
ext-sort.py
Desc: A utility that sorts files based on their extension
v.0.3
2020 by radicalarchivist

Usage:
  ext-sort.py [-ckr] -x EXTENSION -t TARGET-DIR SCAN-DIR...
  ext-sort.py --help
  ext-sort.py --version

Options:
  SCAN-DIR                              Directory to be scanned
  -t --target TARGET-DIR                Directory to copy files into
  -x --extension EXTENSION              extension(s) of the files to move
  -r --recursive                        Scan recursively
  -k --keep-structure                   Retains directory structure when moving
  -c --cron                             Used when ext-sort.py is run on a schedule, assumes yes to prompts
  -h --help                             Show this screen
  --version                             Show version info

"""

__VERSION__ = 0.3

#
# TODO:
#
#
import argparse
import os
import shutil
from typing import Dict, Iterable, Container


def diff_path(file_dir, scan_dir):
    return file_dir.replace(scan_dir, "")


def splash(args: Dict) -> None:
    print(f"""Folders to scan: {", ".join(args['SCAN-DIR'])} 
Extension(s): {args['extension']}
Target: {args['target']}
Recursive Mode: {('On' if args['recursive'] else 'Off')}
Keep File Structure: {args['keep_structure']}""", flush=True)


def get_filelist(paths: Iterable, exts: Container, recurse: bool) -> Dict:
    retlist = dict()
    for path in paths:
        print(f"Scanning {path}", end="... ", flush=True)
        retlist[path] = []
        abspath = os.path.abspath(path)
        if not recurse:
            try:
                for item in os.listdir(abspath):
                    if os.path.isdir(os.path.join(path, item)):
                        continue
                    if item.split('.')[-1] in exts:
                        retlist[path].append(os.path.join(path, item))
            except Exception:
                raise
        else:
            try:
                for root, dirs, files in os.walk(abspath):
                    for name in files:
                        if name.split('.')[-1] in exts:
                            retlist[path].append(os.path.join(root, name))
            except Exception:
                raise
        print("Done.", flush=True)
    return retlist


def move_files(filelist: Dict, sources: Iterable, destination: str, keep_structure: bool) -> None:
    print(f"Moving files to {destination}", end="... ", flush=True)
    for source in sources:
        for path in filelist[source]:
            if keep_structure:
                target = os.path.join(destination, diff_path(path, source))
            else:
                _, name = os.path.split(path)
                target = os.path.join(destination, name)
            try:
                tPath, _ = os.path.split(target)
                try:
                    os.makedirs(tPath, exist_ok=True)
                except Exception:
                    raise
                print(f"{path} --> {target}")
                shutil.move(path, target)
            except PermissionError:
                print(f"Failed. Permission Error.", flush=True)
                print("Operation Failed.", flush=True)
                exit(1)
            except Exception:
                raise
    print("Done.", flush=True)


def count_files(filelist: Dict) -> int:
    total = 0
    for path, filename in filelist.items():
        total += len(filename)
    print(f"Found {total} files.", flush=True)
    return total


def yn_prompt(prompt: str) -> bool:
    """
    Yes or no prompt
    """
    while True:
        try:
            answer = input(f"{prompt} (y/[n]) ")
            if answer[0] in ('y', 'n'):
                return answer[0] == 'y'
            else:
                raise ValueError
        except ValueError:
            print('You must enter y or n.', flush=True)
        except IndexError:
            return False


def main(arguments: Dict):
    splash(arguments)
    filelist = get_filelist(arguments['SCAN-DIR'], arguments['extension'], arguments['recursive'])
    if count_files(filelist):
        if not arguments['cron']:
            if yn_prompt(f"Do you wish to move the files to {arguments['target']}?"):
                move_files(filelist, arguments['SCAN-DIR'], arguments['target'], arguments['keep_structure'])
    print("Operation Complete.", flush=True)
    exit(0)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='A utility that sorts files based on their extension')

    parser.add_argument('SCAN-DIR', type=str, nargs='+', help='Directories to be scanned', action='store')
    parser.add_argument('-t', '--target', help='Directory to copy files into', required=True)
    parser.add_argument('-x', '--extension', type=str, nargs='+', help='extension(s) of the files to move', required=True)
    parser.add_argument('-r', '--recursive', action='store_true', help='Scan recursively')
    parser.add_argument('-k', '--keep-structure', action='store_true', help='Retains directory structure when moving')
    parser.add_argument('-c', '--cron', action='store_true', help='Used when ext-sort.py is run on a schedule, assumes yes to prompts')
    parser.add_argument('--version', action='store_true', help='Show version info')

    args = parser.parse_args()

    if args.version:
        print(f'Version is: {__VERSION__}')
        exit(0)

    try:
        main(vars(args))
    except KeyboardInterrupt:
        print("\nOperation Terminated.", flush=True)
