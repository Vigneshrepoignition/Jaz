import re
import json
import urllib2, urllib
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
#URLPath = system.tag.read("[default]JMES_InternalTags/urlSITAPI").value

def getAllArea():
	try:	
		scriptName='GetAllArea'
		apiPath = "PlantHierarchyArea/GetAreas"
		Tag1 = "areaName"
		Tag2 = "areaId"
		
		url = URLPath + apiPath
		print url
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
		for i in resultData:	
			Name = i.get(Tag1)
			ID = i.get(Tag2)
			myList = [ID,Name]
			print("ID:",ID," Name:",Name)
			dataList.append(myList)	
			
		headers = ["ID","Name"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails 
	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)	
		return None
		
def getLineList(areaID):
	try:
		scriptName='getLineList'
		apiPath = "PlantHierarchyMachine/GetEnterPrisePlantLinesOnAreaChange/"+str(areaID)
		Tag1 = "lineName"
		Tag2 = "lineId"
		
		
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
		for i in resultData['LineList']:	
		
			Name = i.get(Tag1)
			ID = i.get(Tag2)
			myList = [ID,Name] 
			print("ID:",ID," Name:",Name)
			dataList.append(myList)	
			
		headers = ["ID","Name"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)	
		return None
		
def getMachineLineWise(lineID):
	try:
		scriptName='getMachineLineWise'
		apiPath = "PlantHierarchyMachine/GetPlantHierarchyMachines_OnLineChange/"+str(lineID)
		Tag1 = "machineName"
		Tag2 = "machineId"
		
		
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
		print resultData
		for i in resultData:	
		
			Name = i.get(Tag1)
			ID = i.get(Tag2)
			myList = [ID,Name] 
#			print("ID:",ID," Name:",Name)
			dataList.append(myList)	
			
		headers = ["ID","Name"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)	
		return None
		
def getMachineName(mID):
	try:
		scriptName='getMachineName'
		apiPath = "PlantHierarchyMachine/GetMachines"
		
		machineName='0'
		
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
		for i in resultData:	
			
			machineID = i.get("machineId")	
			
			if str(mID)==str(machineID):
				
				machineName= i.get("machineName")	
				break
		return machineName
	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		print 'error '+str(errorMessage)
		Authentication.exceptionLogger(errorMessage)	
		return None			 
