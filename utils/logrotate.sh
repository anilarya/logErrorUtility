#!/bin/bash
 
## Check user input a log file.
if [ "$1" = "" ]; then
	echo "ERROR: You did not input the log file name."
	exit 1
fi
 
logfile=$1
 
## Check to make sure the input file is real.
if [ ! -f $logfile ]; then
	echo "I could not find that log file. Please check the filename and try again."
	exit 1
fi
 
## Check to see if the user inputs a custom output dir.
if [ "$2" = "" ]; then
	echo "I see you don't want to save the old log file to a custom directory, thats fine."
	echo "We will just save it here: "
	echo "-------------------------------------"
	pwd
	echo "-------------------------------------"
	dest=$(pwd)
	echo; echo
else
	dest=$2
	if [ ! -d $dest ]; then
		echo "The file destination you gave does not exist. We are going to stop now." 
		exit 1
	fi
fi
 
timestamp=`date +%Y:%m:%d`
newlogfile=$logfile.$timestamp
 
if [ -f $dest/$newlogfile.zip ]; then
	echo $newlogfile.zip "already exists. I changed the filename to prevent data loss."
	extra=$(date +"%H:%M:%S")  
	newlogfile=$newlogfile.$extra
	echo
	echo "The name of the new rotated logfile is now:"
	echo "-------------------------------------"
	echo $newlogfile.zip
	echo "-------------------------------------"
fi
 
cat $logfile > $dest/$newlogfile

#Empty logfile : Ready to accept another log
#> $logfile
 
echo
echo "I have copied the information from:"
echo "====================================="
echo $(pwd)/$logfile
echo "----------------- TO ----------------"
echo $dest/$newlogfile.zip
echo "====================================="
echo "Original log file is not blank now and ready to accept more logs."
touch $logfile
/usr/bin/zip -m $dest/$newlogfile.zip $dest/$newlogfile

