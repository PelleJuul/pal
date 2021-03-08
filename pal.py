#!/usr/bin/env python3

import sys
import os
import shutil

palPath = r"{{palPath}}"

def printUsage():
    print("Usage: pal [-h] command\n")
    print("Quickly create new pal projects.\n")
    print("Available commands:")
    print("  new        Create a new pal project in the current directory.")
    print("  help       Print this help message.")
    print("  install    Install pal on your system.")
    print("  update     Update to the latest pal library sources (on this machine).")
    print()
    print("Optional arguments:")
    print("  -h         Print this help message.")

def copyPalFilesToCurrentDir(files):
    overwriteAll = False

    for file in files:
        print(f'Copying {os.path.join(palPath, file)} to {file}')
        source = os.path.join(palPath, file)
        dest = file

        if os.path.exists(file):
            overwrite = overwriteAll

            if not overwriteAll:
                while True:
                    answer = input(f'File {file} already present, do you want to overwrite it? [(y)es, (n)o overwrite, yes to (a)ll] ')

                    if len(answer) == 1:
                        if answer == 'y':
                            overwrite = True
                            break
                        elif answer == 'n':
                            overwrite = False
                            break
                        elif answer == 'a':
                            overwrite = True
                            overwriteAll = True
                            break
                    
                    print('Please answer y, n or a')


            if overwrite:
                if os.path.isdir(file):
                    shutil.rmtree(file)
                else:
                    os.remove(file)
        
        if os.path.isdir(source):
            shutil.copytree(source, dest)
        else:
            shutil.copy(source, dest)

if len(sys.argv) < 2:
    print("Error: expected a command.")
    printUsage()
    exit()

if sys.argv[1] == '-h' or sys.argv[1] == 'help':
    printUsage()

elif sys.argv[1] == "new":
    installFiles = ["main.cpp", "makefile", "pal", "pal.sln", "pal.vcxproj", "pal.vcxproj.filters", "pal.vcxproj.user", "windows"]
    copyPalFilesToCurrentDir(installFiles)

elif sys.argv[1] == "update":
    installFiles = ["makefile", "pal"]

    answer = input("Updating pal will overwrite the pal/ sources and makefile. Proceed? [y/n]: ")

    if (answer.lower() == "y"):
        copyPalFilesToCurrentDir(installFiles)
    else:
        print("Update cancelled.")

elif sys.argv[1] == "install":
    f = open('pal.py', 'r')
    text = f.read()
    f.close()

    installationPath = os.path.join(os.getcwd(), 'installation')

    text = text.replace("{{" + "palPath" + "}}", os.getcwd())

    if os.path.exists('installation'):
        shutil.rmtree('installation')

    os.mkdir('installation')

    f = open(os.path.join('installation', 'pal.py'), 'w')
    f.write(text)
    f.close()

    f = open(os.path.join('installation', 'pal.bat'), 'w')
    f.write(f"python {installationPath}\\pal.py %*")
    f.close()

    print("To finish installation add the following to you Path environment vairable:")
    print(installationPath)


elif sys.argv[1] == "example":
    if (len(sys.argv) < 3):
        print("Usage: pal example <example name>")
        exit(1)

    installFiles = ["makefile", "pal"]

    exampleName = sys.argv[2]
    exampleFolder = os.path.join(palPath, "examples", exampleName)

    if not os.path.exists(exampleFolder):
        print(f"Error: could not find the example {exampleName}. Please make sure that you have spelled the name correctly with correct capitalization. See {os.path.join(palPath, 'examples')} for available examples.")
        exit(1)
    
    exampleFilesFilePath = os.path.join(exampleFolder, "examplefiles")

    if not os.path.exists(exampleFilesFilePath):
        print(f"Error: could not find the 'examplefiles' file in {exampleName}. The example is broken. Please report this issue on GitHub.")
        exit(1)
    
    exampleFilesFile = open(exampleFilesFilePath, 'r')
    exampleFiles = exampleFilesFile.readlines()
    exampleFilesFile.close()

    copyPalFilesToCurrentDir(installFiles)

    for file in exampleFiles:
        file = file.strip()

        if file.startswith("#"):
            continue

        if file == "":
            continue

        path = os.path.join(exampleFolder, file)

        if not os.path.exists(path):
            print(f"Error: could not find the file '{path}' specified in '{exampleFilesFilePath}.")
            exit(1)

        print(f'Copying {path} to {file}')
        os.system(f'cp -r {path} {file}')
else:
    print(f"Error: unrecognized command {sys.argv[1]}.")
    printUsage()