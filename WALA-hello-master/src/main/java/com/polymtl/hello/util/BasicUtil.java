package com.polymtl.hello.util;

import java.io.ByteArrayInputStream;
import java.io.IOException;

import com.ibm.wala.ipa.callgraph.AnalysisScope;
import com.ibm.wala.util.config.FileOfClasses;

public class BasicUtil {

	// more aggressive exclusions to avoid library blowup
	  // in interprocedural tests
  	private static final String EXCLUSIONS = "java\\/awt\\/.*\n" +
  		"javax\\/swing\\/.*\n" + 
  		"sun\\/awt\\/.*\n" + 
  		"sun\\/swing\\/.*\n" + 
  		"com\\/sun\\/.*\n" + 
  		"sun\\/.*\n" + 
  		"org\\/netbeans\\/.*\n" + 
  		"org\\/openide\\/.*\n" + 
  		"com\\/ibm\\/crypto\\/.*\n" + 
  		"com\\/ibm\\/security\\/.*\n" + 
  		"org\\/apache\\/xerces\\/.*\n" + 
  		"java\\/security\\/.*\n" + 
  		"";

	public static void addDefaultExclusions(AnalysisScope scope) throws IOException {
		scope.setExclusions(new FileOfClasses(new ByteArrayInputStream(BasicUtil.EXCLUSIONS.getBytes("UTF-8"))));
	}
	  
}
