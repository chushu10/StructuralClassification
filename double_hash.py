#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, json, os, time
from neighborhood_hash import neighborhood_hash, save_to_file
from common.utils import use_progressbar, count_file, read_hashed_call_graph
from smali_opcode import HCG_FILE_NAME

def save_to_file(hash_cg, graphdir):
    # Dump hash_cg to json file
    f = open(os.path.join(graphdir, 'directed_double_hcg_15bit.json'), 'w')
    json.dump(hash_cg, f)
    f.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='directory of the apk')
    args = parser.parse_args()

    if args.directory:
        # progressbar
        file_count = count_file(args.directory, HCG_FILE_NAME)
        pbar = use_progressbar('double hashing...', file_count)
        pbar.start()
        progress = 0

        for parent, dirnames, filenames in os.walk(args.directory):
            for filename in filenames:
                if filename == HCG_FILE_NAME:
                    graphdir = parent
                    hcg = read_hashed_call_graph(os.path.join(parent, filename))
                    for node in hcg:
                        hcg[node]['label'] = hcg[node]['nhash']
                    double_hcg = neighborhood_hash(hcg, graphdir)
                    save_to_file(double_hcg, graphdir)
                    
                    # progressbar
                    progress += 1
                    pbar.update(progress)

        # progressbar
        pbar.finish()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()