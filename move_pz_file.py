#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input directory of the pz')
    parser.add_argument('-o', '--output', help='ouput directory of the pz')
    args = parser.parse_args()
    if args.input and args.output:
        for parent, dirnames, filenames in os.walk(args.input):
            for filename in filenames:
                if filename.endswith('.pz'):
                    category = os.path.basename(os.path.split(os.path.split(parent)[0])[0])
                    ouput_directory = os.path.join(args.output, category)
                    if not os.path.isdir(ouput_directory):
                        os.mkdir(ouput_directory)
                    os.rename(os.path.join(parent, filename), os.path.join(ouput_directory, filename))
    else:
        parser.print_help()

if __name__ == '__main__':
    main()