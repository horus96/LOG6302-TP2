import xml.etree.cElementTree as ET
import re
import os


outFile = open('cfg.dot', 'wb')
outFile.write("digraph G{\n")
#outFile.write("graph [splines=ortho, nodesep=2]\n")
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

tree = ET.parse('doc.xml')
root=tree.getroot()

for method in root:

    for bloc in method:
        name=bloc.attrib.get("name")
        car = [",","-","?","'","[","]","(",")","{","}","$"," ","<",">","/",".",":",";"]
        namebis=''.join(['_' if i in car else i for i in name ])
        hasssa=False

        if namebis.__contains__("wordcount"):
            for ssa in bloc:

                if ssa.tag=="ssa":
                    outFile.write(namebis+"[\n label=\"{")
                    instr=ssa.attrib.get("instruction")
                    #instrbis=''.join(['_' if i in car else i for i in instr ])
                    outFile.write(instr.replace('@','').replace('<','').replace('>',''))
                    outFile.write("|def:")
                    usee=[]
                    deff=[]
                    for useordef in ssa:
                        if useordef.tag=="def":
                            deff.append(int(useordef.attrib.get("id")))
                        if useordef.tag=="use":
                            usee.append(int(useordef.attrib.get("id")))
                    outFile.write(str(deff))
                    outFile.write("|use:")
                    outFile.write(str(usee))
                    outFile.write("}\"\n]\n")
                    hasssa=True

                #addbloc
            if(not hasssa):

                outFile.write(namebis+"[\n label=\"{")
                if(namebis.__contains__("entry")):
                    outFile.write("entry")
                elif(namebis.__contains__("exit")):
                    outFile.write("exit")
                else :
                    outFile.write("no_ssa")
                outFile.write("}\"\n]\n")





            for edge in bloc:
                if edge.tag=="edge":
                    nametarget=edge.attrib.get("target")
                    nametargetbis=''.join(['_' if i in car else i for i in nametarget ])
                    #addedge
                    if nametargetbis.__contains__("wordcount"):
                        outFile.write(namebis)
                        outFile.write("->")
                        outFile.write(nametargetbis)
                        outFile.write("\n")
outFile.write("}\n")
