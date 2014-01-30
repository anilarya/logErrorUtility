1. Use this logparser-utility for following reasons : 
    *To see 5xx errors, 4xx errors and 2xx  counts  from log file  in  a tabular format.
    *To analyze these errors in pi-charts.
    *To see all 5xx errors in attached file.
    *To see general log info in other txt file. Like --
        -Slow urls > 2.0 ms and number of hits.
        -ClientIPs with number of requests made .
        -Average Number of requests per Hour.

2. Need to update only one file settings.py for log configuration purpose. Like  : 
    Project Name , Logpath,  Name of App web server, Recipient-email-id , SMTP settings.
                                            or
    simply use following command line arguments without looking into settings.py file

3. After making modification in settings.py file , Run following command to run handler.py file to    
    parse log files to fetch general log info : 
    
===============================================================================
   $ python utils/handler.py   # It takes user info from settings.py   

------------------------------or from Command Line Arguments-----------------------------------------------
   $ python handler.py Lithium-dashboard-Qa  e-xzrtpezf2s  /home/arya/Desktop/log apache  anil.kumar@hashedin.com     
   
Arguments explanation :  
python handler.py <environment_name/projectName-env> <environment-Id> <logpath> <server_name> <mailTo>                                    
====================================================================================

4. This sends mail reports to given recipients email-Ids.
