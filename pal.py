#!/usr/bin/env python

import sys
import os

palPath = "{{palPath}}";

def printUsage():
    print("Usage: pal [-h] command\n")
    print("Quickly create new pal projects.\n")
    print("Available commands:")
    print("  new        Create a new pal project in the current directory.")
    print()
    print("Optional arguments:")
    print("  -h         Print this help message.")

if "-h" in sys.argv:
    printUsage

if "new" in sys.argv:
    installFiles = ["main.cpp", "makefile", "pal"]
    
    for file in installFiles:
        print(f'Copying {palPath}/{file} to {file}')
        os.system(f'cp -r {palPath}/{file} {file}')

else:
    printUsage()