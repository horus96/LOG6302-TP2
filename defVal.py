import xml.etree.cElementTree as ET
import re
import os
import sets as s
numero=0

# test
outFile = open('defVar.dot', 'wb')
outFiletxt = open('defVar.txt', 'wb')

tree = ET.parse('cleancfg.xml')
root = tree.getroot()



finish = False

inVar=dict()
outVar=dict()
genVar=dict()
killVar=dict()
parents=dict()
nodemap=dict()

for bloc in root:
    parents[bloc.attrib.get("id")]=set([])
    nodemap[bloc.attrib.get("name")]=bloc.attrib.get("id")

for bloc in root:

    inVar[bloc.attrib.get("id")]=set([])
    outVar[bloc.attrib.get("id")]=set([])
    genVar[bloc.attrib.get("id")]=set([])
    killVar[bloc.attrib.get("id")]=set([])
    if len(bloc.findall('.ssa'))>0 and bloc.findall('.ssa')[0].attrib.get("instruction").__contains__("putfield"):
        if len(bloc.findall('.ssa')[0].attrib.get("instruction").split(','))>2:

            field=bloc.findall('.ssa')[0].attrib.get("instruction").split(',')[2].replace(' ','')
            genVar[bloc.attrib.get("id")].add(field)
    for child in bloc.findall(".edge"):
        parents[nodemap[child.attrib.get("target")]].add(bloc.attrib.get("id"))


for bloc in root:
    for bloc2 in root:
        if len(genVar[bloc.attrib.get("id")] & genVar[bloc2.attrib.get("id")])>0 and bloc!=bloc2 :
            killVar[bloc.attrib.get("id")].add(bloc2.attrib.get("id"))

while not finish :
    inVarInit=inVar.copy()
    for bloc in root:
        bloc.attrib.get("name")
        inVar[bloc.attrib.get("id")]=set([])
        for par in parents[bloc.attrib.get("id")]:
            inVar[bloc.attrib.get("id")]|=outVar[par]
        outVar[bloc.attrib.get("id")]=inVar[bloc.attrib.get("id")].copy()
        if len(genVar[bloc.attrib.get("id")])>0:
            outVar[bloc.attrib.get("id")].add(bloc.attrib.get("id"))
            outVar[bloc.attrib.get("id")]-=killVar[bloc.attrib.get("id")]

    finish = inVarInit==inVar





outFile.write("digraph G{\n")
# outFile.write("graph [splines=ortho, nodesep=2]\n")
outFile.write("fontname = \"Bitstream Vera Sans\"\n")
outFile.write("fontname = \"Bitstream Vera Sans\"\n")
outFile.write("fontsize = 8\n")
outFile.write("node [\n")
outFile.write("fontname = \"Bitstream Vera Sans\"\n")
outFile.write("fontsize = 8\n")
outFile.write("shape = \"record\"\n")
outFile.write("]\n")
outFile.write("edge [\n")
outFile.write("fontname = \"Bitstream Vera Sans\"\n")
outFile.write("fontsize = 8\n")
outFile.write("]\n")
alias=dict()

numero=0

edgelist=[]



for bloc in root:
    isNull=False


    if bloc.tag == "bloc":
        name = bloc.attrib.get("name")
        car = [",", "-", "?", "'", "[", "]", "(", ")", "{", "}", "$", " ", "<", ">", "/", ".", ":", ";"]
        namebis = ''.join(['_' if i in car else i for i in name])

        outFile.write(namebis + "[\n label=\"{")
        outFile.write("Node : ")
        outFile.write(bloc.attrib.get("id"))
        outFiletxt.write("\n\nNode : ")
        outFiletxt.write(bloc.attrib.get("id"))
        outFile.write("| Kill :")
        outFiletxt.write("\n Kill :")
        for i in sorted(list(killVar[bloc.attrib.get("id")])):
            outFile.write(i)
            outFile.write(", ")
            outFiletxt.write(i)
            outFiletxt.write(", ")

        outFile.write("| Gen :")
        outFiletxt.write("\n Gen :")
        for i in sorted(list(genVar[bloc.attrib.get("id")])):
            outFile.write(i)
            outFile.write(", ")
            outFiletxt.write(i)
            outFiletxt.write(", ")

        outFile.write("| In :")
        outFiletxt.write("\n In :")
        for i in sorted(list(inVar[bloc.attrib.get("id")])):
            outFile.write(i)
            outFile.write(", ")
            outFiletxt.write(i)
            outFiletxt.write(", ")

        outFile.write("| Out :")
        outFiletxt.write("\n Out :")
        for i in sorted(list(outVar[bloc.attrib.get("id")])):
            outFile.write(i)
            outFile.write(", ")
            outFiletxt.write(i)
            outFiletxt.write(", ")

        numero+=1
        outFile.write("}\"\n]\n")

        for edge in bloc:
            if edge.tag == "edge" and not(isNull):
                nametarget = edge.attrib.get("target")
                nametargetbis = ''.join(['_' if i in car else i for i in nametarget])
                if nametargetbis.__contains__("wordcount") and (not nametargetbis.__contains__("exit") or bloc.findall(".ssa")[0].attrib.get("instruction").__contains__("return")):
                    outFile.write(namebis)
                    outFile.write("->")
                    outFile.write(nametargetbis)
                    outFile.write("\n")
                    edgelist.append((namebis, nametargetbis))






outFile.write("}\n")
