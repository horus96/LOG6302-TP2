import xml.etree.cElementTree as ET
import re
import os
import csv
import sets as s
numero=0

# test
outFile = open('textFiles/dep.dot', 'wb')




tree = ET.parse('textFiles/cleancfg.xml')
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
varSet=set([])
slicing=dict()
inVar=dict()
outVar=dict()
genVar=dict()
killVar=dict()
parents=dict()
nodemap=dict()
referenced=dict()
definition=dict()
dataDep=dict()

revDep=dict()
controleDep=dict()



#dependances de contrôle

for bloc in root:
    nodemap[bloc.attrib.get("name")]=bloc.attrib.get("id")
    nodeSet.add(bloc.attrib.get("id"))
    dom[bloc.attrib.get("id")]=set([])
    postdom[bloc.attrib.get("id")]=set([])
    idom[bloc.attrib.get("id")]=set([])
    ipostdom[bloc.attrib.get("id")]=set([])
    initDom[bloc.attrib.get("id")]=set([])
    initPostdom[bloc.attrib.get("id")]=set([])
    dataDep[bloc.attrib.get("id")]=set([])
    parents[bloc.attrib.get("id")]=set([])
    controleDep[bloc.attrib.get("id")]=set([])
    revDep[bloc.attrib.get("id")]=set([])





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


S=dict()

for i in nodeSet :
    S[i]=enfants[i]-postdom[i]





for x in nodeSet :
    for y in S[x]:
        node=y
        while not(node in ipostdom[x]):

            controleDep[x].add(node)
            for next in ipostdom[node]:
                node=next






#dependance de donnees

finish = False


for bloc in root:


    nodemap[bloc.attrib.get("name")]=bloc.attrib.get("id")


    for ssa in bloc.findall(".ssa"):
        if ssa.attrib.get("instruction").__contains__("arraystore"):
            if not(ssa.findall(".use")[0].attrib.get("id") in definition):
                definition[ssa.findall(".use")[0].attrib.get("id")]=set([])
            definition[ssa.findall(".use")[0].attrib.get("id")].add(bloc.attrib.get("id"))
        else:
            for defined in ssa.findall(".def"):
                if not(defined.attrib.get("id") in definition):
                    definition[defined.attrib.get("id")]=set([])
                definition[defined.attrib.get("id")].add(bloc.attrib.get("id"))

        for refered in bloc.findall(".use"):
            if not(refered.attrib.get("id") in referenced):
                referenced[refered.attrib.get("id")]=set([])
            referenced[refered.attrib.get("id")].add(bloc.attrib.get("id"))


    for defined in bloc.findall(".phis/phiinstr/def"):
        if not(defined.attrib.get("id") in definition):
            definition[defined.attrib.get("id")]=set([])
        definition[defined.attrib.get("id")].add(bloc.attrib.get("id"))
    for defined in bloc.findall(".pis/piinstr/def"):
        if not(defined.attrib.get("id") in definition):
            definition[defined.attrib.get("id")]=set([])
        definition[defined.attrib.get("id")].add(bloc.attrib.get("id"))


    for refered in bloc.findall(".phis/phiinstr/use"):
        if not(refered.attrib.get("id") in referenced):
            referenced[refered.attrib.get("id")]=set([])
        referenced[refered.attrib.get("id")].add(bloc.attrib.get("id"))
    for refered in bloc.findall(".pis/piinstr/use"):
        if not(refered.attrib.get("id") in referenced):
            referenced[refered.attrib.get("id")]=set([])
        referenced[refered.attrib.get("id")].add(bloc.attrib.get("id"))




for bloc in root:

    inVar[bloc.attrib.get("id")]=set([])
    outVar[bloc.attrib.get("id")]=set([])
    genVar[bloc.attrib.get("id")]=set([])
    killVar[bloc.attrib.get("id")]=set([])
    if len(bloc.findall('.ssa'))>0 and bloc.findall('.ssa')[0].attrib.get("instruction").__contains__("putfield"):
        if len(bloc.findall('.ssa')[0].attrib.get("instruction").split(','))>2:

            field=bloc.findall('.ssa')[0].attrib.get("instruction").split(',')[2].replace(' ','')
            genVar[bloc.attrib.get("id")].add(field)
            varSet.add(field)
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

            outVar[bloc.attrib.get("id")].add((bloc.attrib.get("id")))
            outVar[bloc.attrib.get("id")]-=killVar[bloc.attrib.get("id")]

    finish = inVarInit==inVar

for bloc in root:
    if len(bloc.findall('.ssa'))>0 and bloc.findall('.ssa')[0].attrib.get("instruction").__contains__("getfield"):
        if len(bloc.findall('.ssa')[0].attrib.get("instruction").split(','))>2:
            field=bloc.findall('.ssa')[0].attrib.get("instruction").split(',')[2].replace(' ','')
            for i in inVar[bloc.attrib.get("id")]:
                if field in genVar[i]:
                    dataDep[i].add(bloc.attrib.get("id"))


    for var in bloc.findall('.ssa/def'):
        if var.attrib.get("id") in referenced:
            for i in referenced[var.attrib.get("id")]:
                dataDep[bloc.attrib.get("id")].add(i)





outFile.write("digraph G{\n")
# outFile.write("graph [splines=ortho, nodesep=2]\n")
outFile.write("fontname = \"Bitstream Vera Sans\"\n")
outFile.write("fontname = \"Bitstream Vera Sans\"\n")
outFile.write("fontsize = 8\n")
outFile.write("node [\n")
outFile.write("fontname = \"Bitstream Vera Sans\"\n")
outFile.write("fontsize = 8\n")
outFile.write("shape = \"circle\"\n")
outFile.write("]\n")
outFile.write("edge [\n")
outFile.write("fontname = \"Bitstream Vera Sans\"\n")
outFile.write("fontsize = 8\n")
outFile.write("]\n")


for i in nodeSet:
    outFile.write(i)
    outFile.write("[label=")
    outFile.write(i)
    outFile.write("]\n")




for i in nodeSet:
    for j in controleDep[i]:
        revDep[j].add(i)
        outFile.write(i)
        outFile.write("->")
        outFile.write(j)
        outFile.write(" [color=blue]")
        outFile.write("\n")

for i in nodeSet:
    for j in dataDep[i]:
        revDep[j].add(i)
        outFile.write(i)
        outFile.write("->")
        outFile.write(j)
        outFile.write("\n")

outFile.write("}")



for bloc in root:
    if bloc.attrib.get("name").__contains__("exit"):
        for field in varSet:
            slicing[field]=set([])
            visiting=set([])
            for possibleDef in inVar[bloc.attrib.get("id")]:
                if field in genVar[possibleDef]:
                    visiting.add(possibleDef)
                    slicing[field].add(possibleDef)
            while len(visiting)>0:
                x=visiting.pop()
                visiting|=(revDep[x]-slicing[field])
                slicing[field]|=revDep[x]




l=[]
with open('textFiles/slicing.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)


    for x in nodeSet:
        l.append(int(x))
    ltemp=sorted(l)
    l=[]
    for x in ltemp:
        l.append(str(x))
    writer.writerow(['']+l)
    for v in varSet:
        lv=[v]
        for x in l:
            if x in slicing[v]:
                lv.append('X')
            else:
                lv.append('')
        writer.writerow(lv)

