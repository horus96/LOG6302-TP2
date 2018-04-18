/*******************************************************************************
 * Copyright (c) 2002 - 2006 IBM Corporation.
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * which accompanies this distribution, and is available at
 * http://www.eclipse.org/legal/epl-v10.html
 *
 * Contributors:
 *     IBM Corporation - initial API and implementation
 *     Nicolas Cloutier - Polymtl Modification for an easy build
 *     Karl Julien - Polymtl Modification for extraction
 *******************************************************************************/
package com.polymtl.hello.drivers;

import java.io.File;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.io.IOException;
import java.util.*;

import com.ibm.wala.analysis.pointers.BasicHeapGraph;
import com.ibm.wala.cast.ir.ssa.AstIRFactory;
import com.ibm.wala.cast.ir.ssa.SSAConversion;
import com.ibm.wala.cast.loader.AstMethod;
import com.ibm.wala.cast.types.AstMethodReference;
import com.ibm.wala.cfg.ControlFlowGraph;
import com.ibm.wala.classLoader.*;
import com.ibm.wala.dataflow.IFDS.ICFGSupergraph;
import com.ibm.wala.dataflow.IFDS.ISupergraph;
import com.ibm.wala.ipa.callgraph.*;
import com.ibm.wala.ipa.callgraph.impl.Everywhere;
import com.ibm.wala.ipa.callgraph.impl.Util;
import com.ibm.wala.ipa.callgraph.propagation.InstanceKey;
import com.ibm.wala.ipa.callgraph.propagation.PointerAnalysis;
import com.ibm.wala.ipa.cfg.BasicBlockInContext;
import com.ibm.wala.ipa.cfg.ExplodedInterproceduralCFG;
import com.ibm.wala.ipa.cha.ClassHierarchy;
import com.ibm.wala.ipa.cha.ClassHierarchyFactory;
import com.ibm.wala.ipa.cha.IClassHierarchy;
import com.ibm.wala.shrikeBT.Instruction;
import com.ibm.wala.shrikeCT.InvalidClassFileException;
import com.ibm.wala.ssa.*;
import com.ibm.wala.ssa.analysis.IExplodedBasicBlock;
import com.ibm.wala.types.ClassLoaderReference;
import com.ibm.wala.util.Predicate;
import com.ibm.wala.util.WalaException;
import com.ibm.wala.util.collections.CollectionFilter;
import com.ibm.wala.util.collections.Factory;
import com.ibm.wala.util.graph.Graph;
import com.ibm.wala.util.graph.GraphSlicer;
import com.ibm.wala.util.graph.impl.SlowSparseNumberedGraph;
import com.ibm.wala.viz.DotUtil;
import org.omg.PortableInterceptor.SYSTEM_EXCEPTION;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.*;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

/**
 * Extractor
 */
public class DumpWala extends BasicAnalysis {
    public void run() throws IOException, CallGraphBuilderCancelException {
        try {

            String outFilef = "../textFiles/methodinfo.txt";
            System.out.println(outFilef);

            String outFilecfg = "../logcfg.txt";
            System.out.println(outFilecfg);

            String outFilesupercfg = "../logsupercfg.txt";
            System.out.println(outFilesupercfg);

            String outIntRep = "../logir.txt";


            String outStrSsa = "../logssa.txt";
            String outXml = "../logxml.txt";


            String outStrSsaBis = "../logssabis.txt";

            PrintWriter outtt = new PrintWriter(outFilef);
            PrintWriter outttt = new PrintWriter(outFilecfg);
            PrintWriter superout = new PrintWriter(outFilesupercfg);
            PrintWriter outir = new PrintWriter(outIntRep);
            PrintWriter outssa = new PrintWriter(outStrSsa);
            PrintWriter outssabis = new PrintWriter(outStrSsaBis);
            PrintWriter outxml = new PrintWriter(outXml);


            HashMap<String,Element> xmlFuncMap = new HashMap();
            HashMap<String,Element> xmlClassMap = new HashMap();


            boolean showPrimordial= false;

            DocumentBuilderFactory xmlfactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder xmlbuilder = xmlfactory.newDocumentBuilder();
            Document xml = xmlbuilder.newDocument();
            Element xmlRoot = xml.createElement("project");

            ClassHierarchy cha = ClassHierarchyFactory.make(this.scope);


            AnalysisOptions options = new AnalysisOptions();


            //definition des points d'entree

            Iterable<Entrypoint> entrypoints = Util.makeMainEntrypoints(scope, cha);


            //definition des options d extraction

            options.setEntrypoints(entrypoints);
            // you can dial down reflection handling if you like
            options.setReflectionOptions(AnalysisOptions.ReflectionOptions.NONE);
            AnalysisCache cache = new AnalysisCacheImpl();
            // other builders can be constructed with different Util methods
            CallGraphBuilder builder = Util.makeZeroOneContainerCFABuilder(options, cache, cha, scope);
//	    CallGraphBuilder builder = Util.makeNCFABuilder(2, options, cache, cha, scope);
//	    CallGraphBuilder builder = Util.makeVanillaNCFABuilder(2, options, cache, cha, scope);
            System.out.println("building call graph...");
            CallGraph cg = builder.makeCallGraph(options, null);
            /*PointerAnalysis<InstanceKey> pointerAnalysis = builder.getPointerAnalysis();
            BasicHeapGraph heapGraph = new BasicHeapGraph<>(pointerAnalysis, cg);
            DotUtil.dotify(heapGraph,null,"/home/travail/TP2/LOG6302_TP2/pointer.dot",null,null);*/

            // invoke WALA to build a class hierarchyPrintWriter out = new PrintWriter(outFile)

            SSAOptions factoptions = new SSAOptions();
            IRFactory<IMethod> F = AstIRFactory.makeDefaultFactory();
            Graph<IClass> g = typeHierarchy2Graph(cha);



            // extraction d informations sur les methodes pour la generation du diagramme UML
            for (IClass c : g) {


                outtt.println(c);
                Collection<IMethod> ms = c.getDeclaredMethods();
                outtt.println(ms);
                outtt.println("______");
                Collection<IField> fs = c.getAllFields();
                outtt.println(fs);

            }
            g = pruneForAppLoader(g);
            //String outFile = File.createTempFile("out", ".txt").getAbsolutePath();
            String outFile = "../textFiles/heritage.txt";
            System.out.println(outFile);
            try (PrintWriter out = new PrintWriter(outFile)) {
                out.println(g);
            }


            IRFactory<IMethod> factory = AstIRFactory.makeDefaultFactory();


            //Super cfg
            ICFGSupergraph intercfg = ICFGSupergraph.make(cg);

            intercfg.getNumberOfNodes();
            superout.println(intercfg);

            ExplodedInterproceduralCFG interbis = ExplodedInterproceduralCFG.make(cg);
            Iterator<BasicBlockInContext<IExplodedBasicBlock>> it = interbis.iterator();
            BasicBlockInContext<IExplodedBasicBlock> bloc = it.next();



            //impression du cfg en format xml

            while (it.hasNext()) {


                IMethod m = bloc.getMethod();


                IMethod m2 = m;



                if (m2.toString().contains("Application") || showPrimordial){


                outssabis.println(m);


                    Element xmlMethod;
                    Element xmlClass;


                    //Si la methode ou la classe a deja ete visitee, on met les nouveaux blocs dans la meme methode
                    if (xmlFuncMap.containsKey(m.toString())){
                        xmlMethod=xmlFuncMap.get(m.toString());
                        xmlClass=xmlClassMap.get(m.getDeclaringClass().toString());
                    }else{

                        xmlMethod = xml.createElement("function");
                        xmlMethod.setAttribute("name", m.toString());
                        xmlFuncMap.put(m.toString(),xmlMethod);
                        if (xmlClassMap.containsKey(m.getDeclaringClass().toString())){
                        xmlClass=xmlClassMap.get(m.getDeclaringClass().toString());
                        }else{

                        xmlClass=xml.createElement("class");
                        xmlClass.setAttribute("name", m.getDeclaringClass().toString());
                        xmlClassMap.put(m.getDeclaringClass().toString(),xmlClass);
                        xmlRoot.appendChild(xmlClass);
                        Collection<IField> fs = m.getDeclaringClass().getAllFields();
                        for (IField i : fs){
                            Element xmlField = xml.createElement("field");
                            xmlField.setAttribute("name",i.toString());
                            xmlClass.appendChild(xmlField);
                            }

                        }
                        xmlClass.appendChild(xmlMethod);
                    }





                //outxml.print("<function name=\"");
                //outxml.print(m);
                //outxml.println("\">");

                //<function name="get_sitestats">

                IR ir= bloc.getNode().getIR();


                SymbolTable table = ir.getSymbolTable();
                DefUse du = bloc.getNode().getDU();
                Context context = bloc.getNode().getContext();
                addConstants(xmlMethod,ir, xml);


                    /*IR.SSA2LocalMap localMap = SSAConversion.convert( m, ir, SSAOptions.defaultOptions());
                    AstIRFactory.AstIR;*/


                // On entre dans une methode
                while (m2 == m && it.hasNext()) {

                    String sfName = m.getDeclaringClass().getSourceFileName();

                    Element xmlBloc = xml.createElement("bloc");

                    xmlBloc.setAttribute("name", bloc.toString());
                    xmlBloc.setAttribute("context", context.toString());

                    xmlMethod.appendChild(xmlBloc);

                    //outxml.print("\t<bloc=\"");
                    //outxml.print(bloc);
                    //outxml.println("\">");

                    Iterator<BasicBlockInContext<IExplodedBasicBlock>> succIt = interbis.getSuccNodes(bloc);

                    //Extraction des arcs
                    while (succIt.hasNext()) {


                        Element xmlEdge = xml.createElement("edge");
                        xmlEdge.setAttribute("target", succIt.next().toString());
                        xmlBloc.appendChild(xmlEdge);

                        //outxml.print("\t\t<edge target=\"");
                        //outxml.print(succIt.next());
                        //outxml.println("\">");
                    }

                    SSAInstruction ssaInstr = bloc.getLastInstruction();



                    if (ssaInstr != null) {



                        Element xmlSsa = xml.createElement("ssa");
                        xmlSsa.setAttribute("instruction", ssaInstr.toString());
                        xmlBloc.appendChild(xmlSsa);
                        //outxml.print("\t\t<ssa instr=\"");
                        //outxml.print(ssaInstr.toString());
                        //outxml.println("\">");


                        IBytecodeMethod bcm = ((IBytecodeMethod) m);
                        int bcIndex = bcm.getBytecodeIndex(ssaInstr.iindex);
                        int sourceLineNum = bcm.getLineNumber(bcIndex);


                        for (int j = 0; j < ssaInstr.getNumberOfDefs(); j++) {
                            Element xmlDef = xml.createElement("def");
                            xmlDef.setAttribute("id", String.valueOf(ssaInstr.getDef(j)));
                            xmlSsa.appendChild(xmlDef);


                            /*for (int k = 1; k <=heapGraph.getMaxNumber(); k++) {
                                String[] splitedNode=(heapGraph.getNode(k)).toString().split(" Context:");


                                if(        splitedNode.length>1){






                                    if(splitedNode[0].contains(xmlMethod.getAttribute("name"))
                                        && splitedNode[1].contains(context.toString())
                                        && splitedNode[1].contains("v"+String.valueOf(ssaInstr.getDef(j))+"]")){



                                        //Iterator typeit = heapGraph.getSuccNodes(k);

                                        Stack types = new Stack();
                                        types.push(heapGraph.getNode(k));
                                        while (!types.isEmpty()){
                                            Object node = types.pop();
                                            if (heapGraph.getSuccNodeCount(node)>0){
                                                Iterator typeit=heapGraph.getSuccNodes(node);
                                                while(typeit.hasNext()){
                                                    types.push(typeit.next());
                                                }
                                            }
                                            else{
                                                Element xmlType = xml.createElement("type");
                                                xmlType.setAttribute("name", String.valueOf(node));
                                                xmlDef.appendChild(xmlType);

                                            }


                                        }

                                    }}
                            }*/



                            //outxml.print("\t\t\t<def id=");outxml.print(ssaInstr.getDef(j));outxml.println(">");
                        }

                        for (int j = 0; j < ssaInstr.getNumberOfUses(); j++) {
                            Element xmlUse = xml.createElement("use");
                            xmlUse.setAttribute("id", String.valueOf(ssaInstr.getUse(j)));
                            xmlSsa.appendChild(xmlUse);
                            String[] loc = ir.getLocalNames(ssaInstr.iindex, ssaInstr.getUse(j));

                            if (bloc.getLastInstructionIndex()>=0&&du.getDef(ssaInstr.getUse(j))!=null){
                                Element xmlDefssa = xml.createElement("ref");
                                xmlDefssa.setAttribute("instr",du.getDef(ssaInstr.getUse(j)).toString() );
                                xmlUse.appendChild(xmlDefssa);}

                            //outxml.print("\t\t\t<use id=");outxml.print(ssaInstr.getUse(j));outxml.println(">");
                        }

                    }


                    //outxml.println("\t\t</ssa>");}


                    //Extraction des instructions phi et pi
                    Iterator<SSAPhiInstruction> iteratorPhis = bloc.getDelegate().iteratePhis();
                    if (iteratorPhis.hasNext()) {

                        Element xmlPhis = xml.createElement("phis");
                        xmlBloc.appendChild(xmlPhis);


                        //outxml.println("\t\t<phis>");

                        while (iteratorPhis.hasNext()) {
                            SSAPhiInstruction PhiInst = iteratorPhis.next();
                            outssabis.println(PhiInst);

                            Element xmlSsaPhis = xml.createElement("ssaPhis");
                            xmlSsaPhis.setAttribute("instruction", PhiInst.toString());
                            xmlPhis.appendChild(xmlSsaPhis);

                            //outxml.print("\t\t\t<ssa type=\"");
                            //outxml.print(PhiInst);
                            //outxml.println("\">");

                            for (int j = 0; j < PhiInst.getNumberOfDefs(); j++) {
                                Element xmlSsaDef = xml.createElement("def");
                                xmlSsaDef.setAttribute("id", String.valueOf(PhiInst.getDef(j)));
                                xmlSsaPhis.appendChild(xmlSsaDef);



                                //outxml.print("\t\t\t\t<def id=");
                                //outxml.print(PhiInst.getDef(j));
                                //outxml.println(">");
                            }

                            for (int j = 0; j < PhiInst.getNumberOfUses(); j++) {
                                Element xmlSsaUse = xml.createElement("use");
                                xmlSsaUse.setAttribute("id", String.valueOf(PhiInst.getUse(j)));
                                xmlSsaPhis.appendChild(xmlSsaUse);
                                //outxml.print("\t\t\t\t<use id=");
                                //outxml.print(PhiInst.getUse(j));
                                //outxml.println(">");
                            }
                        }
                    }//fin de l'extraction du cfg en format xml



                    outssabis.println("the instr:");
                    outssabis.println(bloc.getDelegate().getInstruction());
                    Iterator<SSAPiInstruction> iteratorPis = bloc.getDelegate().iteratePis();

                    if (iteratorPis.hasNext()) {
                        outssabis.println("pis:");
                        //outxml.println("\t\t<pis>");

                        Element xmlPis = xml.createElement("pis");
                        xmlBloc.appendChild(xmlPis);


                        while (iteratorPis.hasNext()) {
                            SSAPiInstruction PiInst = iteratorPis.next();
                            outssabis.println(PiInst);

                            //outxml.print("\t\t\t<ssa type=\"");
                            //outxml.print(PiInst);
                            //outxml.println("\">");

                            Element xmlSsaPis = xml.createElement("ssaPhis");
                            xmlSsaPis.setAttribute("instruction", PiInst.toString());
                            xmlPis.appendChild(xmlSsaPis);

                            for (int j = 0; j < PiInst.getNumberOfDefs(); j++) {
                                Element xmlSsaDef = xml.createElement("def");
                                xmlSsaDef.setAttribute("id", String.valueOf(PiInst.getDef(j)));
                                xmlSsaPis.appendChild(xmlSsaDef);

                                //outxml.print("\t\t\t\t<def id=");
                                //outxml.print(PiInst.getDef(j));
                                //outxml.println(">");
                            }
                            for (int j = 0; j < PiInst.getNumberOfUses(); j++) {
                                Element xmlSsaUse = xml.createElement("use");
                                xmlSsaUse.setAttribute("id", String.valueOf(PiInst.getUse(j)));
                                xmlSsaPis.appendChild(xmlSsaUse);

                                //outxml.print("\t\t\t\t<use id=");
                                //outxml.print(PiInst.getUse(j));
                                //outxml.println(">");
                            }
                        }
                    }


                    bloc = it.next();
                    m2 = bloc.getMethod();

                    //outxml.println("\t</bloc>");
                }
                }else{bloc=it.next();}

                //outxml.println("</function>");
                outssabis.println("=============================");
            }


            String resultFile = "../textFiles/dumpedcfg.xml";
            StreamResult XML = new StreamResult(resultFile);
            Transformer t = TransformerFactory.newInstance().newTransformer();
            t.setOutputProperty(OutputKeys.INDENT, "yes");
            t.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
            t.transform(new DOMSource(xmlRoot), XML);


            //cfg

            printcfg(factory, cha,outssa, outir, outttt);

            outssa.close();
            outssabis.close();
            outxml.close();






      /*intercfg.getSuccNodes();
              getICFG().;*/


            String outFile2 = "../locg.txt";
            System.out.println(outFile2);
            try (PrintWriter outt = new PrintWriter(outFile2)) {
                outt.println(cg);
            }
            return;
        } catch (WalaException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            return;
        } catch (ParserConfigurationException e) {
            e.printStackTrace();
        } catch (TransformerConfigurationException e) {
            e.printStackTrace();
        } catch (TransformerException e) {
            e.printStackTrace();
        } catch (InvalidClassFileException e) {
            e.printStackTrace();
        }
    }

    public static <T> Graph<T> pruneGraph(Graph<T> g, Predicate<T> f) throws WalaException {
        Collection<T> slice = GraphSlicer.slice(g, f);
        return GraphSlicer.prune(g, new CollectionFilter<>(slice));
    }


    public static void addConstants(Element xmlMethod, IR ir, Document xml){
        SymbolTable table = ir.getSymbolTable();
        int n = table.getMaxValueNumber();
        for (int i=1;i<=n;i++){
            if(table.isParameter(i)){
                Element xmlParameter = xml.createElement("parameter");
                xmlParameter.setAttribute("id", String.valueOf(i));
                xmlMethod.appendChild(xmlParameter);
            }

            if(table.isConstant(i)){
                Element xmlConstant = xml.createElement("constant");
                xmlConstant.setAttribute("id", String.valueOf(i));
                xmlConstant.setAttribute("value", String.valueOf(table.getConstantValue(i)));
                //xmlConstant.setAttribute("type",(table.getConstantValue(i)).getClass().toString());
                xmlMethod.appendChild(xmlConstant);
            }


        }


    }

    public static void printcfg(IRFactory<IMethod> factory, ClassHierarchy cha, PrintWriter outssa, PrintWriter outir, PrintWriter outttt){
        for (IClass klass : cha) {

            // get the IMethod representing the code
            if (klass.getClassLoader().getReference().equals(ClassLoaderReference.Application)) {
                for (IMethod m : klass.getDeclaredMethods()) {
                    if (m != null) {
                        try {
                            IR ir = factory.makeIR(m, Everywhere.EVERYWHERE, new SSAOptions());

                            outir.println(ir);
                            ControlFlowGraph<SSAInstruction, ISSABasicBlock> cfg = ir.getControlFlowGraph();
                            outssa.println(m);
                            for (SSAInstruction i : cfg.getInstructions()) {
                                try {

                                    outssa.print(i.iindex);
                                    outssa.print(" : ");
                                    outssa.print(ir.getBasicBlockForInstruction(i));
                                    outssa.print(" : ");
                                    outssa.println(i);
                                    outssa.print("|| NDef = ");
                                    outssa.print(i.getNumberOfDefs());
                                    outssa.print("|| NUse = ");
                                    outssa.println(i.getNumberOfUses());
                                    if (i.getNumberOfDefs() > 0) {
                                        outssa.print("def:");

                                        for (int j = 0; j < i.getNumberOfDefs(); j++) {
                                            outssa.print(i.getDef(j));
                                            outssa.print(", ");
                                        }
                                        outssa.println();
                                    }
                                    if (i.getNumberOfUses() > 0) {
                                        outssa.print("uses:");
                                        for (int j = 0; j < i.getNumberOfUses(); j++) {
                                            outssa.print(i.getUse(j));
                                            outssa.print(", ");
                                        }
                                        outssa.println();
                                    }
                                } catch (Exception e) {
                                    outssa.println("error");
                                }
                            }
                            outttt.println(cfg);
                        } catch (Exception e2) {
                            outttt.println("error");
                            outssa.println("error");
                        }
                        outttt.println("===================================");
                        outssa.println("===================================");
                        outttt.println(klass.getName());
                        outttt.println(m.getName());
                    }
                }

            }
        }
    }


    /**
     * Restrict g to nodes from the Application loader
     */
    public static Graph<IClass> pruneForAppLoader(Graph<IClass> g) throws WalaException {
        Predicate<IClass> f = new Predicate<IClass>() {
            @Override
            public boolean test(IClass c) {
                return (c.getClassLoader().getReference().equals(ClassLoaderReference.Application));
            }
        };
        return pruneGraph(g, f);
    }

    /**
     * Return a view of an {@link IClassHierarchy} as a {@link Graph}, with edges from classes to immediate subtypes
     */
    public static Graph<IClass> typeHierarchy2Graph(IClassHierarchy cha) throws WalaException {
        Graph<IClass> result = SlowSparseNumberedGraph.make();
        for (IClass c : cha) {
            result.addNode(c);
        }
        for (IClass c : cha) {
            for (IClass x : cha.getImmediateSubclasses(c)) {
                result.addEdge(c, x);
            }
            if (c.isInterface()) {
                for (IClass x : cha.getImplementors(c.getReference())) {
                    result.addEdge(c, x);
                }


            }
        }
        return result;
    }
}
