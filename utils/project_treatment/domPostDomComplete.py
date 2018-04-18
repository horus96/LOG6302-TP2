import sys
import xml.etree.cElementTree as ET
import re
import os
from lxml import etree
import sets as s
numero=0






outFile = open('textFiles/dompostdom.xml', 'wb')

tree = ET.parse('textFiles/cfgintra.xml')

root = tree.getroot()

croot = etree.Element("projet")



for method in root:
    print("computing dominators in "+method.attrib.get("name"))
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
    cmethod=etree.SubElement(croot,"method")
    cmethod.set("name",method.attrib.get("name"))
    for bloc in method:
        nodemap[bloc.attrib.get("name")]=bloc.attrib.get("id")
        nodeSet.add(bloc.attrib.get("id"))
        dom[bloc.attrib.get("id")]=set([])
        postdom[bloc.attrib.get("id")]=set([])
        idom[bloc.attrib.get("id")]=set([])
        ipostdom[bloc.attrib.get("id")]=set([])
        initDom[bloc.attrib.get("id")]=set([])
        initPostdom[bloc.attrib.get("id")]=set([])


    for ssa in method.findall(".ssa"):
        parents[ssa.attrib.get("id")]=set([])
        enfants[ssa.attrib.get("id")]=set([])

        dom[ssa.attrib.get("id")]|=nodeSet
        postdom[ssa.attrib.get("id")]|=nodeSet

    for ssa in method.findall(".phissa"):
        parents[ssa.attrib.get("id")]=set([])
        enfants[ssa.attrib.get("id")]=set([])

        dom[ssa.attrib.get("id")]|=nodeSet
        postdom[ssa.attrib.get("id")]|=nodeSet

    for ssa in method.findall(".pissa"):
        parents[ssa.attrib.get("id")]=set([])
        enfants[ssa.attrib.get("id")]=set([])

        dom[ssa.attrib.get("id")]|=nodeSet
        postdom[ssa.attrib.get("id")]|=nodeSet

    for nossa in method.findall(".nossa"):
        parents[nossa.attrib.get("id")]=set([])
        enfants[nossa.attrib.get("id")]=set([])
        if nossa.attrib.get("name").__contains__("entry"):
            dom[nossa.attrib.get("id")]=set([nossa.attrib.get("id")])
            postdom[nossa.attrib.get("id")]|=nodeSet
        elif nossa.attrib.get("name").__contains__("exit"):
            dom[nossa.attrib.get("id")]|=nodeSet
            postdom[nossa.attrib.get("id")]=set([nossa.attrib.get("id")])

    for bloc in method:

        for child in bloc.findall(".edge"):
            if (not child.attrib.get("target").__contains__("exit")) or (len(bloc.findall(".ssa"))>0 and bloc.findall(".ssa")[0].attrib.get("instruction").__contains__("return")) :
                parents[child.attrib.get("target")].add(bloc.attrib.get("id"))
                enfants[bloc.attrib.get("id")].add(child.attrib.get("target"))



    #analyse du point fixe
    finish=False
    while not finish:
        for el in nodeSet:
            initDom[el]=set([])|dom[el]
        for el in nodeSet:
            initPostdom[el]=set([])|postdom[el]
        for bloc in method:

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

        idom[i]|=dom[i]
        for j in dom[i]:
            idom[i]-=dom[j]
        ipostdom[i]|=postdom[i]
        for j in postdom[i]:
            ipostdom[i]-=postdom[j]





    for i in nodeSet:
        cnode=etree.SubElement(cmethod,"node")
        cnode.set("id",i)


    for i in nodeSet:
        for j in idom[i]:
            for cnode in cmethod:
                if cnode.attrib.get("id")==i:
                    cidom=etree.SubElement(cnode,"idom")
                    cidom.set("id",j)

    for i in nodeSet:
        for j in ipostdom[i]:
            for cnode in cmethod:
                if cnode.attrib.get("id")==i:
                    cipostdom=etree.SubElement(cnode,"ipostdom")
                    cipostdom.set("id",j)


outFile.write(etree.tostring(croot, pretty_print=True))
outFile.close()
