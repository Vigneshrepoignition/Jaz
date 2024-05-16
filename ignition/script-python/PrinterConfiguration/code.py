import re
import json
import urllib2, urllib
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
#URLPath = system.tag.read("[default]JMES_InternalTags/urlSITAPI").value

def GetLineWisePrinterList(userID):
	try:
		scriptName = "API: Get GetLineWisePrinterList"
		apiPath = "PrinterConfiguration/GetLineWisePrinterList?AreaId="+str(userID)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData=data.json
		print 'resultData',resultData
		dataList = []
		SRNo=1
		for i in resultData:	
			PrinterId = i.get("PrinterId")
			PrinterName = i.get("PrinterName")
			PrinterIP = i.get("PrinterIP")
			Port = i.get("Port")
			IsActive = i.get("IsActive")
			CreatedBy = i.get("CreatedBy")
			CreatedOn = i.get("CreatedOn")
			ModifiedBy = i.get("ModifiedBy")
			LineName= i.get("LineName")
			if str(ModifiedBy).strip()=='' or str(ModifiedBy).strip()=='None' or str(ModifiedBy).lower().strip()=='null':
				ModifiedBy=''
			ModifiedOn = i.get("ModifiedOn")
			if str(ModifiedOn).strip()=='' or str(ModifiedOn).strip()=='None' or str(ModifiedOn).lower().strip()=='null':
				ModifiedOn=''
			LineId = i.get("LineId")
			IsEnabled = i.get("IsEnabled")	
			View=""
			myList = [SRNo,PrinterId,PrinterName,PrinterIP,Port,LineName,IsActive,CreatedBy,CreatedOn,ModifiedBy,ModifiedOn,LineId,IsEnabled,View] 
			dataList.append(myList)
			SRNo=SRNo+1
				
		headers = ["SRNo","PrinterId","PrinterName","PrinterIP","Port","LineName","IsActive","CreatedBy","CreatedOn","ModifiedBy","ModifiedOn","LineId","IsEnabled","View"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		resultDetails = system.dataset.toPyDataSet(resultDetails)
		print 'resultDetails :',resultDetails
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		print 	errorMessage
		return None	
		


def addLineWisePrinter(lineList,printName,printIP,printPort,UserId,printerId,IsEnabled,IsActive):
	try: 
		scriptName="API:/ PrinterConfiguration/CreatePrinterConfiguration"
		apiPath = "PrinterConfiguration/CreatePrinterConfiguration"
		
		if IsEnabled==1 or str(IsEnabled)=='1' or str(IsEnabled==1).lower().strip()=='true':
			isEnabled=True	
		else:
			isEnabled=False
		if IsActive==1 or str(IsActive)=='1' or str(IsActive==1).lower().strip()=='true':
			IsActive=True	
		else:
			IsActive=False	
		IsActive=True
		isEnabled=True
		url = URLPath + apiPath	
		writeData={
		  "printerId": printerId,
		  "printerName": printName,
		  "printerIP": printIP,
		  "port": printPort,
		  "isEnabled": isEnabled,
		  "lineId": 0,
		  "lineIdList": lineList,
		  "isActive": IsActive,
		  "createdBy": UserId,
		  "createdOn": "2023-02-20T18:46:05.63Z",
		  "modifiedBy": 0,
		  "modifiedOn": "2023-02-20T18:46:05.63Z",
		  "isArchive": True
		}
		jsonParams = system.util.jsonEncode(writeData)		
		resultDetails = 0
		resultDetails = system.net.httpPost(url,'application/json',jsonParams)
#			system.perspective.print("resultDetails = ",resultDetails)
		print resultDetails
		return 1
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		print errorMessage
		system.perspective.print("errorMessage= ",errorMessage)
		return 0

def GetEnterPrisePlantLinesOnAreaChange(areaId):
	try:
		scriptName = "API: Get GetEnterPrisePlantLinesOnAreaChange"
#		apiPath = "PlantHierarchyMachine/GetEnterPrisePlantLinesOnAreaChange/"+str(areaId)
		apiPath = "PlantHierarchyLine/GetLines"
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData=data.json
		print 'resultData',resultData
		dataList = []
		
		for i in resultData:	
			lineId = i.get("lineId")
			lineName = i.get("lineName")	
			myList = [lineId,lineName] 
			dataList.append(myList)	
				
		headers = ["lineId","lineName"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		resultDetails = system.dataset.toPyDataSet(resultDetails)
		print 'resultDetails :',resultDetails
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)	
		return None	
		

def GetWONumberLineWisePrinterDetails(lineId,WorkorderId):
	try:
		scriptName = "API: Get GetLineWisePrinterList"
#		system.perspective.print("lineId "+str(lineId))
#		system.perspective.print("WorkorderId "+str(WorkorderId))
#		apiPath = "PrinterConfiguration/GetWONumberLineWisePrinterDetails?lineId="+str(lineId)+"&WONumber="+str(WONumber)
		apiPath = "PrinterConfiguration/GetWONumberLineWisePrinterDetails?lineId="+str(lineId)+"&workOrderId="+str(WorkorderId)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData=data.json
		dataList = []
		SRNo=1
		for i in resultData:	
			PrinterId = i.get("PrinterId")
			PrinterName = i.get("PrinterName")
			PrinterIP = i.get("PrinterIP")
			Port = i.get("Port")
			LineId = i.get("LineId")

		
			myList = [PrinterId,PrinterName,PrinterIP,Port,LineId]
			dataList.append(myList)
			SRNo=SRNo+1
				
		headers = ["PrinterId","PrinterName","PrinterIP","Port","LineId"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		resultDetails = system.dataset.toPyDataSet(resultDetails)
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print("errorMessage "+str(errorMessage))
		print 	errorMessage
		return None	
																						