import re
import json
import urllib2, urllib
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
#URLPath = system.tag.read("[default]JMES_InternalTags/urlSITAPI").value

#------------Get--Entersprise-List--------------------------------------------------
def getEnterpriseList(UserId):
	try:
		scriptName = "API: Get Enterprise List"
		apiPath = "OperatorConsole/GetAuthorizedEnterpriseForUserforOperatorConsole?UserId="+str(UserId)
		url = URLPath + apiPath
#		request = urllib2.Request(url)
#		response=urllib2.urlopen(request)
#		data = system.net.httpGet(url)
#		resultData= system.util.jsonDecode(data)
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:
			resultData=data.json
		dataList = []
		oprList =[]
		for i in resultData:	
			ID = i.get("EnterpriseId")
			Name = i.get("EnterpriseName")
			myList = [ID,Name]
			if Name not in oprList:
				print 'List',myList
				dataList.append(myList)	
				oprList.append(Name)
			else:
				continue
#			dataList.append(myList)	
		
		headers = ["ID","Name"]
		resultDetails = system.dataset.toDataSet(headers,dataList)		
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)

#------------Get--Plant-List--------------------------------------------------

def getPlantList(enterpriseID,UserId):
	try:
		scriptName = "API: Get Plant List"
		apiPath = "OperatorConsole/GetAuthorizedPlantForUserforOperatorConsole?UserId="+str(UserId)+"&EnterpriseId="+str(enterpriseID)
		url = URLPath + apiPath
#		request = urllib2.Request(url)
#		response=urllib2.urlopen(request)
#		data = system.net.httpGet(url)
#		resultData= system.util.jsonDecode(data)
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData=data.json
		dataList = []
		oprList = []
		for i in resultData:	
			ID = i.get("PlantId")
			Name = i.get("PlantName")
			myList = [ID,Name]
			if Name not in oprList:
				dataList.append(myList)	
				oprList.append(Name)
			else:
				continue
			
		headers = ["ID","Name"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		
#------------Get--Area-List--------------------------------------------------

def getAreaList(enterpriseID,plantID,UserId):
	try:
		scriptName = "API: Get Area List"
		apiPath = "OperatorConsole/GetAuthorizedAreaForUserforOperatorConsole?UserId="+str(UserId)+"&EnterpriseId="+str(enterpriseID)+"&PlantId="+str(plantID)
		
		url = URLPath + apiPath

		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData=data.json
		dataList = []
		oprList = []
		for i in resultData:
			ID = i.get("AreaId")	
			Name = i.get("AreaName")
			myList = [ID,Name]
			if Name not in oprList:
				dataList.append(myList)	
				oprList.append(Name)
			else:
				continue
			
		headers = ["ID","Name"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
 	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)

#------------Get--Line-List--------------------------------------------------

def getLineList(enterpriseID,plantID,areaID,UserId):
	try:
		scriptName = "API: Get Line List"
		apiPath = "OperatorConsole/GetAuthorizedLineForUserforOperatorConsole?UserId="+str(UserId)+"&EnterpriseId="+str(enterpriseID)+"&PlantId="+str(plantID)+"&AreaId="+str(areaID)
	
		url = URLPath + apiPath
#		request = urllib2.Request(url)
#		response=urllib2.urlopen(request)
#		data = system.net.httpGet(url)
#		
#		resultData= system.util.jsonDecode(data)
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData=data.json
		dataList = []
		oprList = []
		for i in resultData:	
			ID = i.get("LineId")
			Name = i.get("LineName")
			myList = [ID,Name] 
			if Name not in oprList:
				dataList.append(myList)	
				oprList.append(Name)
			else:
				continue
			
		headers = ["ID","Name"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)

#------------Get--Machine-List--------------------------------------------------
def getMachineList(enterpriseID,plantID,areaID,lineID,UserId):
	try:
		scriptName = "API: Get Machine List"
		apiPath = "OperatorConsole/GetAuthorizedMachineForUserforOperatorConsole?UserId="+str(UserId)+"&EnterpriseId="+str(enterpriseID)+"&PlantId="+str(plantID)+"&AreaId="+str(areaID)+"&LineId="+str(lineID)
	
		url = URLPath + apiPath

		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData=data.json
		dataList = []
		oprList = []
		print resultData
		for i in resultData:	
			ID = i.get("MachineId")
			Name = i.get("MachineName")
			MachineDescription = i.get("MachineDescription")
			Name=Name+' / '+MachineDescription
			myList = [ID,Name] 
			if Name not in oprList:
				dataList.append(myList)	
				oprList.append(Name)
			else:
				continue
			
		headers = ["ID","Name"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)

def getMachineListCLRI(enterpriseID,plantID,areaID,lineID,UserId):
	try:
		scriptName = "API: Get Machine List"
		apiPath = "OperatorConsole/GetAuthorizedMachineForUserforOperatorConsole?UserId="+str(UserId)+"&EnterpriseId="+str(enterpriseID)+"&PlantId="+str(plantID)+"&AreaId="+str(areaID)+"&LineId="+str(lineID)
	
		url = URLPath + apiPath

		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData=data.json
		dataList = []
		oprList = []
		print resultData
		for i in resultData:	
			ID = i.get("MachineId")
			Name = i.get("MachineName")
			MachineDescription = i.get("MachineDescription")
			Name=Name+' / '+MachineDescription
#			Name = i.get("MachineName")
#			print Name
			myList = [ID,Name] 
			if Name not in oprList:
				dataList.append(myList)	
				oprList.append(Name)
			else:
				continue
			
		headers = ["ID","Name"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
#-----------------------

def getPlantHirarchyDetailsbyMachineId(enterpriseID,plantID,areaID,lineID,UserId):
	apiPath = "OperatorConsole/GetAuthorizedMachineForUserforOperatorConsole?UserId="+str(UserId)+"&EnterpriseId="+str(enterpriseID)+"&PlantId="+str(plantID)+"&AreaId="+str(areaID)+"&LineId="+str(lineID)
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	return resultData
	
	
def getPlantHirarchyDetailsbyLineId(enterpriseID,plantID,areaID,UserId):
	apiPath = "OperatorConsole/GetAuthorizedLineForUserforOperatorConsole?UserId="+str(UserId)+"&EnterpriseId="+str(enterpriseID)+"&PlantId="+str(plantID)+"&AreaId="+str(areaID)
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	return resultData

def getPlantHirarchyDetailsbyAreaId(enterpriseID,plantID,UserId):
	apiPath = "OperatorConsole/GetAuthorizedAreaForUserforOperatorConsole?UserId="+str(UserId)+"&EnterpriseId="+str(enterpriseID)+"&PlantId="+str(plantID)
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	return resultData
	
def getPlantHirarchyDetailsbyPlantId(enterpriseID,UserId):
	apiPath = "OperatorConsole/GetAuthorizedPlantForUserforOperatorConsole?UserId="+str(UserId)+"&EnterpriseId="+str(enterpriseID)
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	return resultData

def GetEnterPrisePlantLinesOnAreaChange(areaId):
	try:
		scriptName = "API: Get GetEnterPrisePlantLinesOnAreaChange"
		apiPath = "PlantHierarchyMachine/GetEnterPrisePlantLinesOnAreaChange/"+str(areaId)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:
			resultData=data.json
		print 'resultData',resultData
		dataList = []
		for i in resultData['LineList']:
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
		errorMessage=scriptName +' Exception : '+ str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		return None