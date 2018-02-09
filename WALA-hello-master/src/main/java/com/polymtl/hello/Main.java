package com.polymtl.hello;

import com.ibm.wala.ipa.callgraph.CallGraphBuilderCancelException;
import com.ibm.wala.util.WalaException;
import com.polymtl.hello.drivers.BasicAnalysis;
import com.polymtl.hello.drivers.DumpWala;

import java.io.IOException;

/**
 *
 * This simple example WALA application analyze a project and push it.
 *
 * @author Nicolas Cloutier
 */
public class Main {

    public static void main(String[] args) throws IOException, WalaException {
        BasicAnalysis analysis = new DumpWala();
        analysis.setupRun();
        try {
            analysis.run();
        } catch (CallGraphBuilderCancelException e) {
            e.printStackTrace();
        }
    }

}
