#!/bin/bash

file="$1"
output="$2"

shopt -s nocasematch
if [[ $file != *.xml ]]; then
	echo "The filetype must be XML. Syntax: AutoDecrypt-mRemoteNG.sh file.xml output.txt"
elif [[ $output == '' ]]; then
	echo "You must specify an output file. Syntax: AutoDecrypt-mRemoteNG.sh file.xml output.txt"	
else
	xmlstarlet sel  -t -m //Node -v "concat(@Username,':',@Password)" -n $file | grep -v "^:$" > $output
	echo "$(./AutoDecrypt-mRemoteNG.py -f $output)" > $output
fi 
