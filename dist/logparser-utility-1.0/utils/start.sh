#!/bin/bash
#Use link for logRotation : http://kb.site5.com/cron-jobs/how-to-run-a-script-using-a-cron-job/
#author :  Anil Arya

read -e -p "Enter the path to the log directory: " -i "/var/log/ngnix" LOGPATH
read -e -p "Enter comma separated recepient email-ids:" EMAIL

CURRENT_DIR="`pwd`" 
COMMAND="python $CURRENT_DIR/utils/utils.py 2014-08-01T21:12:12 2014-08-01T23:12:12 $LOGPATH $EMAIL"
JOB="*/2+1 * * * * $COMMAND"

cat <(fgrep -i -v "$COMMAND" <(crontab -l)) <(echo "$JOB") | crontab -

COMMAND1="bash $CURRENT_DIR/utils/logrotate.sh $LOGPATH/access.log"
JOB1="*/2+1 * * * * $COMMAND1"

cat <(fgrep -i -v "$COMMAND1" <(crontab -l)) <(echo "$JOB1") | sudo crontab -

#read -e -p "Select time structure: dof = date of month[1-31] ;mon= month[1-12] ; dow = date of week[0-6] ; own =Complete cronjob pattern * * * * * *:    
#-- min 
#-- hour
#-- dom 
#-- mon 
#-- dow 
#-- own
#Enter your text option :" yn
#case $yn in 
#    min ) read -e -p "Enter time in min. to set cron job :" MIN;;
#    hour) read -e -p "Enter time in hour to set cron job :" HOUR;;
#    dom ) read -e -p "Enter date of month to set cron job :" DOM;;
#    mon ) read -e -p "Enter month to set cron job :" MON;;
#    dow ) read -e -p "Enter date of week to set cron job :" DOW;;
#    own ) read -e -p "Complete standard pattern [min hour dom mon dow] to set cron job :" OWN;;
#esac
#if [ "-1${MIN}" -ne -1 ] ;then
#    JOB="*/$MIN+1 * * * * $COMMAND"
#    
#elif [ "-1${HOUR}" -ne -1 ];then
#    JOB="0 */$HOUR * * *  $COMMAND"
#
#elif [ "-1${DOM}" -ne -1 ];then
#    JOB="* */$DOM * * * $COMMAND"
#    
#elif [ "-1${MON}" -ne -1 ];then
#    JOB="* * */$MON * * $COMMAND"
#    
#elif [ "-1${DOW}" -ne -1 ];then
#    JOB="* * * */$DOW * $COMMAND"
#    
#elif [ -n "${OWN}" ];then
#    JOB="$OWN $COMMAND"
#fi
