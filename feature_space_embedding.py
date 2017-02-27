#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, argparse, os, arff
from count_hash import get_hash
from common.utils import use_progressbar

def embed(hcgpath, N, M, hash_value_list):
    '''embed the hashed call graph into a sparse vector space, the dimension is N*M'''
    # 1. get the hash occurrence of one single hashed call graph(hcg_hash_dict)
    # 2. loop through all the possible hash value(hash_value_list)
    #   2.1 if the hash value does not in hcg_hash_dict, do nothing
    #   2.2 if the hash value in hcg_hash_dict
    hcg_hash_dict = get_hash(hcgpath)
    vector = []
    for i in range(len(hash_value_list)):
        if hash_value_list[i] in hcg_hash_dict:
            occurrence = hcg_hash_dict[hash_value_list[i]]
            # vector.append(str(i) + ' ' + str(occurrence))
            for j in range(occurrence):
                vector.append(str(j+(i*M)) + ' 1')
    return vector

def embed_all(directory, N, M, hash_value_list):
    '''iteratively embed all the hashed call graph into a sparse matrix'''
    # 1. iteratively embed all the hcg files into vector spaces
    # 2. add category according to their folders
    # 3. add up all the vectors to a matrix

    # progressbar
    pbar = use_progressbar('Start embedding...', 1260)
    pbar.start()
    progress = 0

    matrix = []
    category_set = set()
    for parent, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename == 'directed_hcg.json':
            # if filename == 'hcg.json':
                category = os.path.basename(os.path.split(os.path.split(parent)[0])[0])
                category_set.add(category)
                vector = embed(os.path.join(parent, filename), N, M, hash_value_list)
                vector.append(str(N) + ' ' + category)
                matrix.append(vector)

                # progressbar
                progress += 1
                pbar.update(progress)

    # progressbar
    pbar.finish()

    return matrix, category_set

def save_to_arff(matrix, hash_value_list, category_set, directory):
    '''save the matrix to a arff file for training'''
    # 1. write 'relation' and 'attributes' areas
    # 2. write 'data' area
    f = open(os.path.join(directory, 'weka_sparse_data.arff'), 'w')
    
    # f.write('@relation sparse.data\n')
    # f.write('\n')
    # for hash_value in hash_value_list:
    #     f.write('@attribute ' + hash_value + ' numeric\n')
    # f.write('@attribute class {')
    # cnt = 0
    # for category in category_set:
    #     if cnt < len(category_set)-1:
    #         f.write(category + ',')
    #     else:
    #         f.write(category)
    #     cnt += 1
    # f.write('}\n')
    # f.write('\n')
    f.write('@data\n')
    for vector in matrix:
        f.write('{')
        for i in range(len(vector)-1):
            f.write(vector[i] + ',')
        f.write(vector[len(vector)-1])
        f.write('}\n')

    f.close()

def save_to_file(hash_value_list, directory):
    f = open(os.path.join(directory, 'hash_value_list.txt'), 'w')
    for hash_value in hash_value_list:
        f.write(hash_value + '\n')
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
        matrix, category_set = embed_all(args.directory, N, M, hash_value_list)
        save_to_arff(matrix, hash_value_list, category_set, args.directory)
        # save_to_file(hash_value_list, args.directory)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()