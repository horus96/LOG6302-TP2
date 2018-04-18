import sys
import xml.etree.cElementTree as ET
from lxml import etree
import re
import os



name_fun=sys.argv[1]


numero= 0

def copydefuse(sourcenode,targetnode):
    for defnode in sourcenode.findall(".def"):
        cdef = etree.SubElement(targetnode,"def")
        cdef.set("id",defnode.attrib.get("id"))
    for usenode in sourcenode.findall(".use"):
        cuse = etree.SubElement(targetnode,"use")
        cuse.set("id",usenode.attrib.get("id"))



# test
cOutFile = open('textFiles/cleancfg.xml', 'wb')

alias=dict()

tree = ET.parse('textFiles/dumpedcfg.xml')

root = tree.getroot()
croot = etree.Element("projet")



edgelist=[]
for classe in root:
    for method in classe.findall(".function"):

        for bloc in method:
            isNull=False


            if bloc.tag == "bloc":


                name = bloc.attrib.get("name")
                # car = [",", "-", "?", "'", "[", "]", "(", ")", "{", "}", "$", " ", "<", ">", "/", ".", ":", ";"]
                # namebis = ''.join(['_' if i in car else i for i in name])
                hasssa = False
                if name.__contains__(name_fun):
                    phis = []
                    pis = []
                    if len(bloc.findall('ssa'))>0 or len(bloc.findall('phis'))>0 or len(bloc.findall('pis'))>0 or len(bloc.findall('edge'))>1 or name.__contains__('entry') or name.__contains__('exit'):
                        cbloc = etree.SubElement(croot,"bloc")
                        cbloc.set("name",name)
                        cbloc.set("id",str(numero))
                        numero+=1

                        for phisorpis in bloc:
                            if phisorpis.tag == "phis":
                                for phisinstr in phisorpis:
                                    cphiinstr = etree.SubElement(cbloc,"phiinstr")
                                    cphiinstr.set("instruction",phisinstr.attrib.get("instruction"))
                                    copydefuse(phisinstr,cphiinstr)
                            if phisorpis.tag == "pis":
                                for pisinstr in phisorpis:
                                    cpiinstr = etree.SubElement(cbloc,"piinstr")
                                    cpiinstr.set("instruction",pisinstr.attrib.get("instruction"))
                                    copydefuse(pisinstr,cpiinstr)
                        for ssa in bloc.findall(".ssa"):
                            #outFile.write(namebis + "[\n label=\"{")
                            instr = ssa.attrib.get("instruction")
                            # instrbis=''.join(['_' if i in car else i for i in instr ])
                            #outFile.write(instr.replace('@', '').replace('<', '').replace('>', ''))
                            cinstr = etree.SubElement(cbloc,"ssa")
                            cinstr.set("instruction", instr)
                            copydefuse(ssa,cinstr)

                            #outFile.write("|def:")

                            hasssa = True

                            # addbloc
                        if (name.__contains__("entry")):

                            cparameter = etree.SubElement(cbloc,"parameter")

                            for param in method.findall('.parameter'):
                                cdef = etree.SubElement(cparameter,"def")
                                cdef.set("id",str(param.attrib.get("id")))


                            cconst = etree.SubElement(cbloc,"constant")
                            for const in method.findall('.constant'):
                                cdef = etree.SubElement(cconst,"def")
                                cdef.set("id",str(const.attrib.get("id")))
                                cdef.set("value",str(const.attrib.get("value")))
                    else:
                        alias[name]=bloc.findall(".edge")[0].attrib.get("target")

                        isNull=True

                    for edge in bloc.findall('.edge'):
                        if not(isNull):
                            nametarget = edge.attrib.get("target")
                            if nametarget.__contains__(name_fun):
                                edgelist.append((name, nametarget))

for edge in edgelist:
    target=edge[1]
    while target in alias:
        target=alias[target]
    for cbloc in croot:
        if cbloc.attrib.get("name")==edge[0]:
            vsource=cbloc
    cedge=etree.SubElement(vsource,"edge")
    cedge.set("target",target)








cOutFile.write(etree.tostring(croot, pretty_print=True))
