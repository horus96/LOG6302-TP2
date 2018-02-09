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
 *******************************************************************************/
package com.polymtl.hello.drivers;

import java.io.File;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.io.IOException;
import java.util.Collection;

import com.ibm.wala.cast.ir.ssa.AstIRFactory;
import com.ibm.wala.cast.loader.AstMethod;
import com.ibm.wala.cast.types.AstMethodReference;
import com.ibm.wala.cfg.ControlFlowGraph;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IField;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.dataflow.IFDS.ICFGSupergraph;
import com.ibm.wala.dataflow.IFDS.ISupergraph;
import com.ibm.wala.ipa.callgraph.*;
import com.ibm.wala.ipa.callgraph.impl.Everywhere;
import com.ibm.wala.ipa.callgraph.impl.Util;
import com.ibm.wala.ipa.cfg.BasicBlockInContext;
import com.ibm.wala.ipa.cha.ClassHierarchy;
import com.ibm.wala.ipa.cha.ClassHierarchyFactory;
import com.ibm.wala.ipa.cha.IClassHierarchy;
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

/**
 *
 * Extractor
 */
public class DumpWala extends BasicAnalysis {
  public void run() throws IOException, CallGraphBuilderCancelException {
    try {

      String outFilef = "/home/travail/logf.txt";
      System.out.println(outFilef);

      String outFilecfg = "/home/travail/logcfg.txt";
      System.out.println(outFilecfg);

        String outFilesupercfg = "/home/travail/logsupercfg.txt";
        System.out.println(outFilesupercfg);

      PrintWriter outtt = new PrintWriter(outFilef);
      PrintWriter outttt = new PrintWriter(outFilecfg);
      PrintWriter superout = new PrintWriter(outFilesupercfg);
        ClassHierarchy cha = ClassHierarchyFactory.make(this.scope);


        AnalysisOptions options = new AnalysisOptions();
        Iterable<Entrypoint> entrypoints = Util.makeMainEntrypoints(scope, cha);
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




      // invoke WALA to build a class hierarchyPrintWriter out = new PrintWriter(outFile)

      SSAOptions factoptions = new SSAOptions();
      IRFactory<IMethod> F = AstIRFactory.makeDefaultFactory();
      Graph<IClass> g = typeHierarchy2Graph(cha);
      for(IClass c: g){


          outtt.println(c);
          Collection<IMethod> ms = c.getDeclaredMethods();
          outtt.println(ms);
          outtt.println("______");
          Collection<IField> fs = c.getAllFields();
          outtt.println(fs);

      }
      g = pruneForAppLoader(g);
      //String outFile = File.createTempFile("out", ".txt").getAbsolutePath();
      String outFile = "/home/travail/log.txt";
      System.out.println(outFile);
      try(PrintWriter out = new PrintWriter(outFile)) {
        out.println(g);
      }


      IRFactory<IMethod> factory = AstIRFactory.makeDefaultFactory();


      //cfg
      for (IClass klass : cha) {

        // get the IMethod representing the code
          if(klass.getClassLoader().getReference().equals(ClassLoaderReference.Application)){
        for (IMethod m:klass.getAllMethods()){
        if (m != null) {
          try{IR ir = factory.makeIR(m, Everywhere.EVERYWHERE, new SSAOptions());
            ControlFlowGraph<SSAInstruction, ISSABasicBlock> cfg=ir.getControlFlowGraph();
            outttt.println(cfg);}
          catch(Exception e){outttt.println("error");}
          outttt.println("===================================");

          outttt.println(klass.getName());
          outttt.println(m.getName());
        }}

      }}



        //Super cfg
        ICFGSupergraph intercfg = ICFGSupergraph.make(cg);
        intercfg.getNumberOfNodes();
        superout.println(intercfg);





        String outFile2 = "/home/travail/locg.txt";
        System.out.println(outFile2);
        try(PrintWriter outt = new PrintWriter(outFile2)) {
            outt.println(cg);
        }
      return;
    } catch (WalaException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
      return;
    }
  }

  public static <T> Graph<T> pruneGraph(Graph<T> g, Predicate<T> f) throws WalaException {
    Collection<T> slice = GraphSlicer.slice(g, f);
    return GraphSlicer.prune(g, new CollectionFilter<>(slice));
  }

  /**
   * Restrict g to nodes from the Application loader
   */
  public static Graph<IClass> pruneForAppLoader(Graph<IClass> g) throws WalaException {
    Predicate<IClass> f = new Predicate<IClass>() {
      @Override public boolean test(IClass c) {
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
