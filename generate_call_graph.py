#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, argparse, json, re, time
from command import *
from common.utils import merge_two_dicts
from smali_opcode import INSTRUCTION_SET_COLOR
from smali_opcode import INSTRUCTION_CLASSES
from smali_opcode import INSTRUCTION_CLASS_COLOR
from smali_opcode import CG_FILE_NAME

def get_methods(classpath, dirset):
    '''get all methods of a class along with the methods's label'''
    # 1. iterate through each line of the class file
    # 2. when '.method' occurs in the line, start recording the method
    #   2.1 when 'invoke-' occurs in the line, recording the method's out-comming neighbors
    #   2.2 otherwise, recording the method's dvm opcode
    # 3. when '.end method' occurs in the line, end recording the method
    f = open(classpath, 'r')
    lines = f.read().splitlines()
    f.close()

    methods = dict()
    method_flag = 0
    method_name = ''
    for line in lines:
        if (line.find('.method') != -1) and (line.split()[0] == '.method'): # enter a method
            method_flag = 1
            # print(classpath[16:-6])
            # print(line[0:line.find(')')+1].split())
            method_name = classpath[16:-6] + ';->' + line[0:line.find(')')+1].split()[-1]
            methods[method_name] = {}
            methods[method_name]['label'] = ''
            label = [0] * len(INSTRUCTION_CLASSES)
            # methods[method_name]['apis'] = []
            methods[method_name]['out_neighbors'] = []
            methods[method_name]['in_neighbors'] = []
        if (line.find('.end method') != -1) and (line.split()[0] == '.end'): # exit a method
            methods[method_name]['label'] = ''.join([str(x) for x in label])
            method_flag = 0
        if method_flag == 1:
            # if (line.find('invoke-') != -1) and (line[0:6] == 'invoke-'):
            if (line.find('invoke-') != -1) and (line.split()[0][0:7] == 'invoke-'):
                invoke_name = line[line.find('}, L')+4:line.find(')', line.find('}, L')+4)+1]
                if not has_only_android_api(invoke_name, dirset):
                    if invoke_name not in methods[method_name]['out_neighbors']:
                        methods[method_name]['out_neighbors'].append(invoke_name)
                # else:
                #     if invoke_name not in methods[method_name]['apis']:
                #         methods[method_name]['apis'].append(invoke_name)
            elif line != '':
                opcode = line.split()[0]
                indent = len(line) - len(line.lstrip())
                if (re.match(r'[a-z]', opcode[0])) and (indent == 4):
                    # print("indent: %d, %s" % (len(line) - len(line.lstrip()), opcode))
                    label[INSTRUCTION_SET_COLOR[opcode]] = 1
    return methods

def get_dirset():
    '''get all the possible paths of one apk'''
    # walk through all the directories and record them in a set
    dirset = set()
    for parent, dirnames, filenames in os.walk(os.path.join('workspace', 'smali')):
        for filename in filenames:
            dirset.add(parent.replace('workspace/smali/', ''))
    return dirset

def has_only_android_api(method, dirset):
    '''return if a method is android official api'''
    for dirname in dirset:
        if dirname in method:
            return False
    return True

def generate(apkpath):
    '''generate apk's call graph'''
    # 1. decompile the apk to a given directory
    # 2. iterate through all classes and record their methods
    # 3. merge all the methods and we got the directed call graph
    # 4. connect all in-comming neighbors

    # Decompile apk
    DA_clean()
    DA_move_file(apkpath, os.path.join('workspace', 'test.apk'))
    DA_unzip()
    DA_baksmali()

    # Iterate through all classes
    dirset = get_dirset()
    cg = dict()
    for parent, dirnames, filenames in os.walk(os.path.join('workspace', 'smali')):
        for filename in filenames:
            if filename.endswith('.smali'):
                classpath = os.path.join(parent, filename)
                methods = get_methods(classpath, dirset)
                # cg = {**cg, **methods} # merge two dict
                cg = merge_two_dicts(cg, methods) # merge two dict

    # Make cg undirected
    # print('[SC]Making graph undirected...')
    # for src in cg:
    #     for dst in cg:
    #         if (src in cg[dst]['neighbors']) and (dst not in cg[src]['neighbors']):
    #             cg[src]['neighbors'].append(dst)

    # Eliminate useless out_neighbors and connect in_neighbors
    for src in cg:
        legal_neighbors = []
        for neighbor in cg[src]['out_neighbors']:
            if neighbor in cg:
                legal_neighbors.append(neighbor)
                if src not in cg[neighbor]['in_neighbors']:
                    cg[neighbor]['in_neighbors'].append(src)
        cg[src]['out_neighbors'] = legal_neighbors

    apkname = os.path.basename(os.path.normpath(apkpath)).split('.')[0]
    if not os.path.isdir(os.path.join(os.path.split(apkpath)[0], 'cg')):
        os.mkdir(os.path.join(os.path.split(apkpath)[0], 'cg'))
    graphdir = os.path.join(os.path.join(os.path.split(apkpath)[0], 'cg'), apkname)
    if not os.path.isdir(graphdir):
        os.mkdir(graphdir)
    return cg, graphdir

def save_to_file(cg, graphdir):
    f = open(os.path.join(graphdir, CG_FILE_NAME), 'w')
    json.dump(cg, f)
    f.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--apkpath', help='path of the apk')
    args = parser.parse_args()
    if args.apkpath:
        start_time = time.time()
        cg, graphdir = generate(args.apkpath)
        cost_time = time.time() - start_time
        print('costs' + str(cost_time) + ' seconds.')
        save_to_file(cg, graphdir)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()