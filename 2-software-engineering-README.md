Project Title
This script is developed as part of an assessment for Xin Li to qualify for the AWS Fully Managed Cloud Services QA Engineering Consultant opening at 47Lining. In particular, for part-2 software-engineering programming skill testing.

Getting Started
Please download a copy of process-batch.py python script from Xin's deliverable; I also provides a process-batch.zip file in case any binary issue during transfer.  You can simply run below command from linux terminal to unzip:
# unzip process-batch.zip 

Prerequisites
The script is written with python3, so please be sure the linux system has python3 installed at /usr/bin/python3

Installing
Nothing needs to install other than meeting the prerequistites above and make sure the script is executable

Running the tests
1. chmod +x process-batch.py
2. ./process-batch.py
3. It will ask you to input the path for the json batch file. E.g. /home/bitnami/batch-09.json or batch-09.json  

Execution time:
It will depend on the underlinging architeture of the linux OS.  The script will take some time to complete because of looping iteration.  In my AWS t2.micro linux vm, it takes about 2 mins to finish.  

Output
It will has STDOUT output to the screen as well as create 4 json file as requested:
is-invalid-batch.json
waste-metric.json
one-swap-recommendation.json
two-swap-recommendation.json

Error handling:
1. Test if the path of json file does not constitute a valid file
2. Verify the json file has 54 lines, with opening and closing line as [ and ]
3. Validates from line 2 to line 53, the first character is within "A23456789JQK" & "10" and the second/final character is within "CHSD"
4. Verify this batch consists of each of the possible 52 entries in a specified order

Valid Test Case;
1. My logic includes a checking when the original batch is already at best waste metric for either one-wap or two-swap, though the sample input file did not contain this pattern.
