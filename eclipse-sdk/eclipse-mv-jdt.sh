#!/bin/sh

sdkDir=$1
jdtDir=$2

mkdir $jdtDir
cd $jdtDir
mkdir features plugins
mv $sdkDir/features/org.eclipse.jdt_* features
for plugin in org.eclipse.jdt \
 org.eclipse.ant.ui \
 org.eclipse.jdt.apt.core \
 org.eclipse.jdt.apt.ui \
 org.eclipse.jdt.apt.pluggable.core \
 org.eclipse.jdt.compiler.apt \
 org.eclipse.jdt.compiler.tool \
 org.eclipse.jdt.core \
 org.eclipse.jdt.core.manipulation \
 org.eclipse.jdt.debug.ui \
 org.eclipse.jdt.debug \
 org.eclipse.jdt.junit \
 org.eclipse.jdt.junit.runtime \
 org.eclipse.jdt.junit4.runtime \
 org.eclipse.jdt.launching \
 org.eclipse.jdt.ui \
 org.eclipse.jdt.doc.user \
 org.junit \
 org.junit4 ; do
 mv $sdkDir/plugins/${plugin}_* plugins
done

