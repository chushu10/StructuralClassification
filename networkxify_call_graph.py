#!/usr/bin/env python
# -*- coding: utf-8 -*-
import common.pz as pz
import networkx as nx
import os, argparse
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
    methods = self.d.get_methods()
    for method in methods:
        node_name = self.get_method_label(method)

        # find calls from this method
        children = []
        for cob in method.XREFto.items:
            remote_method = cob[0]
            children.append(self.get_method_label(remote_method))

        # find all instructions in method and encode using coloring
        instructions = []
        for i in method.get_instructions():
            instructions.append(i.get_name())
        encoded_label = self.color_instructions(instructions)
        # add node, children and label to nx graph
        fcg.add_node(node_name, label=encoded_label)
        fcg.add_edges_from([(node_name, child) for child in children])

    return fcg

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
                    fnx = os.path.join(out, "{}.pz".format(h))
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