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
import java.io.IOException;

import com.ibm.wala.ipa.callgraph.AnalysisScope;
import com.ibm.wala.ipa.callgraph.CallGraphBuilderCancelException;
import com.ibm.wala.util.config.AnalysisScopeReader;

import com.polymtl.hello.util.BasicUtil;

/**
 *
 * This simple example WALA application analyze a project and push it.
 *
 * @author Nicolas Cloutier
 */
public abstract class BasicAnalysis {
    protected AnalysisScope scope = null;

    public abstract void run() throws IOException, CallGraphBuilderCancelException;

    public void setupRun() throws IOException {
        String scopeFile = "scopeFile.conf";
        File f = new File(scopeFile);
        if(!f.exists() || f.isDirectory()) {
            throw new IOException("Scope File not found!");
        }

        this.scope = AnalysisScopeReader.readJavaScope(scopeFile, null, DumpWala.class.getClassLoader());
        BasicUtil.addDefaultExclusions(scope);
    }
}
