#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, json, os
from generate_call_graph import generate
from smali_opcode import HCG_FILE_NAME

def string_xor(s1, s2):
    '''bitwise exlusive or(XOR) of two strings'''
    # 1. convert strings to a list of character pair tuples
    # 2. go through each tuple, converting them to utf-8 integer (int)
    # 3. perform exclusive or on the utf-8 integer
    # 4. then convert the result back to utf-8 string (str)
    # 5. merge the resulting array of characters as a string
    return ''.join(str(int(a) ^ int(b)) for a,b in zip(s1, s2))

def string_rot(s, x):
    '''x-bit rotation(ROT) to the left'''
    # example:
    #   if s is '110101', then string_rot(s, 1) is '101011'
    #   the result can be split as '10101' and '1'
    #   which is s[1:] and s[0]
    return s[x:] + s[0:x]

def neighborhood_hash(cg, graphdir):
    '''neighborhood hash of a directed graph'''
    # 1. iterate through all the nodes of the graph
    # 2. for each node, do:
    #   2.1 1-bit ROT for the node itself, result marked as n
    #   2.2 XOR for all in-comming neighbors, then 2-bits ROT, result marked as i
    #   2.3 XOR for all out-going neighbors, then 3-bits ROT, result marked as o
    #   2.4 the final label nhash = n XOR i XOR o

    hash_cg = cg
    for node in cg:
        # print('[SC]Hashing node %s' % node)
        rot_label = string_rot(cg[node]['label'], 1)
        if len(cg[node]['in_neighbors']) > 0:
            xor_label = cg[cg[node]['in_neighbors'][0]]['label']
            for i in range(1, len(cg[node]['in_neighbors'])):
                xor_label = string_xor(xor_label, cg[cg[node]['in_neighbors'][i]]['label'])
            rot_label = string_xor(rot_label, string_rot(xor_label, 2))
        if len(cg[node]['out_neighbors']) > 0:
            xor_label = cg[cg[node]['out_neighbors'][0]]['label']
            for i in range(1, len(cg[node]['out_neighbors'])):
                xor_label = string_xor(xor_label, cg[cg[node]['out_neighbors'][i]]['label'])
            rot_label = string_xor(rot_label, string_rot(xor_label, 3))
        hash_cg[node]['nhash'] = rot_label

    return hash_cg

def save_to_file(hash_cg, graphdir):
    # Dump hash_cg to json file
    f = open(os.path.join(graphdir, HCG_FILE_NAME), 'w')
    json.dump(hash_cg, f)
    f.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--apkpath', help='path of the apk')
    args = parser.parse_args()
    if args.apkpath:
        cg, graphdir = generate(args.apkpath)
        hash_cg = neighborhood_hash(cg, graphdir)
        save_to_file(hash_cg, graphdir)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()