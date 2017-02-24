#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, argparse, os
from count_hash import get_hash

def embed(hcgpath, N, M, hash_value_list):
    '''embed the hashed call graph into a vector space, the dimension is N*M'''
    hash_dict = get_hash(hcgpath)
    vector = []

def embed_all(directory, N, M, hash_value_list):
    '''iteratively embed all the hashed call graph into vector spaces'''
    matrix = []
    caption = []
    # for parent, dirnames, filenames in os.walk(directory):
    #     for filename in filenames:
    #         if filename == 'directed_hcg.json':
    #         # if filename == 'hcg.json':
    #             category = os.path.basename(os.path.split(os.path.split(parent)[0])[0])
    #             vector = embed(os.path.join(parent, filename), N, M, hash_value_list)
    #             vector.append(category)
    #             matrix.append(vector)
    f = open(os.path.join(directory, 'directed_matrix.csv'), 'w')
    for vec in matrix:
        for i in range(len(vec)-1):
            f.write(str(vec[i]) + ',')
        f.write(vec[len(vec)-1] + '\n')
    f.close()

def get_hash_occurrence(hopath):
    '''get the occurrence of all the difference hash values'''
    # 1. read hash occurrence dict(hod) from hash_occurrence.json file
    # 2. get the total numbers of hash values as N
    # 3. get the maximum occurrence of hash values as M
    # 4. get all the different hash values as hash_list

    # Load hash occurrence dict(hod)
    f = open(hopath, 'r')
    hod = json.load(f)
    f.close()

    # Get N
    N = len(hod)

    # Get M and hash values
    occurrence_list = []
    hash_value_list = []
    for h in hod:
        occurrence_list.append(hod[h])
        hash_value_list.append(h)
    M = max(occurrence_list)

    return N, M, hash_value_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='directory of the hcg file')
    parser.add_argument('-p', '--hopath', help='path of the hash occurrence file')
    args = parser.parse_args()
    if args.directory and args.hopath:
        N, M, hash_value_list = get_hash_occurrence(args.hopath)
        embed_all(args.directory, N, M, hash_value_list)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()