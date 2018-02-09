WALA Starter Kit
=======

### Introduction

This is a small example project to help in getting started with the
[WALA](https://github.com/wala/WALA) program analysis framework.  You
can clone and build this project to get WALA installed, and then
modify it to suit your own needs.

### Requirements

Requirements are:

  * Java 8
  * The [Gradle](https://gradle.org/) build tool

On Mac OS X, you can install these requirements by installing
[Homebrew](https://brew.sh/) and then running:

    brew cask install java
    brew install gradle
    
If you'd prefer to stick with Java 7, everything should work fine.
Just edit the line `sourceCompatibility = 1.8` in `build.gradle` to
read `sourceCompatibility = 1.7`.

### Installation

Clone the repository, and then run:

    gradle compileJava
    
This will pull in the WALA jars and build the sample code.

### Example analyses

  *
    [Variants of a simple dataflow analysis](https://github.com/msridhar/WALA-start/tree/master/src/main/java/com/ibm/wala/examples/analysis/dataflow), including an [example driver](https://github.com/msridhar/WALA-start/blob/master/src/main/java/com/ibm/wala/examples/drivers/CSReachingDefsDriver.java)
  * [Simple driver](https://github.com/msridhar/WALA-start/blob/master/src/main/java/com/ibm/wala/examples/drivers/ScopeFileCallGraph.java) for building a [call graph](http://wala.sourceforge.net/wiki/index.php/UserGuide:CallGraph) from a [scope file](http://wala.sourceforge.net/wiki/index.php/UserGuide:AnalysisScope)
  
We plan to add more examples soon, like examples of doing Android or JavaScript analysis.

License
-------

All code is available under the [Eclipse Public License](http://www.eclipse.org/legal/epl-v10.html).
