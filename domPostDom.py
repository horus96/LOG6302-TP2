import xml.etree.cElementTree as ET
import re
import os
import sets as s
numero=0

# test
outFiled = open('dom.dot', 'wb')
outFilep = open('postdom.dot', 'wb')



tree = ET.parse('cleancfg.xml')
root = tree.getroot()

parents=dict()
enfants=dict()
dom=dict()
postdom=dict()
idom=dict()
ipostdom=dict()
nodemap=dict()
nodeSet=set([])
initDom=dict()
initPostdom=dict()

for bloc in root:
    nodemap[bloc.attrib.get("name")]=bloc.attrib.get("id")
    nodeSet.add(bloc.attrib.get("id"))
    dom[bloc.attrib.get("id")]=set([])
    postdom[bloc.attrib.get("id")]=set([])
    idom[bloc.attrib.get("id")]=set([])
    ipostdom[bloc.attrib.get("id")]=set([])
    initDom[bloc.attrib.get("id")]=set([])
    initPostdom[bloc.attrib.get("id")]=set([])


for bloc in root:
    parents[bloc.attrib.get("id")]=set([])
    enfants[bloc.attrib.get("id")]=set([])

    if bloc.attrib.get("name").__contains__("entry"):
        dom[bloc.attrib.get("id")]=set([bloc.attrib.get("id")])
        postdom[bloc.attrib.get("id")]|=nodeSet
    elif bloc.attrib.get("name").__contains__("exit"):
        dom[bloc.attrib.get("id")]|=nodeSet
        postdom[bloc.attrib.get("id")]=set([bloc.attrib.get("id")])
    else :
        dom[bloc.attrib.get("id")]|=nodeSet
        postdom[bloc.attrib.get("id")]|=nodeSet





for bloc in root:

    for child in bloc.findall(".edge"):
        if (not child.attrib.get("target").__contains__("exit")) or bloc.findall(".ssa")[0].attrib.get("instruction").__contains__("return") :
            parents[nodemap[child.attrib.get("target")]].add(bloc.attrib.get("id"))
            enfants[bloc.attrib.get("id")].add(nodemap[child.attrib.get("target")])


print(enfants)


finish=False
while not finish:
    for el in nodeSet:
        initDom[el]=set([])|dom[el]
    for el in nodeSet:
        initPostdom[el]=set([])|postdom[el]
    for bloc in root:




        if len(parents[bloc.attrib.get("id")])>0:
            for i in parents[bloc.attrib.get("id")]:
                dom[bloc.attrib.get("id")]&=dom[i]
        dom[bloc.attrib.get("id")].add(bloc.attrib.get("id"))

        if len(enfants[bloc.attrib.get("id")])>0:
            for i in enfants[bloc.attrib.get("id")]:
                postdom[bloc.attrib.get("id")]&=postdom[i]
        postdom[bloc.attrib.get("id")].add(bloc.attrib.get("id"))
    finish=(initDom==dom) and (initPostdom==postdom)



for i in nodeSet:
    postdom[i].remove(i)
    dom[i].remove(i)

for i in nodeSet:
    ipostdom[i]|=postdom[i]
    for j in postdom[i]:
        ipostdom[i]-=postdom[j]
    idom[i]|=dom[i]
    for j in dom[i]:
        idom[i]-=dom[j]

print(postdom)

print(dom)

print(ipostdom)

print(idom)

outFiled.write("digraph G{\n")
# outFile.write("graph [splines=ortho, nodesep=2]\n")
outFiled.write("fontname = \"Bitstream Vera Sans\"\n")
outFiled.write("fontname = \"Bitstream Vera Sans\"\n")
outFiled.write("fontsize = 8\n")
outFiled.write("node [\n")
outFiled.write("fontname = \"Bitstream Vera Sans\"\n")
outFiled.write("fontsize = 8\n")
outFiled.write("shape = \"circle\"\n")
outFiled.write("]\n")
outFiled.write("edge [\n")
outFiled.write("fontname = \"Bitstream Vera Sans\"\n")
outFiled.write("fontsize = 8\n")
outFiled.write("]\n")


for i in nodeSet:
    outFiled.write("[label=")
    outFiled.write(i)
    outFiled.write("]\n")

for i in nodeSet:
    for j in idom[i]:
        outFiled.write(i)
        outFiled.write("->")
        outFiled.write(j)
        outFiled.write("\n")
outFiled.write("}")



outFilep.write("digraph G{\n")
# outFile.write("graph [splines=ortho, nodesep=2]\n")
outFilep.write("fontname = \"Bitstream Vera Sans\"\n")
outFilep.write("fontname = \"Bitstream Vera Sans\"\n")
outFilep.write("fontsize = 8\n")
outFilep.write("node [\n")
outFilep.write("fontname = \"Bitstream Vera Sans\"\n")
outFilep.write("fontsize = 8\n")
outFilep.write("shape = \"circle\"\n")
outFilep.write("]\n")
outFilep.write("edge [\n")
outFilep.write("fontname = \"Bitstream Vera Sans\"\n")
outFilep.write("fontsize = 8\n")
outFilep.write("]\n")


for i in nodeSet:
    outFilep.write("[label=")
    outFilep.write(i)
    outFilep.write("]\n")

for i in nodeSet:
    for j in ipostdom[i]:
        outFilep.write(i)
        outFilep.write("->")
        outFilep.write(j)
        outFilep.write("\n")
outFilep.write("}")
