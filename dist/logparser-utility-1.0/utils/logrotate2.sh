#!/bin/bash
# A bash script to rotate log files
# $Id: log_rotation.sh 77 2006-07-27 22:52:49Z ben $
 
# Configuration
 
# Directories (no trailing slashes)
log_directory="/home/arya/apps/logErrorUtility/utils"
archive_directory="/home/arya/apps/logErrorUtility/utils/ziplog"
 
# Max size of a log file (bytes)
max_size="250000"
 
cd "$log_directory"
 
# Main loop
while [ "1" ]
do
	# Loop through files in log_directory
	for file in *
        do
		echo $file
		[ -f "$file" ] || continue # ignore directories and things
 
		filesize=$(stat -c%s "$file")
 
		# This log needs rotating
		if [ $filesize -ge $max_size ]; then
			# Number the filenames
			i=0
			while [ "1" ]
			do
			 	if [ -f "$archive_directory/$file.$i.gz" -o -f "$archive_directory/$file.$i" ]; then
					((i++))
				else
					break
				fi
			done
 
			mv -f "$file" "$archive_directory/$file.$i"
			gzip -f "$archive_directory/$file.$i"
 
		fi
	done
 
	sleep 5
done
