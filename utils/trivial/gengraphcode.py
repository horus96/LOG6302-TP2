import os
import re


heritage_graph = open('textFiles/methodinfo.txt', 'r')
fonc_graph= open('textFiles/heritage.txt','r')

out = open('textFiles/logBigPart.dot', 'wb')
outSmallPart = open('textFiles/logSmallPart.dot', 'wb')
outSingle= open('textFiles/logSingle.dot', 'wb')
outTestCase = open('textFiles/logTestCase.dot', 'wb')
outStatement = open('textFiles/logStatement.dot', 'wb')
outRunListener= open('textFiles/logRunListener.dot', 'wb')








l="continue"

listClass=[]        #Liste des classes du projet

herit={}            #Carte indiquant des parents de chaque classe

genereRec={}        #Carte indiquant des enfants de chaque classe

funTab={}           #Carte indiquant les methodes de chaque classe

fieldTab={}         #Carte indiquant les attributs de chaque classe

agreg={}            #Carte indiquant les classes composant chaque classe

types={}             #Carte indiquant le type de chaque fonction et attribut de chaque classe

link={}             #Carte indiquant les classes en lien avec chaque classe

while l!="":
    l=fonc_graph.readline()
    classsplit=re.split('[,<>]',l)
    if len(classsplit)>2:
        theClassPre= (classsplit[2].split('/')[-1])
        theClassInterm= theClassPre.split('$')
        if len(theClassInterm)==2:
            theClass=theClassInterm[0]+"XXX"
        else:
            theClass=theClassInterm[0]
        if not(listClass.__contains__(theClass)):


            if(classsplit[1]=="Application"):
                listClass.append(theClass)
                herit[theClass]=[]
                genereRec[theClass]=[]
                #print(theClass)
                l2=fonc_graph.readline()

                l3=l2.replace("[< ",'').replace(">] ", '').split(">, <")
                l4=[]
                for e in l3:
                    r=e.split(",")
                    if len(r)>2:
                        fun=(r[2].split("(")[0]).replace('$',"")
                        types[theClass,fun]=(r[2].split(")"))[1].split('/')[-1].replace(" >]","").replace(";","").replace(" ","").replace("\n","")
                        #funInterm=preFun.split('$')
                        #if len(funInterm)==2:
                        #    fun=funInterm[0]+"___"
                        #else:
                        #    fun=funInterm[0]
                        if not(l4.__contains__(fun)):
                            l4.append(fun)
                #print(l4)
                funTab[theClass]=l4
                #out.write(theClass+"["+"label=\"{"+theClass)
                #out.write("||")
                #for e in l4:
                #    out.write("+ "+e.replace("<",'').replace(">", '')+"() : void\\l")
                #out.write("}\"]\n")
                fonc_graph.readline()
                f2=fonc_graph.readline()

                f3=f2.replace("[< ",'').replace(">] ", '').split(">, <")
                f4=[]
                for e in f3:
                    r=e.split(",")
                    if len(r)>2:
                        field=(r[2])
                        types[theClass,field]=(r[1]).split('/')[-1].replace(" >]","").replace(";","").replace(" ","").replace("\n","")
                        if not(f4.__contains__(field)):
                            f4.append(field)
                fieldTab[theClass]=f4




#out.write("edge [arrowhead = \"empty\"]\n")
l=heritage_graph.readline()

listRel=[]
while l!="":

    parent=re.split('[>,<]',l)
    if len(parent)>1:
        if parent[1]=="Application":
            parentClassPre=(parent[2].split('/')[-1])

            parentClassInterm= parentClassPre.split('$')
            if len(parentClassInterm)==2:
                parentClass=parentClassInterm[0]+"XXX"
            else:
                parentClass=parentClassInterm[0]

            l=heritage_graph.readline()
            while l!='\n' and l!="":
                l2=re.split('[<>,/]', l)
                if len(l2)>1:
                    enfantClassPre=(l2[-2])

                    enfantClassInterm= enfantClassPre.split('$')
                    if len(enfantClassInterm)==2:
                        enfantClass=enfantClassInterm[0]+"XXX"
                    else:
                        enfantClass=enfantClassInterm[0]

                    if not(listRel.__contains__((enfantClass,parentClass))):
                        listRel.append((enfantClass,parentClass))
                        herit[enfantClass].append(parentClass)
                        genereRec[parentClass].append(enfantClass)
                        #out.write(parentClass+"->"+enfantClass+"\n")
                l=heritage_graph.readline()
    l=heritage_graph.readline()



for classe in listClass:
    newList=list(herit[classe])
    for parents in herit[classe]:
        if parents!=classe:
            for redond in herit[parents]:
                if newList.__contains__(redond) and redond!=parents:
                    newList.remove(redond)
        herit[classe]=newList




firstListClass=[]           #Liste des classes de GraphBigPart
secondListClass=[]          #Liste des classes de GraphSmallPart
thirdListClass=[]           #Liste des classes de GraphTestCase
forthListClass=[]           #Liste des classes de GraphStatement
fifthListClass=[]           #Liste des classes de GraphRunListener
lastListClass=[]           #Liste des classes de SingleListener

#element="ExpectExceptionTestXXX"
#print(len(herit[element])>0 and (len(herit[element])>1 or herit[element][0]!=element))


for classe in listClass:
    agregList=[]
    for fields in fieldTab[classe]:
        if listClass.__contains__(types[classe,fields]):
            if not(agregList.__contains__(types[classe,fields])):
                agregList.append(types[classe,fields])
    agreg[classe]=agregList

for classe in listClass:
    link[classe]=[]

for classe in listClass:
    for e in agreg[classe]:
        link[classe].append(e)
        if e!=classe:
            link[e].append(classe)
    for e in herit[classe]:
        if not(link[classe].__contains__(e)):
            link[classe].append(e)
            if e!=classe:
                link[e].append(classe)



for classe in listClass:

    isTestCase= (len(link[classe])==2 and link[classe].__contains__("TestCase")and link[classe].__contains__(classe)) or (len(link[classe])==1 and link[classe][0]==("TestCase"))
    isStatement= (len(link[classe])==2 and link[classe].__contains__("Statement")and link[classe].__contains__(classe)) or (len(link[classe])==1 and link[classe][0]==("Statement"))
    isRunListener= (len(link[classe])==2 and link[classe].__contains__("RunListener")and link[classe].__contains__(classe)) or (len(link[classe])==1 and link[classe][0]==("RunListener"))

    connex=[]
    connex.append(classe)
    for i in range(7):
        for element1 in connex:
            for element2 in link[element1]:
                if not(connex.__contains__(element2)):
                    connex.append(element2)
    isInFirstGraph=len(connex)>6
    isInSecondGraph=not(isInFirstGraph) and len(connex)>1
    isInFirstGraph=isInFirstGraph and not(isTestCase) and not(isStatement) and not(isRunListener)
    isInLastGraph=len(connex)<2




    if isInFirstGraph:
        firstListClass.append(classe)


    elif isInSecondGraph:
        secondListClass.append(classe)

    elif isInLastGraph:
        lastListClass.append(classe)

    if isTestCase or classe=="TestCase":
        thirdListClass.append(classe)

    if isStatement or classe=="Statement":
        forthListClass.append(classe)

    if isRunListener or classe=="RunListener":
        fifthListClass.append(classe)



#Fonction generant les fichier .dot pour chaque graphe UML a generer

def afficher(classList,outFile):
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

    for classe in classList:
        outFile.write(classe+"["+"label=\"{"+classe)
        outFile.write("|")
        for e in fieldTab[classe]:
            outFile.write("+ "+e.replace("<",'').replace(">", '')+" : ")
            outFile.write(types[classe,e])
            outFile.write("\\l")
        outFile.write("|")
        for e in funTab[classe]:
            outFile.write("+ "+e.replace("<",'').replace(">", '')+"() : ")
            if types[classe,e]=="V":
                outFile.write("void")
            else:
                outFile.write(types[classe,e])
            outFile.write("\\l")
        outFile.write("}\"]\n")

    outFile.write("edge [arrowhead = \"empty\"]\n")

    for classe in classList:
        for parent in herit[classe]:
            if classList.__contains__(parent):
                outFile.write(classe+"->"+parent+"\n")

    outFile.write("edge [arrowhead = \"normal\"]\n")

    for classe in classList:
        for type in agreg[classe]:
            if classList.__contains__(type):
                outFile.write(classe+"->"+type+"\n")

    outFile.write("}\n")
#fin fonction afficher




afficher(firstListClass,out)
afficher(secondListClass,outSmallPart)
afficher(thirdListClass,outTestCase)
afficher(forthListClass,outStatement)
afficher(fifthListClass,outRunListener)
afficher(lastListClass,outSingle)
