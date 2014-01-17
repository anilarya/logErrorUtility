#!/bin/bash
sudo scp  -C -i ~/.ssh/Platform_Dev.pem ec2-user@gateway.hmadev.com:/tmp/access.log /home/arya/apps/logErrorUtility/

