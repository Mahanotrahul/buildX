#!/usr/bin/env python3

import sys
import os
import argparse

BUF_SIZE = 1024

class cp():

    def __init__(self, args):
        self.args = args
        self.recursive = args.recursive

    def copy(self, source, target):
        if os.path.isdir(source):
            if self.recursive == False:
                print("-r not specified. omitting directory {}".format(source))
            else:
                self.copydirs(source, target)
        else:
            self.copyfile(source, target)

    def checkfileValidity(self, filename):
        if os.path.isdir(filename):
            raise TypeError("{} is a dir. Provide -r to copy dirs".format(filename))

        if os.path.isfile(filename) == False:
            return False

        if os.path.exists(filename) == False:
            return False
        
        if os.access(filename, mode = os.R_OK) == False:
            raise TypeError("Permission denied while trying to read file {} ".format(filename))
            return False

    def checkdirValidity(self, dirs):
        for dir in dirs:
            if os.path.isdir(dir) == False:
                raise TypeError("Dir {} is not a valid dir".format(dir))
            if os.access(dir, mode = os.R_OK) == False:
                raise TypeError("Dir {} is not readable".format(dir))
                return False

    def copyfile(self, sourcefile, target):
        try:
            if self.checkfileValidity(sourcefile) == False:
                raise FileNotFoundError("Source File Doesnot exist")
        except Exception as e:
            print(e)
            return
        sf = open(sourcefile, 'r')
        tf = open(target, 'w')
        if os.path.isdir(target):       # if target is a dir, we need to copy sourcefile inside this targetdir
            tf = open(os.path.join(target, sourcefile), 'w')

        print(sourcefile, target)
        while True:
            bytes_read = sf.read(BUF_SIZE)
            if bytes_read == "":
                break
            tf.write(bytes_read)

    def copydirs(self, source, target):
        self.checkdirValidity([source])
        if os.path.exists(target) == False:     # creates targetdir if not already exists
            os.makedirs(target, mode=os.stat(source).st_mode)


        files_in_source_dir = os.listdir(source)
        target_ino = os.stat(target).st_ino
        for f in files_in_source_dir:       # checks if a dir is being copied onto itself to avoid recursion
            if os.stat(os.path.join(source, f)).st_ino == target_ino:
                raise RecursionError("target file is being copied inside or to a targetfile")
                return False
        
        for file in files_in_source_dir:
            if os.path.isdir(os.path.join(source, file)):
                if self.recursive == False:
                    print("-r is not specified. omitting dir {}".format(dir))
                else:
                    self.copydirs(os.path.join(source, '') + file, os.path.join(target, file))
            else:
                self.copyfile(os.path.join(source, file), os.path.join(target, file))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r','--recursive',help="specify -r to copy files inside a dir recursively", action="store_true")
    parser.add_argument('sourcefile', help="source file name or dir")
    parser.add_argument('targetfile', help="target file name or dir")
    args = parser.parse_args()

    cp = cp(args)
    cp.copy(args.sourcefile, args.targetfile)