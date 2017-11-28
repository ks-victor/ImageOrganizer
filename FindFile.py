#!/usr/bin/python

import os
import curses
import hashlib



parser = argparse.ArgumentParser(description="Find duplicate files and moves them other folder")
parser.add_argument('root_path', type=str, action="store", help="Path to folder to scan")

args = parser.parse_args()


dubdir = args.root_path+"/dub"
filelist = []
dict = {}


def filewalk(path):
    count = 0
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if root == dubdir:
                continue
            if filename[:1] == '.':
                continue
            file = os.path.join(root, filename)
            filelist.append(file)
            count = count + 1
    return count;


def getfile():
    file = filelist.pop(0)
    return file;


def hashit():
    file = getfile()
    hash = hashlib.md5(open(file, 'rb').read()).hexdigest()
    dict.update({file: hash})


if __name__ == '__main__':
    filewalk(args.root_path)
    while len(filelist) is not 0:
        for x in filelist:
            hashit()
    print 'dict size:', len(dict), 'filelist size:', len(filelist)

