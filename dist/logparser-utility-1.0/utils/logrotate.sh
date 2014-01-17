#!/bin/bash
 
## Check user input a log file.
if [ "$1" = "" ]; then
	echo "ERROR: You did not input the log file name."
	exit 1
fi
echo $1
logfile=$1
 
## Check to make sure the input file is real.
if [ ! -f $logfile ]; then
	echo "I could not find that log file. Please check the filename and try again."
	exit 1
fi

#(path=($1)
#IFS=/
#ary=($path)
#logname=${ary[$((${#ary[@]} - 1))]}
#)
#echo  "I am here"
#echo $logname

timestamp=`date +%Y:%m:%d` 
newlogfile=$logfile.$timestamp

if [ -f  $newlogfile.zip ]; then
    echo $newlogfile.zip "already exists. I changed the filename to prevent data loss."
	extra=$(date +"%H:%M:%S")  
	newlogfile=$newlogfile.$extra
	echo
	echo "The name of the new rotated logfile is now:"
	echo "-------------------------------------"
	echo $newlogfile.zip
	echo "-------------------------------------"
fi

    cat $logfile > $newlogfile

    #Empty logfile : Ready to accept another log
    #> $logfile
 
    echo
    echo "I have copied the information from:"
    echo "====================================="
    echo  $logfile
    echo "----------------- TO ----------------"
    echo  $newlogfile.zip
    echo "====================================="
    echo "Original log file is not blank now and ready to accept more logs."
    touch $logfile
    /usr/bin/zip -m $newlogfile.zip $newlogfile
    
 
