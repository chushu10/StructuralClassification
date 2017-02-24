#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse, os
from generate_call_graph import generate
from neighborhood_hash import neighborhood_hash, save_to_file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='directory of the apk')
    args = parser.parse_args()
    if args.directory:
        for parent, dirnames, filenames in os.walk(args.directory):
            for filename in filenames:
                if filename.endswith('.apk'):
                    # print(os.path.join(parent, filename))
                    cg, graphdir = generate(os.path.join(parent, filename))
                    hash_cg = neighborhood_hash(cg, graphdir)
                    save_to_file(hash_cg, graphdir)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()