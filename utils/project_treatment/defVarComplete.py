import xml.etree.cElementTree as ET
import re
import os
import sys
from lxml import etree
import sets as s
numero=0



# test
outFile = open('textFiles/defVar.xml', 'wb')



tree = ET.parse('textFiles/cfgintra.xml')
root = tree.getroot()
croot = etree.Element("projet")


for method in root:
    print("computing live variables analysis in "+method.attrib.get("name"))
    cmethod=etree.SubElement(croot,"method")
    cmethod.set("name",method.attrib.get("name"))

    finish = False

    inVar=dict()
    outVar=dict()
    genVar=dict()
    killVar=dict()
    parents=dict()
    nodemap=dict()

    for ssa in method:
        parents[ssa.attrib.get("id")]=set([])
        nodemap[ssa]=ssa.attrib.get("id")

    for ssa in method:

        inVar[ssa.attrib.get("id")]=set([])
        outVar[ssa.attrib.get("id")]=set([])
        genVar[ssa.attrib.get("id")]=set([])
        killVar[ssa.attrib.get("id")]=set([])
        if (ssa.attrib.get("instruction").__contains__("putfield")):
            if len(ssa.attrib.get("instruction").split(','))>2:

                field=ssa.attrib.get("instruction").split(',')[2].replace(' ','')
                genVar[ssa.attrib.get("id")].add(field)
        for child in ssa.findall(".edge"):
            parents[child.attrib.get("target")].add(ssa.attrib.get("id"))


    for bloc in method:
        for bloc2 in method:
            if len(genVar[bloc.attrib.get("id")] & genVar[bloc2.attrib.get("id")])>0 and bloc!=bloc2 :
                killVar[bloc.attrib.get("id")].add(bloc2.attrib.get("id"))


    #analyse du point fixe
    while not finish :
        inVarInit=inVar.copy()
        for bloc in method:
            inVar[bloc.attrib.get("id")]=set([])
            for par in parents[bloc.attrib.get("id")]:
                inVar[bloc.attrib.get("id")]|=outVar[par]
            outVar[bloc.attrib.get("id")]=inVar[bloc.attrib.get("id")].copy()
            if len(genVar[bloc.attrib.get("id")])>0:
                outVar[bloc.attrib.get("id")].add(bloc.attrib.get("id"))
                outVar[bloc.attrib.get("id")]-=killVar[bloc.attrib.get("id")]

        finish = inVarInit==inVar






    alias=dict()

    numero=0

    edgelist=[]



    for bloc in method:
        cbloc=etree.SubElement(croot,bloc.tag)
        cbloc.set("id",bloc.attrib.get("id"))

        isNull=False





        ckill=etree.SubElement(cbloc,"kill")
        for i in sorted(list(killVar[bloc.attrib.get("id")])):
            cnode=etree.SubElement(ckill,"node")
            cnode.set("id",i)

        cgen=etree.SubElement(cbloc,"gen")
        for i in sorted(list(genVar[bloc.attrib.get("id")])):
            cnode=etree.SubElement(cgen,"node")
            cnode.set("id",i)


        cin=etree.SubElement(cbloc,"live_in")
        for i in sorted(list(inVar[bloc.attrib.get("id")])):
            cnode=etree.SubElement(cin,"node")
            cnode.set("id",i)


        cout=etree.SubElement(cbloc,"live_out")
        for i in sorted(list(outVar[bloc.attrib.get("id")])):
            cnode=etree.SubElement(cout,"node")
            cnode.set("id",i)

        numero+=1






outFile.write(etree.tostring(croot, pretty_print=True))



