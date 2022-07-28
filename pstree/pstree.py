#!/usr/bin/env python3

import sys
import os
import psutil

class Pstree():

    def __init__(self):
        self.callback = sys.stdout.write
        self.processcount = 0

    def print(self, printpid = False, callback=sys.stdout.write):
        self.printpid = printpid
        initprocess = psutil.Process(1)
        message = str(initprocess.pid) + ' ' if self.printpid else ''
        message += initprocess.name()
        self.callback(message + '-|')
        self.processcount += 1
        self.printallprocess(initprocess, ' '*len(message) + ' ')

    def printallprocess(self, parentprocess, indent):
        count = 0
        if self.processcount > self.maxprintcount:
            return
        for childprocess in parentprocess.children():
            name = childprocess.name()
            if count == 0:
                if self.processcount == 1: message = '-' + name
                else:
                    message = '----'
                    message += str(childprocess.pid) + ' ' if self.printpid else '' 
                    message += name
                count += 1
            elif count > 0:
                message = '\n'
                message += indent + '|-'
                message += str(childprocess.pid) + ' ' if self.printpid else ''
                message += name
                count += 1
            self.callback(message)
            self.processcount += 1
            self.printallprocess(childprocess, indent + ' '*len(name) + '    ')


if __name__ == '__main__':
    pstree = Pstree()
    pstree.maxprintcount = float('inf')
    pstree.print()
