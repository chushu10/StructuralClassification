#!/usr/bin/env python
# -*- coding: utf-8 -*-
from progressbar import *
import os, json

def use_progressbar(title, maxval, marker='#', left='[', right=']'):
    '''return a progressbar obj'''
    widgets = [title,
               Percentage(), ' ',
               Bar(marker=marker, left=left, right=right),
               ' ', ETA(), ' ']
    pbar = ProgressBar(widgets=widgets, maxval=maxval)
    return pbar

def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z

def count_file(directory, extension):
    '''count files with specific extension in a directory'''
    count = 0
    for parent, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extension):
                count += 1
    return count

def read_hashed_call_graph(hcgpath):
    '''read hashed call graph from file'''
    # Load hcg
    f = open(hcgpath, 'r')
    hcg = json.load(f)
    f.close()

    return hcg