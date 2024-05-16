import re
import json
import urllib2, urllib

URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
#URLPath = "http://172.16.35.201/JEMESWebAPIZAC/api/"

#http://172.16.35.201/JEMESWebAPIZAC/api/

def Login(loginId,Password):
	try:
		
		scriptName='Authentication Login Function'
		url=  URLPath + "Authentication/Post"

#		params={}		
		params ={
				"loginId": loginId,
				"password": Password			
				}
		jsonParams = system.util.jsonEncode(params)
		try:
			system.perspective.print("API URL is: "+str(url))
			system.perspective.print("API Method is: Post ")
			system.perspective.print("API Input Data:"+str(jsonParams))
		except:
			pass		
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		system.net.httpPost(url,'application/json',jsonParams)
		UserDeatils= system.util.jsonDecode(postReturn)
		return UserDeatils

	except:	
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		
#------------------------------------------------------------------------------	
# This function is used to update logs in operator console
# Inputs:  Error Message	
def exceptionLogger(errorMessage):
	logger = system.util.getLogger("MES Application")
	logger.error(errorMessage)
	
def getUserRoleId(userId):
	apiPath = "User/GetUser/"+str(userId)
	url = URLPath + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Get ")
	except:
		pass
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)
	i= system.util.jsonDecode(data)	
			
	RoleId = i.get("RoleId")
	RoleName = i.get("RoleName")	
	return RoleId 


def GetChineaseWords(Parameter1,Parameter2):
	apiPath = "OperatorConsole/GetOperatorConsoleNotes?WorkflowOperationsId="+str(Parameter1)+"&WorkOrderNo="+str(Parameter2)
	url = URLPath + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Get ")
	except:
		pass
	request = urllib2.Request(url)
	print"request",request
	response=urllib2.urlopen(request)
	print "response",response
	data = system.net.httpGet(url)
	print "data",data
	Data1 = data.format()
	return Data1
#		notesTimeStamp = today
#		myList = [notesId,notes,notesTimeStamp] 		
#		dataList.append(myList)	
#		
#	headers = ["NotesID","Notes","notesTimeStamp"]
#	resultDetails = system.dataset.toDataSet(headers,dataList)
def GetModulesForRole(roleId):
	try:
		
		scriptName="Authentication Modules For Role"
		apiPath =  "Authorization/GetModulesForRole/"+str(roleId)
		url = URLPath + apiPath	
		try:
			system.perspective.print("API URL is: "+str(url))
			system.perspective.print("API Method is: Get ")
		except:
			pass	
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		return resultData
	except:	
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		print errorMessage
		return None
		
		
#This Function which calls shift Id:-> Having dependencies please ensure before changing
def getshiftId(selectedLineId):
	apiPath ="OperatorConsole/GetCurrentShiftId?LineID="+str(selectedLineId)
	url = URLPath + apiPath
#	try:
#		system.perspective.print("API URL is: "+str(url))
#		system.perspective.print("API Method is: Get ")
#	except:
#		pass	

	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
 	Data = resultData[0]
 	ShiftId = Data.get('ShiftId')
 	print ShiftId
	return ShiftId
	
def GetAssignFormToUser(roleId):
	try:
		scriptName="Authentication Form For Role"
		apiPath =  "Form/GetAssignFormToUser/"+str(roleId)
		url = URLPath + apiPath		
#		url="http://172.28.3.251/FactoryMagixWebAPI/api/Form/GetAssignFormToUser/"+str(roleId)
		try:
			system.perspective.print("API URL is: "+str(url))
			system.perspective.print("API Method is: Get ")
		except:
			pass
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		return resultData
	except:	
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		print errorMessage
		return None