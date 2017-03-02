#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import common.ml as ml
import json, argparse, os, arff
from count_hash import get_hash, count
from common.utils import use_progressbar, count_file

def compute_label_histogram(hcgpath):
    '''compute the histogram of nhashs in hashed call graph. Every label is a
       binary array. The histogram length is 2**len(nhashs)'''
    hcg_hash_dict = get_hash(hcgpath)
    nhashs = [node for node in hcg_hash_dict]
    h = np.zeros(2 ** len(nhashs[0]))
    for nhash in nhashs:
        h[int(''.join([str(i) for i in nhash]), base=2)] += 1
    return h

def embed_all(directory):
    '''iteratively embed all the hashed call graph into a sparse matrix'''
    # 1. iteratively embed all the hcg files into vector spaces
    # 2. add category according to their folders
    # 3. add up all the vectors to a matrix

    # progressbar
    file_count = count_file(directory, '_hcg.json')
    pbar = use_progressbar('Computing label histogram...', file_count)
    pbar.start()
    progress = 0

    matrix = []
    category_set = set()
    for parent, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename == 'directed_hcg.json':
            # if filename == 'hcg.json':
                category = os.path.basename(os.path.split(os.path.split(parent)[0])[0])
                x_i = compute_label_histogram(os.path.join(parent, filename))
                matrix.append(x_i)

                # progressbar
                progress += 1
                pbar.update(progress)

    # progressbar
    pbar.finish()

    matrix = np.array(matrix, dtype=np.int16)
    print matrix.shape
    print '[SC] Converting features vectors to binary...'
    matrix, m = ml.make_binary(matrix)

    return matrix, category_set

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='directory of the hcg file')
    args = parser.parse_args()
    if args.directory:
        matrix, category_set = embed_all(args.directory)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()