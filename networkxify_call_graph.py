#!/usr/bin/env python
# -*- coding: utf-8 -*-
import common.pz as pz
import networkx as nx
import os, argparse
from common.utils import use_progressbar, count_file

def networkxify(cg):
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='directory of the apk')
    args = parser.parse_args()
    if args.directory:
        # progressbar
        file_count = count_file(args.directory, '.apk')
        pbar = use_progressbar('networkxifying call graph...', file_count)
        pbar.start()
        progress = 0

        for parent, dirnames, filenames in os.walk(args.directory):
            for filename in filenames:
                if filename.endswith('.apk'):
                    # print(os.path.join(parent, filename))
                    cg, graphdir = generate(os.path.join(parent, filename))


                    # progressbar
                    progress += 1
                    pbar.update(progress)

        # progressbar
        pbar.finish()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()