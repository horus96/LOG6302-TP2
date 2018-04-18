import sys
import xml.etree.cElementTree as ET
from lxml import etree
import re
import os




numero= 0

def copydefuse(sourcenode,targetnode):
    for defnode in sourcenode.findall(".def"):
        cdef = etree.SubElement(targetnode,"def")
        cdef.set("id",defnode.attrib.get("id"))
    for usenode in sourcenode.findall(".use"):
        cuse = etree.SubElement(targetnode,"use")
        cuse.set("id",usenode.attrib.get("id"))



# test
cOutFile = open('textFiles/cfgintra.xml', 'wb')

alias=dict()

tree = ET.parse('textFiles/dumpedcfg.xml')

root = tree.getroot()
croot = etree.Element("projet")



#on parcourt les classes
for classe in root:
    print("computing class "+classe.attrib.get("name"))
    #on parcourt les methodes
    for method in classe.findall(".function"):
        #definition des elements propres a la methodes
        edgelist=[]
        blocToId=dict()
        idToInstr=dict()
        cmethod = etree.SubElement(croot, "method")
        cmethod.set("name",method.attrib.get("name"))

        #on copie le bloc
        for bloc in method:
            isNull=False


            if bloc.tag == "bloc":


                name = bloc.attrib.get("name")
                hasssa = False
                phis = []
                pis = []

                #on regarde si le bloc est utile
                if len(bloc.findall('ssa'))>0 or len(bloc.findall('phis'))>0 or len(bloc.findall('pis'))>0 or len(bloc.findall('edge'))>1 or name.__contains__('entry') or name.__contains__('exit'):
                    first = True

                    #on recherche toutes les instructions du bloc
                    for phisorpis in bloc:
                        if phisorpis.tag == "phis":
                            for phisinstr in phisorpis:

                                cphiinstr = etree.SubElement(cmethod,"phissa")
                                cphiinstr.set("instruction",phisinstr.attrib.get("instruction"))
                                cphiinstr.set("id",str(numero))
                                if(first):
                                    blocToId[name]=numero
                                copydefuse(phisinstr,cphiinstr)

                                if not(first):
                                    edgelist.append((str(numero-1),str(numero)))
                                first=False
                                blocToId[str(numero)]=numero
                                idToInstr[numero]=cphiinstr
                                numero+=1
                        if phisorpis.tag == "pis":
                            for pisinstr in phisorpis:

                                cpiinstr = etree.SubElement(cmethod,"pissa")
                                cpiinstr.set("instruction",pisinstr.attrib.get("instruction"))
                                cpiinstr.set("id",str(numero))
                                if(first):
                                    blocToId[name]=numero
                                copydefuse(pisinstr,cpiinstr)
                                if not(first):
                                    edgelist.append((str(numero-1),str(numero)))
                                first=False
                                blocToId[str(numero)]=numero
                                idToInstr[numero]=cpiinstr
                                numero+=1
                    for ssa in bloc.findall(".ssa"):
                        #outFile.write(namebis + "[\n label=\"{")
                        instr = ssa.attrib.get("instruction")
                        # instrbis=''.join(['_' if i in car else i for i in instr ])
                        #outFile.write(instr.replace('@', '').replace('<', '').replace('>', ''))
                        cinstr = etree.SubElement(cmethod,"ssa")
                        cinstr.set("instruction", instr)
                        cinstr.set("id",str(numero))
                        if(first):
                            blocToId[name]=numero
                        copydefuse(ssa,cinstr)
                        if not(first):
                            edgelist.append((str(numero-1),str(numero)))
                        first=False
                        blocToId[str(numero)]=numero
                        idToInstr[numero]=cinstr
                        numero+=1

                        #outFile.write("|def:")

                        hasssa = True

                    #si il n'y a pas d'instruction dans le bloc, on met un nossa
                    if(first):
                        blocToId[name]=numero
                        cbloc = etree.SubElement(cmethod,"nossa")
                        cbloc.set("name",name)
                        cbloc.set("instruction", "nossa")
                        cbloc.set("id",str(numero))
                        blocToId[str(numero)]=numero
                        numero+=1
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
                            cdef.set("value",const.attrib.get("value"))
                    if (name.__contains__("exit")):
                        exitNode=numero-1
                else:
                    #si le bloc est inutile, on le supprime et on redirige les arcs vers le suivant
                    alias[name]=bloc.findall(".edge")[0].attrib.get("target")
                    isNull=True


                #copie des arcs
                for edge in bloc.findall('.edge'):
                    if not(isNull):
                        nametarget = edge.attrib.get("target")
                        #on cherche les arcs intraproceduraux
                        if nametarget.__contains__(classe.attrib.get("name").split(',L')[1].split('>')[0]+"."+method.attrib.get("name").split(',')[2].split(' >')[0].split(' ')[1]) \
                            or (nametarget.__contains__(classe.attrib.get("name").split(',')[1].split('>')[0]+',')
                                and nametarget.__contains__(method.attrib.get("name").split(',')[2].split(' >')[0].split(' ')[1])):
                            edgelist.append((numero-1, nametarget))


        #ecriture des arcs sur le nouveau fichier
        for edge in edgelist:
            if not(edge[1].__contains__("exit")) or (edge[0] in idToInstr and idToInstr[edge[0]].attrib.get("instruction").__contains__("return")):
                target=edge[1]
                while target in alias:
                    target=alias[target]
                for cbloc in cmethod:
                    if cbloc.attrib.get("id")==str(edge[0]):
                        vsource=cbloc
                cedge=etree.SubElement(vsource,"edge")
                cedge.set("target",str(blocToId[target]))








cOutFile.write(etree.tostring(croot, pretty_print=True))
