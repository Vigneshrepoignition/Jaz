#------------Move Url To Internal Tag-------------------------------
import re
import json
import urllib2, urllib
#----------------Get Records Scripts-----------------------------
URLTag = system.tag.read("[default]JMES_InternalTags/urlAPI_zag")
#URLPath = system.tag.read("[default]JMES_InternalTags/urlSITAPI").value
URLPath = URLTag.value
#	printerIP ='172.19.83.39'		#	JE QA Client Side
#	printerIP ='172.28.29.59'		#	Local
#	printerIP = '10.252.140.67'		# 	CNS BA Line Printer IP
# 	printerIP ='172.19.83.39'
printerIP ='10.252.140.67'

def printPackingLabel(item):
	from java.net import Socket
	from java.io import DataOutputStream	
#	printerIP='172.19.83.39'		#JE QA Client Side    # 172.19.83.50
#	printerIP = '172.19.83.50'
#	printerIP='172.28.29.59'		#Local
	port = 9100
	scriptName = 'shared.production.printLogLabels '
	try:
	# Open Socket Connection
		system.perspective.print("print start")
		clientSocket = Socket(printerIP,port)	
		system.perspective.print("print start1")
		outToPrinter = DataOutputStream(clientSocket.getOutputStream())
		system.perspective.print("print start2")
#		outToPrinter.write(PrintFile)#Code for dynamic print
#     	Code For test
#		item = 'test ignition an ba'
		PrintFile = "<STX><ESC><E2<CAN><ETX><STX><ESC>F1<LF>" + str(item) + "<ETX><STX><ETB><ETX>"
		outToPrinter.write(PrintFile)
		system.perspective.print(PrintFile)
#     Code For test End		
		outToPrinter.close();
		clientSocket.close();
		system.perspective.print("print start4")
		system.perspective.print("print end")
		return True
	except:
		system.perspective.	print(scriptName + str(sys.exc_info()[1]))		
	#		print(scriptName + str(sys.exc_info()[1]))	
		return False	
		
def printingServer(PrintFile,NoOfPrint,printerIP,port):	
	from java.net import Socket
	from java.io import DataOutputStream
	import socket
	import sys	
#	printerIP = '172.19.83.39'		#JE QA Client Side
#	printerIP = '172.28.29.59'		#Local
#	printerIP = '10.252.140.67'		# CNS BA Line Printer IP
#	port = 9100	
	port = int(port)
	scriptName = 'shared.production.printLogLabels No of Print '
	try:
	# Open Socket Connection
#		system.perspective.print("print start")
		clientSocket=Socket(printerIP,port)	
#		system.perspective.print("print start1")
		outToPrinter=DataOutputStream(clientSocket.getOutputStream())
#		system.perspective.print("print start2")
		for i in range(NoOfPrint):
			outToPrinter.write(PrintFile)#Code for dynamic print
#			system.perspective.print("for loop PrintFile inside function "+ (PrintFile))
		outToPrinter.close();
		clientSocket.close();
#		system.perspective.print("DONE TRue")
#		system.perspective.print("print start4")
#		system.perspective.print("print end")
		return True
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
#		system.perspective.print("errorMessage ="+str(errorMessage))
		print errorMessage
		Authentication.exceptionLogger(errorMessage)
#		system.perspective.print("errorMessage " +str(errorMessage))
		return False
			
def printingServertest():	
	import socket
	import sys	
	tcp_ip = '172.19.83.39'#QA Client Side
#	tcp_ip = '172.28.29.59'#Local
	tcp_port = 9100
	try:
		scriptName = 'shared.production.printLogLabels '
		print("print start")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("before print port socket =" +str(s))
		s.connect((tcp_ip, tcp_port))
		print("after print port")
		item='test ignition not an bb'
		MESSAGE = "<STX><ESC><E2<CAN><ETX><STX><ESC>F1<LF>" + str(item) + "<ETX><STX><ETB><ETX>"		
		s.send(MESSAGE)
		s.close()
		return True	
	except:
		print(scriptName + str(sys.exc_info()[1]))	
		return False	

def printingServerUploadFile(PrintFile):	
	from java.net import Socket
	from java.io import DataOutputStream
	import socket
	import sys
	system.perspective.print("mANUAL PRINT "+str(PrintFile))
	printerIP = '172.19.83.39'#JE #QA Client Side
#	printerIP = '10.252.140.67'	
##	printerIP = '172.28.29.59'#Local
	port = 9100
	scriptName = 'shared.production.printLogLabels '
	try:
#		Open Socket Connection
#		system.perspective.print("print start")
#		system.perspective.print("PrintFile "+str(PrintFile))
		clientSocket=Socket(printerIP,port)	
#		system.perspective.print("print start1")
		outToPrinter=DataOutputStream(clientSocket.getOutputStream())
#		system.perspective.print("print start2")		
		outToPrinter.write(PrintFile)#Code for dynamic print
		outToPrinter.close();
		clientSocket.close();
#		system.perspective.print("print start4")
#		system.perspective.print("print end")
		return True
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
#		system.perspective.print("errorMessage ="+str(errorMessage))
		print errorMessage
		Authentication.exceptionLogger(errorMessage)
		return False

#----------------------------------------------------------------------------------
# Description  : This Function is used for Lable Auto Printning
# Created By   : Sagar Iparkar
# Modified By  : Sagar Iparkar
# Modified On  : 30-05-2023

#----------------------------------------------------------------------------------  
def printfile():
    ContainerList= PackingAndLabelling.getnotPrintedContainer()
    print 'ContainerList ',ContainerList
    Type='Container'
#    labelTypeId=2
    if ContainerList!=[]:
        for i in (ContainerList):
            Number=i.get('ContainerName')
            number=i.get('ContainerName')
            WorkorderId=i.get('WorkOrderID')
            labelTypeId=i.get('PackingLabelId')
            type=i.get('PackingLabelId')
            workOrderNumber=i.get('WorkOrderNo')
#            printFile=PackingAndLabelling.GetWorkOrderPackingConfigurationTemplate(workOrderNumber,Number,labelTypeId)
            printFile= PackingAndLabelling.GetWorkOrderPackingConfigurationTemplate(WorkorderId,number,type)
            print printFile
            NoOfPrint=int(1)
            printedBy=1
            lineId=0
            dsPrintlist=PrinterConfiguration.GetWONumberLineWisePrinterDetails(lineId,WorkorderId)
            if len(dsPrintlist)>0:
                for i  in     dsPrintlist:
                    PrinterId= i['PrinterId']
                    PrinterName= str(i['PrinterName']).strip()
                    PrinterIP= str(i['PrinterIP']).strip()
                    Port= str(i['Port']).strip()
                    LineId = str(i['LineId']).strip()
                    break
                print "PrinterIP "+str(PrinterIP)
                print "Port " +str(Port)
                if     str(PrinterIP).strip()=='' or str(PrinterIP).strip()==None or str(PrinterIP).lower().strip()=='none' or  str(PrinterIP).lower().strip()=='null':
                    pass
                elif str(Port).strip()=='' or str(Port).strip()==None or str(Port).lower().strip()=='none' or  str(Port).lower().strip()=='null':
                    pass
                else:    
                    serverprint=Print.printingServer(printFile,NoOfPrint,PrinterIP,Port)
                    print "serverprint "+str(serverprint)
                    if serverprint==True or serverprint=='True' or serverprint=='true':
                        workOrderNumber=workOrderNumber
                        containerName=Number
                        PackingAndLabelling.PrintNumberPacking(Number,labelTypeId,printedBy,NoOfPrint,WorkorderId)
                        containerstatusupdate=PackingAndLabelling.updatecontainerprintingstatus(workOrderNumber,containerName)
