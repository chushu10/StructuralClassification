#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import argparse, os, time, sys
from generate_call_graph import generate
from neighborhood_hash import neighborhood_hash, save_to_file
from common.utils import use_progressbar
from common.utils import count_file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='directory of the apk')
    args = parser.parse_args()
    if args.directory:
        # progressbar
        file_count = count_file(args.directory, '.apk')
        pbar = use_progressbar('Generating hashed call graph...', file_count)
        pbar.start()
        progress = 0

        graph_time_list = []
        hash_time_list = []
        graph_node_time_list = []
        hash_node_time_list = []
        min_file_size = sys.maxint
        max_file_size = 0
        min_node_count = sys.maxint
        max_node_count = 0
        min_graph_time = sys.maxint
        max_graph_time = 0
        min_hash_time = sys.maxint
        max_hash_time = 0
        for parent, dirnames, filenames in os.walk(args.directory):
            for filename in filenames:
                if filename.endswith('.apk'):
                    apk_file = os.path.join(parent, filename)
                    # check file size
                    file_size = os.stat(apk_file).st_size

                    # graph generation and neighborhood hash
                    start_time = time.time()
                    cg, graphdir = generate(apk_file)
                    graph_time = time.time() - start_time

                    start_time = time.time()
                    hash_cg = neighborhood_hash(cg, graphdir)
                    hash_time = time.time() - start_time

                    save_to_file(hash_cg, graphdir)

                    graph_time_coordinate = (file_size/(10**6), graph_time)
                    hash_time_coordinate = (file_size/(10**6), hash_time)
                    graph_node_time_coordinate = (len(cg), graph_time)
                    hash_node_time_coordinate = (len(cg), hash_time)
                    graph_time_list.append(graph_time_coordinate)
                    hash_time_list.append(hash_time_coordinate)
                    graph_node_time_list.append(graph_node_time_coordinate)
                    hash_node_time_list.append(hash_node_time_coordinate)

                    if file_size > max_file_size:
                        max_file_size = file_size
                    if len(cg) > max_node_count:
                        max_node_count = len(cg)
                    if file_size < min_file_size:
                        min_file_size = file_size
                    if len(cg) < min_node_count:
                        min_node_count = len(cg)
                    if graph_time > max_graph_time:
                        max_graph_time = graph_time
                    if graph_time < min_graph_time:
                        min_graph_time = graph_time
                    if hash_time > max_hash_time:
                        max_hash_time = hash_time
                    if hash_time < min_hash_time:
                        min_hash_time = hash_time

                    # progressbar
                    progress += 1
                    pbar.update(progress)

        # progressbar
        pbar.finish()

        # sort list
        graph_time_list.sort(key=lambda tup: tup[0])
        hash_time_list.sort(key=lambda tup: tup[0])
        graph_node_time_list.sort(key=lambda tup: tup[0])
        hash_node_time_list.sort(key=lambda tup: tup[0])

        # save time consumption
        f = open(os.path.join(args.directory,'time_evaluation'), 'w')
        f.write('max file size:%f\n' % (max_file_size/(10**6)) )
        f.write('min file size:%f\n' % (min_file_size/(10**6)) )
        f.write('max node count:%d\n' % max_node_count)
        f.write('min node count:%d\n' % min_node_count)
        f.write('max graph time:%f\n' % max_graph_time)
        f.write('min graph time:%f\n' % min_graph_time)
        f.write('max hash time:%f\n' % max_hash_time)
        f.write('min hash time:%f\n' % min_hash_time)
        f.write('graph generation(size):\n')
        for gtc in graph_time_list:
            f.write(str(gtc))

        f.write('\nneighborhood hash(size):\n')
        for htc in hash_time_list:
            f.write(str(htc))

        f.write('\ngraph generation(node):\n')
        for gntc in graph_node_time_list:
            f.write(str(gntc))

        f.write('\nneighborhood hash(node):\n')
        for hntc in hash_node_time_list:
            f.write(str(hntc))
        f.close()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()