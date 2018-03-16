import xml.etree.cElementTree as ET
import re
import os
numero=0

# test
outFile = open('newcfg.dot', 'wb')
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

tree = ET.parse('cleancfg.xml')
root = tree.getroot()

edgelist=[]



for bloc in root:
    isNull=False


    if bloc.tag == "bloc":
        name = bloc.attrib.get("name")
        car = [",", "-", "?", "'", "[", "]", "(", ")", "{", "}", "$", " ", "<", ">", "/", ".", ":", ";"]
        namebis = ''.join(['_' if i in car else i for i in name])
        hasssa = False
        if namebis.__contains__("wordcount"):
            phis = []
            pis = []
            for phisorpis in bloc:
                if phisorpis.tag == "phiinstr":
                    phis.append(phisorpis.attrib.get("instruction"))
                if phisorpis.tag == "piinstr":
                    pis.append(phisorpis.attrib.get("instruction"))

            for ssa in bloc:
                if ssa.tag == "ssa":
                    outFile.write(namebis + "[\n label=\"{")
                    outFile.write("Node : ")
                    outFile.write(str(numero))
                    outFile.write("|")
                    numero+=1
                    instr = ssa.attrib.get("instruction")
                    # instrbis=''.join(['_' if i in car else i for i in instr ])
                    outFile.write(instr.replace('@', '').replace('<', '').replace('>', ''))
                    outFile.write("|def:")
                    usee = []
                    deff = []
                    for useordef in ssa:
                        if useordef.tag == "def":
                            deff.append(int(useordef.attrib.get("id")))
                        if useordef.tag == "use":
                            usee.append(int(useordef.attrib.get("id")))
                    outFile.write(str(deff))
                    outFile.write("|use:")
                    outFile.write(str(usee))
                    if phis != []:
                        outFile.write("|")
                        for phiinstr in phis:
                            outFile.write(phiinstr)
                            outFile.write("\l")
                    if pis != []:
                        outFile.write("|")
                        for piinstr in pis:
                            outFile.write(piinstr)
                            outFile.write("\l")
                    outFile.write("}\"\n]\n")
                    hasssa = True

                # addbloc
            if (not hasssa):


                if (namebis.__contains__("entry")):
                    outFile.write(namebis + "[\n label=\"{")
                    outFile.write("Node : ")
                    outFile.write(str(numero))
                    outFile.write("|")
                    numero+=1
                    outFile.write("entry")
                    outFile.write("|")
                    outFile.write("parameters:\l")
                    for param in bloc:
                        if param.tag=="parameter":
                            for d in param:
                                outFile.write(str(d.attrib.get("id"))+"\l")

                    outFile.write("|")
                    outFile.write("constants:\l")
                    for constant in bloc:
                        if constant.tag=="constant":
                            for d in constant:
                                outFile.write(str(d.attrib.get("id"))+"="+str(d.attrib.get("value"))+"\l")

                    if phis != []:
                        outFile.write("|")
                        for phiinstr in phis:
                            outFile.write(phiinstr)
                            outFile.write("\l")
                    if pis != []:
                        outFile.write("|")
                        for piinstr in pis:
                            outFile.write(piinstr)
                            outFile.write("\l")
                    outFile.write("}\"\n]\n")



                elif (namebis.__contains__("exit")):
                    outFile.write(namebis + "[\n label=\"{")
                    outFile.write("Node : ")
                    outFile.write(str(numero))
                    outFile.write("|")
                    numero+=1
                    outFile.write("exit")

                    if phis != []:
                        outFile.write("|")
                        for phiinstr in phis:
                            outFile.write(phiinstr)
                            outFile.write("\l")
                    if pis != []:
                        outFile.write("|")
                        for piinstr in pis:
                            outFile.write(piinstr)
                            outFile.write("\l")
                    outFile.write("}\"\n]\n")

                else:
                    if phis!=[] or pis!=[] or len(bloc.findall(".edge"))>1:
                        outFile.write(namebis + "[\n label=\"{")
                        outFile.write("Node : ")
                        outFile.write(str(numero))
                        outFile.write("|")
                        numero+=1
                        outFile.write("no_ssa")
                        if phis != []:
                            outFile.write("|")
                            for phiinstr in phis:
                                outFile.write(phiinstr)
                                outFile.write("\l")
                        if pis != []:
                            outFile.write("|")
                            for piinstr in pis:
                                outFile.write(piinstr)
                                outFile.write("\l")
                        outFile.write("}\"\n]\n")
                    else:

                        newname=bloc.findall(".edge")[0].attrib.get("target")
                        alias[namebis]=''.join(['_' if i in car else i for i in newname])
                        isNull=True

            for edge in bloc:
                if edge.tag == "edge" and not(isNull):
                    nametarget = edge.attrib.get("target")
                    nametargetbis = ''.join(['_' if i in car else i for i in nametarget])
                    if nametargetbis.__contains__("wordcount"):
                        outFile.write(namebis)
                        outFile.write("->")
                        outFile.write(nametargetbis)
                        outFile.write("\n")
                        edgelist.append((namebis, nametargetbis))






outFile.write("}\n")
