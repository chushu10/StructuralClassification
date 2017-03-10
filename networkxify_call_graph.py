#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import common.pz as pz
import networkx as nx
import os, argparse
from generate_call_graph import generate
from common.utils import use_progressbar, count_file

def networkxify(cg):
    """ Using NX and Smali, build a directed graph NX object so that:
        - node names are method names as: class name, method name and
          descriptor
        - each node has a label that encodes the method behavior
    """
    # nx graph for FCG extracted from APK: nodes = method_name,
    # labels = encoded instructions
    fcg = nx.DiGraph()
    for method in cg:
        node_name = get_method_label(method)

        # find calls from this method
        children = []
        for cob in cg[method]['out_neighbors']:
            children.append(get_method_label(cob))

        # use the pre-generated labels
        label_str = cg[method]['label']
        label_len = len(label_str)
        h = [0] * label_len
        for i in range(label_len):
            h[i] = int(label_str[i])
        encoded_label = np.array(h)

        # add node, children and label to nx graph
        fcg.add_node(node_name, label=encoded_label)
        fcg.add_edges_from([(node_name, child) for child in children])

    return fcg

def get_method_label(method):
    pointer_index = method.find('->')
    bracket_index = method.find('(', pointer_index)
    class_name = 'L' + method[0:pointer_index]
    method_name = method[pointer_index+2:bracket_index]
    parameter = method[bracket_index:]
    return (class_name, method_name, parameter)

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
                    fcg = networkxify(cg)
                    h = os.path.splitext(filename)[0]
                    fnx = os.path.join(graphdir, "{}.pz".format(h))
                    pz.save(fcg, os.path.join(graphdir, fnx))

                    # progressbar
                    progress += 1
                    pbar.update(progress)

        # progressbar
        pbar.finish()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()