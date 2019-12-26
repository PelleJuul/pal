#!/usr/bin/env python3

import sys
import os
import shutil

# Location of the pal source files. Will be changed when running `pal install`
# should not be changed manually.
codeLocation = '{{codeLocation}}'

# name of the directory where pal will put prebuilt object files.
objectsDir = 'objects'

# The source files for all of pal, excluding ImGui sources.
palCppFiles = ['gain.cpp', 'gui.cpp', 'realtime.cpp', 'scope.cpp', 'sinosc.cpp', 'utils.cpp']

def shell(command):
    exitCode = os.system(command)

    if (exitCode != 0):
        raise ChildProcessError(f'Command `{command}` finished with exit code {exitCode}')

def main():
    global codeLocation

    if not os.path.isdir(codeLocation):
        codeLocation = '.'

    command = 'help'
    
    if len(sys.argv) > 1:
        command = sys.argv[1]

    if command == 'install':  
        install(sys.argv[2:])
    elif command == 'build':
        build(sys.argv[2:])
    elif command == 'run':
        print('Running', sys.argv[2:])
    elif command == 'new':
        new(sys.argv[2:])
    elif command == 'help':
        printHelp();
    else:
        print(f'Unrecognized command \'{command}\'. See `pal help`.\n')

def install(args):
    cwd = os.getcwd()

    prefix = '/usr/local/bin/'
    source = os.path.join(cwd, 'pal.py')
    target = os.path.join(prefix, 'pal')

    f = open(source, 'r')
    text = f.read()
    f.close()

    cl = '{{' + 'codeLocation' + '}}'
    text = text.replace(cl, cwd)

    debug = 'debug' in args

    installBuildObjects(debug)

    if not '--dry-run' in args:
        f = open(target, 'w')
        f.write(text)
        f.close()

        shell(f'chmod +x {target}')
        print(f'pal installed to {target}')
    else:
        pass

def installBuildObjects(debug = False):
    print('Building object files')

    if not os.path.isdir('objects'):
        os.mkdir('objects')

    imguiCppFiles = [os.path.join('imgui', f) for f in os.listdir('imgui') if os.path.isfile(os.path.join('imgui', f)) and f.endswith('.cpp')]
    cppFiles = imguiCppFiles + palCppFiles;

    flags = ['-I /usr/local/include/SDL2', '-I .', '-I imgui', '-std=c++11']

    if (debug):
        flags.append('-g');

    flagString = ' '.join(flags);

    for cppFile in cppFiles:
        target = os.path.join('objects', os.path.basename(cppFile) + '.o')
        buildCommand = f'c++ {flagString} -c {cppFile} -o {target}'
        
        print(buildCommand)
        shell(buildCommand)  

def getBuildCommand(source, target):
    return f'c++ -I /usr/local/include/SDL2 -I imgui -std=c++11 -c {source} -o {target}' 

def build(args):
    # Check if the file contains a build comment
    if len(args) == 1 and os.path.isfile(args[0]):
        with open(args[0], 'r') as f:
            for line in f.readlines():
                if line.startswith("// pal build"):
                    cmd = line.replace('// ', '')
                    print(f'Running build comment.')
                    shell(cmd)
                    return

    libs = ['-lSDL2', '-lportaudio', '-framework OpenGl']
    includes = ['-I', os.path.join(codeLocation, 'imgui'), f'-I {codeLocation}', '-I /usr/local/include/SDL2']
    flags = ['-std=c++11']
    objects = os.path.join(codeLocation, 'objects', '*.o')

    if not '-o' in args:
        files = [s for s in args if s.endswith('.cpp')]

        if len(files) > 0:
            args = args + ['-o', files[0].replace('.cpp', '')]
        else:
            error('Could not figure out how to proceed with build. No .cpp files given.')

    flagString = ' '.join(libs + includes + flags + [objects] + args)

    buildCommand = f'c++ {flagString}'

    print(buildCommand)
    shell(f'c++ {flagString}')

def new(args):
    filename = "main.cpp"

    if len(args) >= 1:
        filename = args[0]

        if not filename.endswith(".cpp"):
            filename = filename + ".cpp"

    shutil.copyfile(os.path.join(codeLocation, 'templates/template.cpp'), filename)
    print(f'Generated {filename}')

def printHelp():
    print('Usage: pal [command] <args>')

def error(str):
    print(f'Error: {str}')
    quit(1)

if __name__ == "__main__":
    main() 