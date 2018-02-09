#!/usr/bin/env python3

import subprocess
import sys

if len(sys.argv) <= 1:
    print("You must specify a jar file or a bin folder container the generated class files")
    exit(-1)

template = open("baseScopeFile.conf", "r")
scope = open("scopeFile.conf", "w")
for line in template:
    scope.write(line)

baseFolderLine = "Application,Java,binaryDir,"
baseJarLine = "Application,Java,jarFile,"

for target in sys.argv[1:]:
    if target.endswith(".jar"):
        scope.write(baseJarLine + target + "\n")
    else:
        scope.write(baseFolderLine + target + "\n")

template.close()
scope.close()

gradle_cmd_args = ["gradle", "execute"]
subprocess.call(gradle_cmd_args)
