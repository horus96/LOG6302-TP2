import xml.etree.cElementTree as ET
import re
import os
import csv
import sets as s
from lxml import etree

numero=0

# test



cOutFile = open('textFiles/dependencies.xml', 'wb')

tree = ET.parse('textFiles/cfgintra.xml')
root = tree.getroot()
croot = etree.Element("projet")

for method in root:
    print("computing dependencies in "+method.attrib.get("name"))
    cmethod=etree.SubElement(croot,"method")
    cmethod.set("name",method.attrib.get("name"))


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
    varSet=set([])
    slicing=dict()
    inVar=dict()
    outVar=dict()
    genVar=dict()
    killVar=dict()

    referenced=dict()
    definition=dict()
    dataDep=dict()

    revDep=dict()
    controleDep=dict()





    # dompostdom


    for bloc in method:
        nodemap[bloc.attrib.get("name")]=bloc.attrib.get("id")
        nodeSet.add(bloc.attrib.get("id"))
        dom[bloc.attrib.get("id")]=set([])
        postdom[bloc.attrib.get("id")]=set([])
        idom[bloc.attrib.get("id")]=set([])
        ipostdom[bloc.attrib.get("id")]=set([])
        initDom[bloc.attrib.get("id")]=set([])
        initPostdom[bloc.attrib.get("id")]=set([])
        controleDep[bloc.attrib.get("id")]=set([])
        dataDep[bloc.attrib.get("id")]=set([])


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
        ipostdom[i]|=postdom[i]
        for j in postdom[i]:
            ipostdom[i]-=postdom[j]
        idom[i]|=dom[i]
        for j in dom[i]:
            idom[i]-=dom[j]


    S=dict()

    for i in nodeSet :
        S[i]=enfants[i]-postdom[i]




    #calcul de dépendences
    for x in nodeSet :
        for y in S[x]:
            node=y
            while not(node in ipostdom[x]):

                controleDep[x].add(node)
                for next in ipostdom[node]:
                    node=next
                if len(ipostdom[node])==0:
                    break








    #dependence donnees

    finish = False


    for bloc in method:





        if bloc.attrib.get("instruction").__contains__("arraystore"):
            if not(bloc.findall(".use")[0].attrib.get("id") in definition):
                definition[bloc.findall(".use")[0].attrib.get("id")]=set([])
            definition[bloc.findall(".use")[0].attrib.get("id")].add(bloc.attrib.get("id"))
        else:
            for defined in bloc.findall(".def"):
                if not(defined.attrib.get("id") in definition):
                    definition[defined.attrib.get("id")]=set([])
                definition[defined.attrib.get("id")].add(bloc.attrib.get("id"))

        for refered in bloc.findall(".use"):
            if not(refered.attrib.get("id") in referenced):
                referenced[refered.attrib.get("id")]=set([])
            referenced[refered.attrib.get("id")].add(bloc.attrib.get("id"))






    for bloc in method:

        inVar[bloc.attrib.get("id")]=set([])
        outVar[bloc.attrib.get("id")]=set([])
        genVar[bloc.attrib.get("id")]=set([])
        killVar[bloc.attrib.get("id")]=set([])
        if bloc.attrib.get("instruction").__contains__("putfield"):
            if len(bloc.attrib.get("instruction").split(','))>2:

                field=bloc.attrib.get("instruction").split(',')[2].replace(' ','')
                genVar[bloc.attrib.get("id")].add(field)
                varSet.add(field)
        for child in bloc.findall(".edge"):
            parents[child.attrib.get("target")].add(bloc.attrib.get("id"))


    for bloc in method:
        for bloc2 in method:
            if len(genVar[bloc.attrib.get("id")] & genVar[bloc2.attrib.get("id")])>0 and bloc!=bloc2 :
                killVar[bloc.attrib.get("id")].add(bloc2.attrib.get("id"))

    while not finish :
        inVarInit=inVar.copy()
        for bloc in method:
            bloc.attrib.get("name")
            inVar[bloc.attrib.get("id")]=set([])
            for par in parents[bloc.attrib.get("id")]:
                inVar[bloc.attrib.get("id")]|=outVar[par]
            outVar[bloc.attrib.get("id")]=inVar[bloc.attrib.get("id")].copy()
            if len(genVar[bloc.attrib.get("id")])>0:

                outVar[bloc.attrib.get("id")].add((bloc.attrib.get("id")))
                outVar[bloc.attrib.get("id")]-=killVar[bloc.attrib.get("id")]

        finish = inVarInit==inVar

    for bloc in method:
        if bloc.attrib.get("instruction").__contains__("getfield"):
            if len(bloc.attrib.get("instruction").split(','))>2:
                field=bloc.attrib.get("instruction").split(',')[2].replace(' ','')
                for i in inVar[bloc.attrib.get("id")]:
                    if field in genVar[i]:
                        dataDep[i].add(bloc.attrib.get("id"))


        for var in bloc.findall('.def'):
            if var.attrib.get("id") in referenced:
                for i in referenced[var.attrib.get("id")]:
                    dataDep[bloc.attrib.get("id")].add(i)








    for i in nodeSet:
        cnode=etree.SubElement(cmethod,"node")
        cnode.set("id",i)
        for j in controleDep[i]:
            ccontdep=etree.SubElement(cnode,"control_dep")
            ccontdep.set("id",j)
        for j in dataDep[i]:
            cdatadep=etree.SubElement(cnode,"data_dep")
            cdatadep.set("id",j)








cOutFile.write(etree.tostring(croot, pretty_print=True))




