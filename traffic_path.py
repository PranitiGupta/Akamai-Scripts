#!/usr/bin/python
import re
import subprocess
import sys, argparse
def getInput():
    parser= argparse.ArgumentParser()
    parser.add_argument('-s', help="Source IP")
    parser.add_argument('-d', help="Destination IP")
    args= parser.parse_args()
    if args.s==None or args.d==None:
        print "Arguments are missing. \n usage: traffic_path [-h] [-s Ghost IP who want to NSH to] [-d Origin IP]"
        sys.exit()
    else:
        sourceIP= str(args.s)
        destinationIP= str(args.d)
    return (sourceIP, destinationIP)

def getMTR():
    print "NSHing to the ghost to get MTR outout. This takes few seconds..."
    command= "nsh "+sourceIP+" mtr "+destinationIP
    try:
        mtr= subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        return mtr
    except subprocess.CalledProcessError:
        print "Error! Please check if the IPs are correct."
        sys.exit()
        
    
def getListOfHops(mtr):
    IPList= list()
    asList= mtr.split("\n")
    for line in asList:
        m= "(\S{1,3}\.){3}\S{1,3}"
        obj= re.search(m, line, re.I|re.M)
        if obj:
            IPList.append(obj.group())
    return IPList

def getISP():
    finalList= list()
    IPList= getListOfHops(mtr)
    for IP in IPList:
        command1= "es_pro "+IP+" | grep -v '#' | cut -d' ' -f17"
        command2= "es_pro "+IP+" | grep -v '#'| cut -d' ' -f2,3,4,5"
        company= subprocess.check_output(command1, stderr=subprocess.STDOUT, shell=True).replace("\n","")
        location= subprocess.check_output(command2, stderr=subprocess.STDOUT, shell=True).replace("\n", "")
        ISP= company.split(":")[1]
        output= ISP +" ("+location+")"
        finalList.append(output)
    return finalList

def final_output():
    #removing duplication and modifying display
    finalList= getISP()
    noDup= list() #list with no duplicates
    for i in finalList:
        if i not in noDup:
            noDup.append(i)
    print noDup[0],
    for i in range(1,len(noDup)):
        print "-->"+noDup[i]+" ",
    
if __name__ == '__main__':
    sourceIP, destinationIP= getInput()
    mtr= getMTR()
    final_output()
    
    
