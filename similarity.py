#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, argparse, json
from command import *

def get_code_string(apkpath):
    # Decompile apk
    DA_clean()
    DA_move_file(apkpath, os.path.join('workspace', 'test.apk'))
    DA_unzip()
    DA_baksmali()

    code_string = ''
    for parent, dirnames, filenames in os.walk(os.path.join('workspace', 'smali')):
        for filename in filenames:
            if filename.endswith('.smali'):
                print(os.path.join(parent, filename))
                # f = open(os.path.join(parent, filename))
                # string = f.readlines()
                # f.close()

def similarity(apkA, apkB):
    # 1. decompile apk
    # 2. iterate through all dirs, find smalis
    # 3. paste into a large file
    # 4. compare two large files
    # 5. return similarity
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--apkA', help='path of the apk A')
    parser.add_argument('-b', '--apkB', help='path of the apk B')
    args = parser.parse_args()
    if args.appA and args.appB:
        print('similarity: 90%')
    else:
        parser.print_help()

if __name__ == '__main__':
	main()