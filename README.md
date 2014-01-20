logErrorUtility
===============
 

Python Distutils package to fire  nginx log errors regulary at x interval of time daily.

Download .tar.gz file from link :    https://github.com/anilarya/logErrorUtility/blob/master/dist/logparser-utility-1.0.tar.gz


Installtion steps : 

1. Run [ $tar -xzvf logparser-utility-1.0.tar.gz] to extract .tar.gz files in current directory

2. Do [$ cd  logparser-utility.1.0 ] and do [$ ls] , You will see setup.py file and other project directories.

3. Run [$ sudo python setup.py install] 

4. This will run post bash scripts in background to enter details like a) logpath b) email-ids

5. This will set cronjob to run utils.py script to parse logs and sends mail about log errors.


Pre installation steps -[ Creation of distribution Packages ]  

1.Make setup.py file in parent project directory. 

What is setup.py?   Refer links :
http://stackoverflow.com/questions/1471994/what-is-setup-py
http://docs.python.org/2/distutils/setupscript.html

2. Make MANIFEST.in file to include non-python files or directories in same folder where setup.py exists.

3. Command to create source distribution in current directory :   $ python setup.py sdist 

This will create dist directory in current folder having  logparser-utility.1.0.tar.gz file

4. Do [$ cd dist]  and run [ $tar -xzvf logparser-utility-1.0.tar.gz] to extract .tar.gz files in current directory

5. Do [$ cd  logparser-utility.1.0 ] and do [$ ls] , You will see setup.py file and other project directories.
