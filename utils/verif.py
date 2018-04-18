import xml.etree.cElementTree as ET
import re
import os
from sets import *


deflist=[]
uselist=[]

tree = ET.parse('cleancfg.xml')
root = tree.getroot()


[bloc for bloc in root if bloc.attrib.get("name").__contains__("entry")]

for bloc in root:
    for instr in bloc:
        if instr.tag!="edge":
            for defvar in instr.findall(".def"):
                deflist.append(defvar.attrib.get("id"))
            for usevar in instr.findall(".use"):
                uselist.append(usevar.attrib.get("id"))

print(set(uselist)-set(deflist)==set([]))
