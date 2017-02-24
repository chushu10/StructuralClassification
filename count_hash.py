#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, argparse, json

def merge_hash_dict(d1, d2):
    '''merge d1 into d2'''
    # 1. iterate through all keys of d1
    # 2. check if the key is also in d2
    #   2.1 yes, place the key with the maximum value in d2
    #   2.2 no, add the key-value pair into d2
    for node in d1:
        if node in d2:
            d2[node] = max(d1[node], d2[node])
        else:
            d2[node] = d1[node]
    return d2

def get_hash(hcgpath):
    '''get hash values from a hcg.json file'''
    # 1. load the hcg into a dictionary
    # 2. iterate through all the nodes of the hcg
    # 3. make hash values keys of another dictionary
    #    while the values is its occurrence

    # Load hcg
    f = open(hcgpath, 'r')
    hcg = json.load(f)
    f.close()

    # Iterate through all nodes
    hash_dict = dict()
    for node in hcg:
        if hcg[node]['nhash'] not in hash_dict:
            hash_dict[hcg[node]['nhash']] = 1
        else:
            hash_dict[hcg[node]['nhash']] += 1

    return hash_dict

def count(directory):
    '''count all the indivisual hash values'''
    # 1. iterate through all the hcg.json files
    # 2. get hash values from a hcg.json file
    # 3. merge the hash values into one file
    hash_dict = dict()
    for parent, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename == 'directed_hcg.json':
            # if filename == 'hcg.json':
                hash_dict = merge_hash_dict(get_hash(os.path.join(parent, filename)), hash_dict)
    return hash_dict

def has_hash_and_occurrence(hash_dict, hash_value, occurrence):
    if hash_value in hash_dict:
        if hash_dict[hash_value] == occurrence:
            return True
    return False

def find(directory):
    '''find the file with the specific occurrence of given hash value'''
    # 1. iterate through all the hcg.json files
    # 2. get hash values from a hcg.json file
    # 3. compare the hash values with the given ones
    hash_value = '0100000000000000000'
    occurrence = 2302
    for parent, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename == 'directed_hcg.json':
                hash_dict = get_hash(os.path.join(parent, filename))
                if has_hash_and_occurrence(hash_dict, hash_value, occurrence):
                    print(os.path.join(parent, filename))

def save_to_file(hash_dict, directory):
    # Dump hash_dict to json file
    f = open(os.path.join(directory, 'directed_hash_occurrence.json'), 'w')
    # f = open(os.path.join(directory, 'hash_occurrence.json'), 'w')
    json.dump(hash_dict, f)
    f.close()
    print('[SC]All hash values stored in /%s/hash_occurrence.json' % directory)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='directory of the apk')
    parser.add_argument('-m', '--mode', help='0 = count hash; 1 = find hash')
    args = parser.parse_args()
    if args.directory and args.mode:
        if args.mode == '0':
            hash_dict = count(args.directory)
            save_to_file(hash_dict, args.directory)
        elif args.mode == '1':
            find(args.directory)
        else:
            parser.print_help()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()