import re
import json
import urllib2, urllib
import datetime
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
#URLPath = system.tag.read("[default]JMES_InternalTags/urlSITAPI").value
	
def getUserAssignedWOList(enterpriseID,plantID,areaID,lineID,machineID,userId):	
 	apiPath = "OperatorConsole/GetOperatorConsoleWorkOrdersonInput?EnterpriseId="+str(enterpriseID)+"&PlantId="+str(plantID)+"&AreaId="+str(areaID)+"&LineId="+str(lineID)+"&MachineId="+str(machineID)+"&UserId="+str(userId)
	prin
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)
	
	resultData= system.util.jsonDecode(data)
	dataList = []
	j=1
	for i in resultData:			

		ID = j
		WoNumber = i.get("WorkOrderNo")
		Item = i.get("Item")
		Operation = i.get("Operations")
		Workflow = i.get("WorkflowName")		
		Process = i.get("Process")
		Quantity = i.get("Qty")
		Status = i.get("Status")		
		Completion = i.get("Completion")
		StartDate = i.get("PlannedStartDate")
		ActualStartDate = i.get("ActualStartDate")
		DueDate = i.get("DueDate")
		ActualCompletionDate = i.get("ActualCompleteDate")
		WorkflowOperationsId = i.get("WorkflowOperationsId"	)		
		WorkflowId = i.get("WorkflowId")	
		EnterpriseName = i.get("EnterpriseName")
		PlantName = i.get("PlantName")
		areaID= i.get("AreaId")
		areaName= i.get("AreaName")
		lineID= i.get("LineId")	
		lineName= i.get("LineName")
		machineID= i.get("MachineId")
		machineName= i.get("MachineName")
		revision = i.get("Revision")
		UOM = i.get("UOM")
		IO = i.get("IO")
		workOrderType = i.get("WorkOrderType")
		SubInventoryCode = i.get("SubInventoryCode")
		
				
		myList = [ID,WoNumber,Item,Operation,Workflow,Process,Quantity,Status,Completion,StartDate,ActualStartDate,DueDate,ActualCompletionDate,WorkflowOperationsId,"",WorkflowId,EnterpriseName,PlantName,areaID,areaName,lineID,lineName,machineID,machineName,revision,UOM,IO,workOrderType,SubInventoryCode] 		
		dataList.append(myList)	
		j = j+1
		
	headers = ["ID","WoNumber","Item","Operation","Workflow","Process","Quantity","Status","Completion","StartDate","ActualStartDate","DueDate","ActualCompletionDate","WorkflowOperationsId","View_Details","WorkflowId","EnterpriseName","PlantName","areaID","areaName","lineID","lineName","machineID","machineName","Revision","UOM","IO","workOrderType","SubInventoryCode"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails
#-------------------------------------------------------------------------Function END --------------------------------------------------------------------------------------------------------------------------	

def getOprConsoleShopNotes(WorkflowOperationsId,WorkOrderNo):
	apiPath = "OperatorConsole/GetOperatorConsoleNotes?WorkflowOperationsId="+str(WorkflowOperationsId)+"&WorkOrderNo="+str(WorkOrderNo)		   
	url = URLPath + apiPath
	
	client = system.net.httpClient() 
	data = client.get(url)
	if data.good:
		resultData=data.json
	dataList = []
	
	for i in resultData:			
		notesId = i.get("NotesId")
		notes = i.get("Notes")	
		notesTimeStamp =  i.get("AddedOn")
		AddedBy = i.get("AddedBy")
		myList = [notesId,notes,notesTimeStamp,AddedBy]
		print myList
		dataList.append(myList)
		
	headers = ["NotesID","Notes","notesTimeStamp",'AddedBy']
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails	
#-------------------------------------------------------------------------Function END --------------------------------------------------------------------------------------------------------------------------	
def getInstrumentList(Operation,WorkflowId,process,userId):			

	apiPath = "OperatorConsole/GetAttachedWorkFlowProcessActionLinksForOperatorConsole"
	url = URLPath + apiPath
	params = {
	
	  "workflowId": WorkflowId,
	  "workflowOperationId": Operation,
	  "workflowProcessId": process,
	  "headerName": "Add Instrument"  # It is hardcoded for Instrument list
	 }
	
	jsonParams = system.util.jsonEncode(params)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except:		
		result = 0
		postReturn = ''
		pass
	actualValue = 0
	resultData= system.util.jsonDecode(postReturn)
	
	dataList = []
	for i in resultData:
		ID = i.get("Links")	
		convertedDict = json.loads(ID)	
		for j in convertedDict:
			iD = j.get("id")		
			instrumentName = j.get("name")			
			myList = [iD,instrumentName] 		
			dataList.append(myList)		
			print(myList)
	headers = ["Id","Instrument Name"]
	resultDetails = system.dataset.toDataSet(headers,dataList)	

	return resultDetails	

#-------------------------------------------------------------------------Function END --------------------------------------------------------------------------------------------------------------------------	

def getSelectedOperationDetails(enterpriseID,plantID,areaID,lineID,machineID,UserId,WoNumber,Operation,Workflow):
	apiPath = "PlantHierarchyAuthorization/GetMachines/"+str(enterpriseID)+"/"+str(plantID)+"/"+str(areaID)+"/"+str(lineID)+"/"+str(UserId)+"/"+str(WoNumber)+"/"+str(Operation)+"/"+str(Workflow)
#--------------------------------------------- Define Variables to Read ----------------------	
	Tag1 = "Id"
	Tag2 = "WoNumber"
	Tag3 = "Item"
	Tag4 = "Operation"
	Tag5 = "Workflow"
	Tag6 = "Quantity"
	Tag7 = "Status"
	Tag8 = "Completion"
	Tag9 = "StartDate"
	Tag10 = "ActualStartDate"
	Tag11 = "DueDate"
	Tag12 = "ActualCompletionDate"
	Tag13 = "View_Details"		
#-----------------------------	
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)
	
	resultData= system.util.jsonDecode(data)
	dataList = []
	for i in resultData:			
		ID = i.get(Tag1)
		WoNumber = i.get(Tag2)
		Item = i.get(Tag3)
		Operation = i.get(Tag4)
		Workflow = i.get(Tag5)
		Quantity = i.get(Tag6)
		Status = i.get(Tag7)
		Completion = i.get(Tag8)
		StartDate = i.get(Tag9)
		ActualStartDate = i.get(Tag10)
		DueDate = i.get(Tag11)
		ActualCompletionDate = i.get(Tag12)
		View_Details = i.get(Tag13)			
			
		myList = [ID,WoNumber,Item,Operation,Workflow,Quantity,Status,Completion,StartDate,ActualStartDate,DueDate,ActualCompletionDate,View_Details] 		
		dataList.append(myList)	
		
	headers = ["ID","WoNumber","Item","Operation","Workflow","Quantity","Status","Completion","StartDate","ActualStartDate","DueDate","ActualCompletionDate","View_Details"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails 	

#-------------------------------------------------------------Function Used on Create Alert PopUp -----------------	
def getUsers():
	apiPath = "User/GetUsers"
	url = URLPath + apiPath

	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)
	
	resultData= system.util.jsonDecode(data)
	dataList = []
	for i in resultData:	
		UserID = i.get("UserId")
		FirstName = i.get("FirstName")
		LastName=i.get("LastName")
		UserName = FirstName + ' ' + LastName
		myList = [UserID,UserName] 		
		dataList.append(myList)	
		
	headers = ["EmployeeId","Username"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails
#--------------------------------------------
def getMESOnOffStatus(machineId):
    apiPath = "PlantHierarchyMachine/GetMachine/"+str(machineId)
    url = URLPath + apiPath
    request = urllib2.Request(url)
    response=urllib2.urlopen(request)
    data = system.net.httpGet(url)    
    resultData= system.util.jsonDecode(data)
    isMesOn    = resultData.get("isMesOn")
    return isMesOn 
#--------------------------------------------	

def getLastWOOperation(WorkflowId):
	apiPath = "OperatorConsole/GetFirstandLastOperationforOperatorConsole?WorkflowId="+str(WorkflowId)
	url = URLPath + apiPath
	
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)
	
	resultData= system.util.jsonDecode(data)
	dataList = []
	for i in resultData:	
		lastOperation = i.get("LastOperation")
		firstOperation = i.get("FirstOperation")
		myList = [firstOperation,lastOperation] 		
		dataList.append(myList)	
	
	headers = ["First_Operation","Last_Operation"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return lastOperation

def getFirstWOOperation(WorkflowId):
	apiPath = "OperatorConsole/GetFirstandLastOperationforOperatorConsole?WorkflowId="+str(WorkflowId)
	url = URLPath + apiPath

#	request = urllib2.Request(url)
#	response=urllib2.urlopen(request)
#	data = system.net.httpGet(url)
#	resultData= system.util.jsonDecode(data)
	
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	print "resultData",resultData
	SrNo=0
	
	dataList = []
	for i in resultData:	
		lastOperation = i.get("LastOperation")
		firstOperation = i.get("FirstOperation")
		myList = [firstOperation,lastOperation] 		
		dataList.append(myList)	
		
	headers = ["First_Operation","Last_Operation"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return firstOperation
#----------------------------------------------------------------------
# This function is shared between Operator Console and Warehouse Operator Console
def getReasonsCodes(mainReasonTypeId,subReasonTypeId):
	apiPath = "OperatorConsole/GetReasonCodeByInput?ReasontypeId="+str(mainReasonTypeId)+"&ReasaonsubtypeId="+str(subReasonTypeId)
#	url = URLPath + apiPath
#	request = urllib2.Request(url)
#	response=urllib2.urlopen(request)
#	data = system.net.httpGet(url)
#	resultData= system.util.jsonDecode(data)
	resultData=None
	url = URLPath + apiPath
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	print "resultData",resultData
	SrNo=0

	
	dataList = []
	for i in resultData:	
		reasonCodeId = i.get("Id")
		reasonCodeName = i.get("Name")
		myList = [reasonCodeId,reasonCodeName] 		
		dataList.append(myList)	
		
	headers = ["ReasonCodeId","ReasonCodeName"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails	
		
		
def saveCreatedAlert(WorkflowOperationsId,WoNumber,EmployeeID,ReasonCodeID,Comments,userID):
	apiPath = "OperatorConsole/CreateAlert"
	url = URLPath + apiPath
	writeData = {
	  "isActive": True,
	  "createdBy": userID,
	  "createdOn": "2022-07-01T04:10:27.339Z",
	  "modifiedBy": 0,
	  "modifiedOn": "2022-07-01T04:10:27.339Z",
	  "workOrderNo": WoNumber,
	  "alertReasonCodeId": ReasonCodeID,
	  "alertId": 0,
	  "alertComments": Comments,
	  "workflowOperationsId": WorkflowOperationsId,
	  "userId": EmployeeID
		}	
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		print("PostReturn",postReturn)
	except:		
		result = 0
		pass
	print(result)	
		
#---------------------------------------------------Functions used on ---------
def addShopNotes(WorkflowOperationsId,WoNumber,txtNotes,userID):
	apiPath = "OperatorConsole/CreateNotes"
	url = URLPath + apiPath	
	writeData = {
	  "isActive": True,
	  "createdBy": userID,
#	  "createdOn": "2022-07-01T04:10:27.339Z",
#	  "modifiedBy": 0,
#	  "modifiedOn": "2022-07-01T04:10:27.339Z",
	  "workOrderNo": WoNumber,
	  "notesId": 0,
	  "shopNotes": txtNotes,
	  "workflowOperationsId": WorkflowOperationsId
		}	
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		print("PostReturn",postReturn)
	except:		
		result = 0
		pass
	print(result)		

#---Get Single Row

def getSingleWORow(WorkflowOperationsId,WoNumber,Operations,WorkflowId,machineId):    
	apiPath = "OperatorConsole/GetOperatorConsolesingle"
	url = URLPath + apiPath
	params = {
	     "workOrderNo": WoNumber,
	     "workflowOperationsId": WorkflowOperationsId,
	     "operations": Operations,
	     "workflowId": WorkflowId,
	     "machineId": machineId
	      }
	jsonParams = system.util.jsonEncode(params)        
	result = 1
	try:
	    postReturn = system.net.httpPost(url,'application/json',jsonParams)    
	    print(postReturn)
	except:        
	    result = 0        
	    pass    
	resultData= system.util.jsonDecode(postReturn)
	print(resultData)
	dataList = []
	j=1
	for i in resultData:
	    ID = j
	    WoNumber = i.get("WorkOrderNo")
	    Item = i.get("Item")
	    Operation = i.get("Operations")
	    Workflow = i.get("WorkflowName")        
	    Process = i.get("Process")
	    Quantity = i.get("Qty")
	    Status = i.get("Status")
	    Completion = i.get("Completion")
	    StartDate = i.get("PlannedStartDate")
	    ActualStartDate = i.get("ActualStartDate")
	    DueDate = i.get("DueDate")
	    ActualCompletionDate = i.get("ActualCompleteDate")
	    WorkflowOperationsId = i.get("WorkflowOperationsId"    )        
	    WorkflowId = i.get("WorkflowId")
	
	    myList = [ID,WoNumber,Item,Operation,Workflow,Process,Quantity,Status,Completion,StartDate,ActualStartDate,DueDate,ActualCompletionDate,WorkflowOperationsId,WorkflowId]         
	    dataList.append(myList)    
	    j = j+1
	    print(myList)
	headers = ["ID","WoNumber","Item","Operation","Workflow","Process","Quantity","Status","Completion","StartDate","ActualStartDate","DueDate","ActualCompletionDate","WorkflowOperationsId","WorkflowId"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	print "resultDetails",resultDetails
	return resultDetails

#Update workOrder Status

def updateWorkOrderStatus(WoNumber,statusId):
	apiPath = "OperatorConsole/UpdateWorkOrderStatusForOperatorConsole"
	url = URLPath + apiPath		
	writeData = {
				  "workOrderNo": str(WoNumber),
				  "statusId": int(statusId)
				}
	jsonParams = system.util.jsonEncode(writeData)
	system.perspective.print("API WO Status update jsonParams--->"+str(jsonParams))		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		system.perspective.print("PostReturn",postReturn)
	except:	
		result = 0
		pass
	return result


#Start Operation---->
def startOperation(WorkflowOperationsId,WoNumber,WorkflowId,scanBadgeText,userID,machineId):	#machineId
	apiPath = "OperatorConsole/OperatorConsoleHistory"
	url = URLPath + apiPath		
	writeData = {
	  "createdBy": userID,
	  "workOrderNo": str(WoNumber),
	  "workflowOperationsId": WorkflowOperationsId,
	  "scanBadge": str(scanBadgeText),
	  "workflowId": int(WorkflowId),
	  "statusId": 1,
	  "machineId" : int(machineId)
		}
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		print("PostReturn",postReturn)
	except:		
		result = 0
		pass
	return result	
		
def holdOperation(WorkflowOperationsId,WoNumber,WorkflowId,scanBadgeText,holdReasonId,holdComment,userID,machineId):
	apiPath = "OperatorConsole/OperatorConsoleHistory"
	url = URLPath + apiPath
	writeData = {
	  "createdBy": userID,
	  "workOrderNo": WoNumber,
	  "workflowOperationsId": WorkflowOperationsId,
	  "scanBadge": scanBadgeText,
	  "holdReasonCodeId": holdReasonId,
	  "operatorConsoleComments": holdComment,	
	  "workflowId": WorkflowId,	
	  "machineId" : int(machineId),
	  "statusId": 2
	}
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		print("PostReturn",postReturn)
	except:		
		result = 0
		pass
	print(result)	
#-----------------------------------------------------------------------------------------
def resumeHoldOperation(WorkflowOperationsId,WoNumber,WorkflowId,scanBadgeText,resumeComment,userID,machineId):
	apiPath = "OperatorConsole/OperatorConsoleHistory"
	url = URLPath + apiPath
	writeData = {
	  "createdBy": userID,
	  "workOrderNo": WoNumber,
	  "workflowOperationsId": WorkflowOperationsId,
	  "scanBadge": scanBadgeText,	
	  "operatorConsoleComments": resumeComment,	
	  "workflowId": WorkflowId,	
	  "machineId" : int(machineId),
	  "statusId": 1	
	}
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		print("PostReturn",postReturn)
	except:		
		result = 0
		pass
	return result	
#-----------------------------------------------------------------------------------------
def completeOperation(operationsId,WoNumber,WorkflowId,scanBadgeText,goodQty,badQty,isPartialFlag,isFullFlag,commentText,userID,machineId):
	if badQty=="":
		badQty=0
	else:
		pass
	apiPath = "OperatorConsole/OperatorConsoleHistory"
	url = URLPath + apiPath
	writeData = {
	  "isActive": True,
	  "createdBy": userID,
	  "workOrderNo": WoNumber,	
	  "workflowOperationsId": operationsId,	
	  "scanBadge": scanBadgeText,	
	  "operatorConsoleComments": commentText,
	  "qualityGood": goodQty,
	  "qualityBad": badQty,
	  "isPartial": isPartialFlag,
	  "isFull": isFullFlag,	
	  "workflowId": WorkflowId,	
	  "machineId" : int(machineId),
	  "statusId": 3	
	}
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		print("PostReturn",postReturn)
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception:POC: Post Complete Operation  :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)	
		result = 0
		
	return result	
	
def updateDowntimes(WorkflowOperationsId,WoNumber,scanBadgeText,downtimeReasonId,commentText,lineID,machineId,userID):
	apiPath = "OperatorConsole/DownTimeOps"	
	url = URLPath + apiPath
	writeData = {
	  "isActive": True,
	  "createdBy": userID,
	  "createdOn": "2022-07-14T08:57:41.351Z",	
	  "workOrderNo": WoNumber,	
	  "workflowOperationsId": WorkflowOperationsId,	
	  "downTimeOpsId": 0,
	  "downTimeReasonCodeId": downtimeReasonId,
	  "systemStartDate": "2022-07-14T08:57:41.351Z",
	  "maintenanceEndDate": "2022-07-14T08:57:41.351Z",
	  "downTimeOpsScanBadge": scanBadgeText,	
	  "downTimeOpsComments": commentText,
	  "lineId": lineID,
	  "machineId": machineId,	
	  "statusId": 4
	}
	
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		print("PostReturn",postReturn)
	except:		
		result = 0
		pass
	print(result)

#---Add Downtime
def AddDowntime(WorkflowOperationsId,WoNumber,WorkflowId,userID,machineId):
	apiPath = "OperatorConsole/OperatorConsoleHistory"
	url = URLPath + apiPath
	writeData = {
	  "createdBy": userID,
	  "workOrderNo": WoNumber,
	  "workflowOperationsId": WorkflowOperationsId,
	  "workflowId": WorkflowId,	
	  "machineId" : int(machineId),
	  "statusId": 4,
	}
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		print("PostReturn",postReturn)
	except:		
		result = 0
		pass
	print(result)	

def getCharacteristicsDetails(WoNumber,workflowId,workflowOperationId,workflowProcessId,userID):		
	apiPath = "OperatorConsole/GetAttachedWorkFlowPAcharacteristicsForOperatorConsole"
	url = URLPath + apiPath
	params = {
	  "workOrderNo":WoNumber,
	  "workflowId": workflowId,
	  "workflowOperationId": workflowOperationId,
	  "workflowProcessId": workflowProcessId,
	  "headerName": "Add Characteristics",
	  "characteristicsTypeId": 1,	
	}
	jsonParams = system.util.jsonEncode(params)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except:		
		result = 0
		postReturn = ''
		pass
	
	resultData= system.util.jsonDecode(postReturn)
	#print(resultData)
	dataList = []
	for i in resultData:
		ID = i.get("Links")	
		LCL = i.get("LCL")
		UCL = i.get("UCL")	
		UOM = i.get("UOM")		
		selLinkID = i.get("SelectedLinkId")
		expectedValue = i.get("ExpectedValue")
		
		actualValue = i.get("ActualValue")
		InstumentName = i.get("InstrumentId")
		InstumentId = i.get("InstrumentId")
		InstrumentSrNo = i.get("InstrumentSerialNo")
		
		Minflag = i.get("Minflag")
		Maxflag = i.get("Maxflag")
		Nomflag = i.get("Nomflag")

		convertedDict = json.loads(ID)	
		k = 1
		for j in convertedDict:
			iD = j.get("id")
			SrNo = k		
			characteristicName = j.get("name")			
			myList = [SrNo,iD,characteristicName,LCL,UCL,UOM,expectedValue,actualValue,InstumentName,InstrumentSrNo,selLinkID,InstumentId,False,Minflag,Maxflag,Nomflag] 		
			dataList.append(myList)	
			k =k+1	
	
	headers = ["SrNo","CharacteristicsId","CharacteristicsName","LCL","UCL","UOM","ExpectedValue","ActualValue","InstumentName","InstrumentSrNo","primaryKey","InstrumentID","Disable_Limit","Minflag","Maxflag","Nomflag"]
	resultDetails = system.dataset.toDataSet(headers,dataList)	

	return resultDetails
#-----------------------------
def getCharacteristicsAttributeDetails(WoNumber,workflowId,workflowOperationId,workflowProcessId,userID):		
	apiPath = "OperatorConsole/GetAttachedWorkFlowPAcharacteristicsForOperatorConsole"
	url = URLPath + apiPath
	params = {
	  "workOrderNo":WoNumber,
	  "workflowId": workflowId,
	  "workflowOperationId": workflowOperationId,
	  "workflowProcessId": workflowProcessId,
	  "headerName": "Add Characteristics",
	  "characteristicsTypeId": 2,	
	}
	jsonParams = system.util.jsonEncode(params)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except:		
		result = 0
		postReturn = ''
		pass
	
	resultData= system.util.jsonDecode(postReturn)
	#print(resultData)
	dataList = []
	for i in resultData:
		ID = i.get("Links")	
		expectedValueId = i.get("ExpectedValueId")		
		expectedValueName = i.get("ExpectedValueName")
		isOk = i.get("IsOk")	
				
		convertedDict = json.loads(ID)	
		k = 1
		for j in convertedDict:
			iD = j.get("id")	
			SrNo = k	
			characteristicName = j.get("name")			
			myList = [SrNo,iD,characteristicName,expectedValueId,expectedValueName,isOk] 		
			dataList.append(myList)		
			k = k+1
	headers = ["SrNo","CharacteristicsId","CharacteristicsName","ExpectedValueId","ExpectedValueName","IsOk"]
	resultDetails = system.dataset.toDataSet(headers,dataList)	

	return resultDetails	
#----------------------------
def getComponentDetails(WoNumber,workflowId,operation,process):
	apiPath = "OperatorConsole/GetAttachedWorkFlowProcessActionLinksForOperatorConsole"
	url = URLPath + apiPath
	params = {
	  "workOrderNo":WoNumber,
	  "workflowId": workflowId,
	  "workflowOperationId": operation,
	  "workflowProcessId": process,
	  "headerName": "ADD PARTS TO BE consumed"
		}
	jsonParams = system.util.jsonEncode(params)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except:		
		result = 0
		postReturn = ''
		pass
	try:
		resultData= system.util.jsonDecode(postReturn)
	except:
		resultData = []				
	k=1
	dataList = []
	for i in resultData:
		ID = i.get("Links")	
		serialNo = i.get("SerialNo")	
		consumeQty = i.get("ConsumedQty")
		lotNo = i.get("LotNo")
		
		isAlternateBOM = True
		AlternateBOMName = "ABC11"
		AlternateBOMId = 111
		uom = "Unit"
		partDescription = "Part Description"
		revision = "A"
		
		convertedDict = json.loads(ID)	
		for j in convertedDict:
			SrNo = k
			ID = j.get("id")	
			componentName = str(j.get("name"))+"_"+str(revision)			
			myList = [SrNo,ID,componentName,serialNo,lotNo,consumeQty,isAlternateBOM,AlternateBOMName,AlternateBOMId,uom,partDescription] 		
			dataList.append(myList)	
			k = k+1			
	headers = ["SrNo","Id","Parameter","SerialNumber","LotNumber","ConsumeQty","isAlternateBOM","AlternateBOMName","AlternateBOMId","uom","partDescription"]
	resultDetails = system.dataset.toDataSet(headers,dataList)	
	return resultDetails
#--------------------------- Get Component details along with Substitute component details -------------------------
def getSubstitueComponentDetails(WoNumber,workflowId,operation,process):
	try:
		apiPath = "OperatorConsole/GetAttachedWorkFlowProcessComponentsWithSubstituteForOperatorConsole"
		url = URLPath + apiPath
		
		params = {
		  "workOrderNo":WoNumber,
		  "workflowId": workflowId,
		  "workflowOperationId": operation,
		  "workflowProcessId": process,
		  "headerName": "ADD PARTS TO BE consumed"
			}
		
		jsonParams = system.util.jsonEncode(params)			 
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)			
		except:		
			result = 0
			postReturn = ''
			pass
		try:
			resultData= system.util.jsonDecode(postReturn)		
		except:
			resultData = []				
		k=1
		dataList = []
		print str(resultData)
		for i in resultData:
			partNumber = i.get("PartNo")
			if str(partNumber).lower()!=str(None).lower() :
				SrNo = k
				ID = i.get("SelectedId")
				revision = i.get("Revision")
				componentName = i.get("PartWithRevision")   # str(partNumber)+"_"+str(revision)
				uom = i.get("UOMName")
				isSubstituteAvailableFlag = i.get("isSubstituteAvailable")
				SubstituteIdentification = i.get("SubstituteIdentification")		
				SubstituteItemId = i.get("SubstituteItemId")
				SubstituteItemPartNo = i.get("SubstituteItemPartNoWithRevision")	
				lotNo = i.get("LotNo")
				serialNo = 0					
				consumeQty = i.get("ConsumedQty")
				ComponentExpiryDate = i.get("ComponentExpiryDate")
				ERPTransferLot = MaterialRequestAPI.isNotBlank(i.get('TransferLot'))
				ERPTransferQty = MaterialRequestAPI.isNotBlank(i.get('TransferQty'))
				ERPFactoryName = MaterialRequestAPI.isNotBlank(i.get('FactoryName'))
				ERPVendorName = MaterialRequestAPI.isNotBlank(i.get('VendorName'))
				ERPExpirationDate=MaterialRequestAPI.isNotBlank(i.get('ExpirationDate'))
				ERPVendorCode = ''
				if str(ERPTransferQty) == "":
					ERPTransferQty = 'Qty Not Transfered'
				else:
					pass
				today = system.date.now()
				TodayDate= system.date.format(today, "dd/MM/yyyy,HH:mm:ss")
				ComponentExpiryDateDefault = "01/01/1900,00:00:00"
				
#				if ComponentExpiryDate >= TodayDate or ComponentExpiryDate == None or ComponentExpiryDateDefault == ComponentExpiryDate:
#					IsExpired = 0
#					print "Not Expired--->"
#				else:
#					IsExpired = 1
#					print "Expired-------> "
				print 'ERPExpirationDate',ERPExpirationDate
				system.perspective.print('ERPExpirationDate  FROM Script is: ' + str(ERPExpirationDate))
				system.perspective.print('ERPExpirationDate  FROM Script is: ' + str(type(ERPExpirationDate)))
				if ERPExpirationDate >= TodayDate or ERPExpirationDate == None or str(ERPExpirationDate).strip().lower() == str("None").strip().lower() or str(ERPExpirationDate).strip().lower() == str("null").strip().lower() or str(ERPExpirationDate).strip().lower() == str("").strip().lower():
					IsExpired = 0
					print "Not Expired--->"
					system.perspective.print('ERPExpirationDate : ' + str(ERPExpirationDate) + str( " || IsExpired  :" + str(IsExpired)))
				else:
					IsExpired = 1
					print "Expired------->"
					system.perspective.print('ERPExpirationDate : ' + str(ERPExpirationDate) + str( " || IsExpired  :" + str(IsExpired)))

				myList = [SrNo,ID,componentName,uom,isSubstituteAvailableFlag,SubstituteIdentification,SubstituteItemId,SubstituteItemPartNo,serialNo,lotNo,consumeQty,IsExpired,ERPTransferLot,ERPTransferQty,ERPFactoryName,ERPVendorName,ERPExpirationDate,ERPVendorCode] 		
				dataList.append(myList)
				k = k+1
			else:
				print 'No Record'
		headers = ["SrNo","Id","Parameter","uom","isSubstituteAvailableFlag","SubstituteIdentification","SubstituteItemId","SubstituteItemPartNo","SerialNumber","LotNumber","ConsumeQty","IsExpired","ERPTransferLot","ERPTransferQty","ERPFactoryName","ERPVendorName","ERPExpirationDate","ERPVendorCode"]
		resultDetails = system.dataset.toDataSet(headers,dataList)	
		return resultDetails
	except:
		exc_type, exc_obj,tb = sys.exc_info()
		errorMessage = "Error:"+ str(exc_obj)
		lineno = tb.tb_lineno
		print 'errorMessage:', errorMessage
		print 'LineNo', lineno

#---------------------------
def getAllWOComponentDetails(WoNumber,workflowId,goodQty):
	apiPath = "OperatorConsole/GetAttachedWorkFlowOperationsForOperatorConsole"
	url = URLPath + apiPath
	params = {
	  "workOrderNo":WoNumber,
	  "workflowId": workflowId,
	  "goodQty": goodQty
		}
	jsonParams = system.util.jsonEncode(params)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except:		
		result = 0
		postReturn = ''
		pass
	try:
		resultData= system.util.jsonDecode(postReturn)
	except:
		resultData = []			
	dataList = []
	j=1
	for i in resultData:
		SrNo = j	
		partNumber = i.get("PartNo")
		lotNo = i.get("LotNo")
		lotQty = i.get("LotQty")
		componentRevision = i.get("Revision")
		uom = i.get("UOMName")				
		myList = [SrNo,partNumber,0,lotNo,lotQty,componentRevision,uom] 		
		dataList.append(myList)	
		j = j+1			
	headers = ["Id","Parameter","SerialNumber","LotNumber","ConsumeQty","componentRevision","UOM"]
	resultDetails = system.dataset.toDataSet(headers,dataList)	
	return resultDetails
#----------------------------
def getAllWOComponentDetailsForPDAStart(WoNumber,workflowId):
	apiPath = "OperatorConsole/GetOperatorConsoleComponentDataForverification"
	url = URLPath + apiPath
	params = {
	  "workOrderNo":WoNumber,
	  "workflowId": workflowId	  
		}
	jsonParams = system.util.jsonEncode(params)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except:		
		result = 0
		postReturn = ''
		pass
	try:
		resultData= system.util.jsonDecode(postReturn)
	except:
		resultData = []			
	dataList = []
	j=1
	for i in resultData:
		SrNo = j	
		partNumber = i.get("PartNo")
		lotNo = i.get("LotNo")
		lotQty = i.get("LotQty")
		componentRevision = i.get("Revision")
		uom = i.get("UOMName")				
		myList = [SrNo,partNumber,0,lotNo,lotQty,componentRevision,uom] 		
		dataList.append(myList)	
		j = j+1			
	headers = ["Id","Parameter","SerialNumber","LotNumber","ConsumeQty","componentRevision","UOM"]
	resultDetails = system.dataset.toDataSet(headers,dataList)	
	return resultDetails	
#----------------------------
#def getChecklistWorkInstructionDetails(WoNumber,workflowId,workflowOperationId,workflowProcessId):
#	apiPath = "OperatorConsole/GetAttachedWorkFlowProcessActionLinksForOperatorConsole"
#	url = URLPath + apiPath	
#	params = {
#	  "workOrderNo": WoNumber,
#	  "workflowId": workflowId,
#	  "workflowOperationId": workflowOperationId,
#	  "workflowProcessId": workflowProcessId,
#	  "headerName": "Add Checklists"
#		}
#	jsonParams = system.util.jsonEncode(params)		
#	result = 1
#	try:
#		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
#	except:		
#		result = 0
#		postReturn = ''
#		pass
#	
#	resultData= system.util.jsonDecode(postReturn)
#	k = 1
#	dataList = []
#	for i in resultData:
#		ID = i.get("Links")	
#		parameter = i.get("Parameter")
#		isSelected = i.get("IsSelected")
#		if isSelected==1:
#			YesNo = True
#		else:
#			YesNo = False
#		convertedDict = json.loads(ID)
#			
#		for j in convertedDict:
#			Id = j.get("id")	
#			SrNo = k	
#			dataValues = j.get("name")						
#			myList = [SrNo,Id,dataValues,parameter,YesNo] 		
#			dataList.append(myList)		
#			k = k+1
#	headers = ["SrNo","Id","Type","Parameter","Yes_No"]
#	resultDetails = system.dataset.toDataSet(headers,dataList)	
#	
#	return resultDetails
	
	
	
def getChecklistWorkInstructionDetails(WoNumber,workflowId,workflowOperationId,workflowProcessId):
	apiPath = "OperatorConsole/GetAttachedWorkFlowProcessActionLinksForOperatorConsole"
	url = URLPath + apiPath	
	params = {
	  "workOrderNo": WoNumber,
	  "workflowId": workflowId,
	  "workflowOperationId": workflowOperationId,
	  "workflowProcessId": workflowProcessId,
	  "headerName": "Add Checklists"
		}
	jsonParams = system.util.jsonEncode(params)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except:		
		result = 0
		postReturn = ''
		pass
	
	resultData= system.util.jsonDecode(postReturn)
	print resultData
	k = 1
	dataList = []
	for i in resultData:
		ID = i.get("Links")	
		print 'ID-->'+str(ID)
		parameter = i.get("Parameter")
		isSelected = i.get("IsSelected")
		if isSelected==1:
			YesNo = True
		else:
			YesNo = False
		convertedDict = json.loads(ID)
		print "Convertd Dict--->"+str(convertedDict)	
		for j in convertedDict:
			Id = j.get("id")	
			SrNo = k	
			dataValues = j.get("name")
			checklistType = j.get("type")
									
		myList = [SrNo,Id,dataValues,parameter,checklistType,YesNo] 		
		dataList.append(myList)		
		k = k+1
	headers = ["SrNo","Id","Name","Parameter","checklistType","Yes_No"]
	resultDetails = system.dataset.toDataSet(headers,dataList)	
	
	return resultDetails

#-------------------------------------------------
def getChecklistMaterialAvailabilityDetails(WorkOrderNo,Item,Revision):
	apiPath = "OperatorConsole/GetOperatorConsoleMaterialAvailability?WorkOrderNo="+str(WorkOrderNo)+"&Item="+str(Item)+"&Revision="+str(Revision)
	url = URLPath + apiPath	
	
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)
	print(data)
	resultData= system.util.jsonDecode(data)
	print(resultData)
	dataList = []
	j=1
	for i in resultData:			
		SrNo = j
		componentName = i.get("PartNo")	
		bomQty = i.get("Bom_Qty")
		checkedStatus = i.get("IsChecked")	
		if checkedStatus==1:
			isChecked = True
		else:
			isChecked = False
			
		myList = [SrNo,componentName,bomQty,isChecked] 		
		dataList.append(myList)	
		j = j+1
		
	headers = ["SrNo","componentName","bomQty","isChecked"]
	resultDetails = system.dataset.toDataSet(headers,dataList)		
	return resultDetails 

#-------------------------------------------------

def getWorkInstructionTextDetails(WoNumber,workflowId,workflowOperationId,workflowProcessId):
	apiPath = "OperatorConsole/GetAttachedWorkFlowProcessActionLinksForOperatorConsole"
	
	
#	system.perspective.print("WoNumber = " +  str(WoNumber))
#	system.perspective.print("workflowId = " +  (workflowId))
#	system.perspective.print("workflowOperationId = " +  (workflowOperationId))
#	system.perspective.print("workflowProcessId = " +  (workflowProcessId))

	
	url = URLPath + apiPath
	params = {
	  "workOrderNo": WoNumber,
	  "workflowId": workflowId,
	  "workflowOperationId": workflowOperationId,
	  "workflowProcessId": workflowProcessId,
	  "headerName": "Add Work Instruction"
		}
	system.perspective.print("url= " + str(url))

	jsonParams = system.util.jsonEncode(params)		
	system.perspective.print("jsonParams = " +  (jsonParams))
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except Exception as e:		
		result = 0
		scriptName = "Operator Console:"
		errorMessage=scriptName  +' Exception : '+  str(e)
		Authentication.exceptionLogger(errorMessage)			
	else:		
		resultData= system.util.jsonDecode(postReturn)		
		dataList = []
		k=1
		for i in resultData:			
			ID = i.get("Links")				
			convertedDict = json.loads(ID)	
			for j in convertedDict:
				#SrNo = j.get("id")	
				SrNo = k
				dataValues = j.get("name")	
				k = k+1		
				fileName='NA'	
				filePath='NA'
				Link='NA'
			myList = [SrNo,dataValues] 		
			dataList.append(myList)				
		headers = ["SrNo","dataValues"]
#		headers = ["SrNo","fileName","filePath","Link","dataValues"]
		resultDetails = system.dataset.toDataSet(headers,dataList)	
		return resultDetails
#--------------------------------------------------
def getWorkInstructionAttachmentDetails(WoNumber,workflowId,workflowOperationId,workflowProcessId):
	apiPath = "OperatorConsole/GetAttachedWorkFlowProcessActionLinksForOperatorConsole"
	url = URLPath + apiPath
	params = {
	  "workOrderNo": WoNumber,
	  "workflowId": workflowId,
	  "workflowOperationId": workflowOperationId,
	  "workflowProcessId": workflowProcessId,
	  "headerName": "Add Work Instruction"
		}
	jsonParams = system.util.jsonEncode(params)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except Exception as e:		
		result = 0
		scriptName = "Operator Console:"
		errorMessage=scriptName  +' Exception : '+  str(e)
		Authentication.exceptionLogger(errorMessage)	
	else:
		resultData= system.util.jsonDecode(postReturn)		
		dataList = []
		j = 1
		for i in resultData:
			fileName = i.get("FileName")	
			filePath = i.get("Path")	
			Link='View'
			dataValues=''		
			myList = [fileName,filePath,Link] 					
			dataList.append(myList)		
			j = j+1
#		headers = ["SrNo","fileName","filePath","Link"]
		headers = ["fileName","filePath","Link"]
#		headers = ["SrNo","fileName","filePath","Link","dataValues"]
		resultDetails = system.dataset.toDataSet(headers,dataList)	
		return resultDetails
#-------------------------------
def postComponentDetails(WorkflowOperationsId,WoNumber,WorkflowId,operatorConsoleComponentId,selectedItemId,serialNo,lotNo,consumeQty,userId,IsExpired):
	apiPath = "OperatorConsole/CreateOperatorConsoleComponent"
	url = URLPath + apiPath		
	
	if IsExpired == int(1) or IsExpired == 1:
		IsExpired = True
	else:
		IsExpired = False	
	
	writeData = {	
	  "operatorConsoleComponents": [
	    {
	      "operatorConsoleComponentId": 0,
	      "selectedItemId": int(selectedItemId),
	      "serialNo": str(serialNo),
	      "lotNo": str(lotNo),
	      "consumedQty": int(consumeQty),
	      "operationId": WorkflowOperationsId,
	      "workflowId": WorkflowId,
	      "createdBy": userId,
	      "workOrderNo": WoNumber,
	      "IsActive": True,
	      "IsExpired": IsExpired
	    }
	  ]
	}
	
	
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except Exeption as e:		
		result = 0
		scriptName = "Operator Console:Post Component Details.."
		errorMessage=scriptName  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)
	return postReturn

def postChecklistDetails(WorkflowOperationsId,WoNumber,WorkflowId,operatorConsoleChecklistId,selectedChecklistId,selectedParameter,selectedTypeId,isSelected,userId,Notes):
	apiPath = "OperatorConsole/CreateOperatorConsoleChecklist"
	url = URLPath + apiPath	
	selectedTypeId = 0	
	if isSelected == 1:
		checkBoxResult = True
	else:
		checkBoxResult = False		
	writeData = {	
	  "operatorConsoleChecklists": [
	    {
	      "operatorConsoleChecklistId": 0,
	      "selectedChecklistId": selectedChecklistId,
	      "selectedParameter": selectedParameter,
	      "selectedTypeId": int(2),
	      "operationId": WorkflowOperationsId,	      
	      "workflowId": WorkflowId,
	      "createdBy": userId,
	      "workOrderNo": WoNumber,
	      "isSelected": checkBoxResult,
	      "isActive": True,
	      "Notes": Notes
	    }
	  ]	
	}	
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		system.perspective.print("PostReturn :" + str(postReturn))
	except:		
		result = 0
		postReturn=''
		pass
	return postReturn
#------------------------------------------------------------------
def postChecklistDetailsForMaterialAvailability(WoNumber,Item,Revision,partName,isChecked,userId):
	apiPath = "OperatorConsole/CreateOperatorConsoleMaterialAvailability"
	url = URLPath + apiPath	
	
	if isChecked == 1:
		isCheckedFlag = True
	else:
		isCheckedFlag = False		
	writeData =  {
	"operatorConsoleMaterialAvailability": [
		{
		     "operatorConsoleMaterialAvaliablityId": 0,
		     "workorderNo": WoNumber,
		     "item": Item,
		     "revision": Revision,
		     "partNo": partName,
		     "isChecked": isCheckedFlag,
		     "createdBy": userId,
		    # "machineId":machineId
		     "isActive": True    
		     }]
		    }
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)		
	except:		
		result = 0		
		pass
	return postReturn
#-----------------------------------------------------------------
def postCharacteristicsDetails(WorkflowOperationsId,WoNumber,WorkflowId,selectedCharacteristicsId,actualValue,instrumentId,instrumentSerialNo,userID):
	
	apiPath = "OperatorConsole/CreateOperatorCharacteristics"
	url = URLPath + apiPath		
	writeData = {	
	  "operatorConsoleCharacteristics": [
	    {
	      "operatorConsoleCharacteristicsId": 0,
	      "selectedCharacteristicsId": selectedCharacteristicsId,
	      "selectedCharacteristicsTypeId": 1,
	      "actualValue": float(actualValue),
	      "instrumentId": instrumentId,
	      "instrumentSerialNo": instrumentSerialNo,
	      "operationId": WorkflowOperationsId,
	      "workflowId": WorkflowId,
	      "createdBy": userID,
	      "workOrderNo": WoNumber,
	      "isActive": True
	    }
	  ]
	
	}
	
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		#print("PostReturn",postReturn)
	except:		
		result = 0
		pass
	return postReturn
	
#----------------------	
def postCharacteristicsAttributeDetails(WorkflowOperationsId,WoNumber,WorkflowId,selectedCharacteristicsId,isOk,userID):
	apiPath = "OperatorConsole/CreateOperatorCharacteristicsTypeAttribute"
	url = URLPath + apiPath	
	if 	isOk==1 or isOk==True or isOk=='true':
		isSelected = True 
	else:
		isSelected = False
	writeData = {	
	  "operatorConsoleCharacteristicsTypeAttribute": [
	    {
	      "operatorConsoleCharacteristicsId": 0,
	      "selectedCharacteristicsId": selectedCharacteristicsId,
	      "selectedCharacteristicsTypeId": 2,
	      "operationId": WorkflowOperationsId,
	      "workflowId": WorkflowId,
	      "createdBy": userID,
	      "isOk": isSelected,
	      "workOrderNo": WoNumber,
	      "isActive": True
	    }
	  ]
	
	}
	
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		#print("PostReturn",postReturn)
	except:		
		result = 0
		pass
	return postReturn

#---------------------------------------------------------------------------------------------
def postCompleteDetailsToERP(WoNumber,woLotNumber,workflowId,workOrderType,lineName,partNumber,revision,goodQty,UOM,IO,OU,subInventoryCode,ledger,locatorName,containerNo):
	apiPath = "ConsumptionProductionReporting/AddMaterialConsumptionProductionReporting"
	url = URLPath + apiPath		
	ComponentDetails = WorkOrderDetailsAPI.getAllWOComponentDetails(WoNumber,workflowId,goodQty)

			
	mydate = system.date.now()
	currentDate=system.date.format(mydate, "yyyy-MM-dd'T'HH:mm:ss.ss'Z'")   # Sample Date : "2022-07-28T09:21:13.614Z"
	
	componentList = []	
	for row in range(ComponentDetails.getRowCount()):
		compoName = ComponentDetails.getValueAt(row, "Parameter")
		compoLotNumber = ComponentDetails.getValueAt(row, "LotNumber")
		consumeQty = ComponentDetails.getValueAt(row, "ConsumeQty")	
		compoRevision = ComponentDetails.getValueAt(row, "componentRevision")
		compoUOM = ComponentDetails.getValueAt(row, "UOM")
		
		returnData = PackingAndLabelling.getComponentDetailsRelatedToWO(WoNumber)
		for woFields in returnData:					
			compoLocatorName = 	woFields.get("LocatorName")				
			compoSubInventoryCode = woFields.get("SubInventoryCode")		
		myDict = {
				"workOrderNumber": WoNumber,
		        "partNumber": compoName,
		        "revision": compoRevision,
		        "lotNumber": compoLotNumber,
		        "qty": str(consumeQty),
		        "uom": compoUOM,
		        "io": IO,  							# same as that of Production reporting
		        "subInventoryCode": compoSubInventoryCode,
		        "locatorName": compoLocatorName,
		        "sourceCode": "MES",
		        "workOrderType": workOrderType,		# same as that of Production reporting
		        "reason": "", 						# Not required
		        "reference": "",					# Not required
		        "datetime": currentDate,
		        "employeeNumber": "",				# Not required
		        "ledger": ledger, 					# same as that of Production reporting
		        "ou": OU, 							# same as that of Production reporting
		        "mfgLine": lineName					# same as that of Production reporting
		      }
		componentList.append(myDict)
		
#--------------	
	writeData = [
	  {
	    "productionReportings": [
	       {
	           "workOrderNumber": WoNumber,
	           "scheduledFlag": "",						# Not required
	           "mfgLine": lineName,
	           "containerName": str(containerNo),  # get ContainerNo
	           "partNumber": partNumber,
	           "revision": revision,
	           "lotNumber": woLotNumber,
	           "qty": str(goodQty),
	           "uom": UOM,
	           "io": IO,
	           "subInventoryCode": subInventoryCode,
	           "locatorName": locatorName,
	           "sourceCode": "MES",						# Fixed Field
	           "workOrderType": workOrderType,
       		   "reason": "",							# Not required
	           "reference": "",							# Not required
	           "datetime": "2022-07-28T09:21:13.614Z",
	           "employeeNumber": "",					# Not required
	           "ledger": ledger,
	           "ou": OU,
	           "actualStartDateTime": "",				# Not required
	           "actualEndDateTime": "",					# Not required
	           "isPartial": ""							# Not required
	         }
	    ],
	    "materialConsumptions": componentList
	  }
	]
	
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
		print("postReturn 1:"+str(postReturn))	
	except:		
		result = 0
		pass
	return result
#-----------------------------------------------------------------------------------------
def postPackingDetailsToERP(ResultData,WoNumber,lineName,containerType,qtyPerCarton,qtyInContainer):				
	apiPath = "Packing"
	for packingDetails in ResultData:	
		workOrderType = packingDetails.get("WorkOrderType")					
		woPartNumber = packingDetails.get("PartNumber")
		IO = packingDetails.get("IO")
		OU = packingDetails.get("OU")
		ledger = packingDetails.get("Ledger")
		subInventoryCode =packingDetails.get("SubInventoryCode")
		locatorName = packingDetails.get("LocatorName")	
		lotNumber = packingDetails.get("LotNo")	
		revision = packingDetails.get("Revision")
		lineName = packingDetails.get("ERPLineName")
		 
		containerNo =  packingDetails.get("CurrentContainerNumber")
		masterContainerNo =  packingDetails.get("CurrentMasterContainerNumber")	
	
	url = URLPath + apiPath		
	
	mydate = system.date.now()
	currentDate=system.date.format(mydate, "yyyy-MM-dd'T'HH:mm:ss.ss'Z'")		
	
	writeData = [
	  {
	    "ContainerNo": containerNo,
	    "ContainerType": containerType,
	    "PartNumber": woPartNumber,
	    "MasterContainerNo": masterContainerNo,
	    "IO": IO,
	    "SubInventoryCode": subInventoryCode,
	    "LocatorName": locatorName,
	    "Datetime": "2022-08-23T05:24:58.421Z",
	    "EmployeeNumber": "",
	    "Ledger": ledger,
	    "OU": OU,
	    "WorkOrderNumber": WoNumber,
	    "WorkOrderType": workOrderType,
	    "Revision": revision,
	    "QtyInContainer": qtyInContainer,
	    "MasterContainerType": "",
	    "LotNumber": lotNumber,
	    "MfgLine": lineName,
	    "SourceCode": "MES"
	  }
	]	
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
		print("postReturn 2:"+str(postReturn))	
	except:		
		result = 0
		print("Error updating ")
		pass
	return result
	
#----------------------------------PDA Related Functions --------------------------------------------------
def getAutoLinesByUserID(userID):
	apiPath = "OperatorConsole/GetOperatorConsoleLinesPDA?UserId="+str(userID)  
	url = URLPath + apiPath
	
	try:
		system.perspective.print("API URL is: "+str(url))
#		system.perspective.print("API InputData is: "+str(jsonParams))
		system.perspective.print("API Method is: Get ")
	except:
		pass
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)
	
	resultData= system.util.jsonDecode(data)
	print "resultData",resultData
	dataList = []
	
	for i in resultData:			
		lineId = i.get("LineId")
		lineName = i.get("LineName")	
		myList = [lineId,lineName] 		
		dataList.append(myList)	
			
	headers = ["LineId","LineName"]
	resultDetails = system.dataset.toDataSet(headers,dataList)	
	return resultDetails
	
def getCNSLinesByUserID(userID):
	apiPath = "OperatorConsole/GetOperatorConsoleLinesPDA?UserId="+str(userID)  
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)
	
	resultData= system.util.jsonDecode(data)
	print "resultData",resultData
	dataList = []
	

	for i in resultData:				
#		AreaId = i.get("AreaId")
#		if int(AreaId) != int(1) and int(AreaId) != int(5):
		DiscreteLine = i.get("DiscreteLine")
		if int(DiscreteLine) == int(1):
			lineId = i.get("LineId")
			lineName = i.get("LineName")
			myList = [lineId,lineName]
			dataList.append(myList)	
			
	headers = ["LineId","LineName"]
	resultDetails = system.dataset.toDataSet(headers,dataList)	
	return resultDetails
	
def getWoNumbersByLine(userId,selectedLine):
	apiPath = "OperatorConsole/GetOperatorConsoleWorkordersPDA?UserId="+str(userId)+"&LineId="+str(selectedLine)  
	url = URLPath + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Get ")
	except:
		pass
		
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)	
	resultData= system.util.jsonDecode(data)
	print"ResultData",(resultData)
	dataList=[]
	for i in resultData:
		workOrderId = i.get("ID")
		woNumber = i.get("WorkOrderNo")
		myList = [workOrderId,woNumber] 		
		dataList.append(myList)
	headers = ["WorkOrderId","WoNumber"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails
	
def getMachineListForSelectedWO(userId,selectedLineId,selectedWOId):
	apiPath = "OperatorConsole/GetOperatorConsoleWorkordersPDAWorkorderdetails?UserId="+str(userId)+"&LineId="+str(selectedLineId)+"&WorkOrderId="+str(selectedWOId)  
																									
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)	
	resultData= system.util.jsonDecode(data)
	myList=[]
	for i in resultData:
		machineName = i.get("MachineName")
#		machineId = i.get("MachineId")	
#		dataList = [machineName]	
		myList.append(machineName)					
#		myList.append(machineName)
	return myList
	
def getMachineListForManualWOOperation(userId,selectedLineId,selectedWOId):
	apiPath = "OperatorConsole/GetOperatorConsoleWorkordersPDAWorkorderdetails?UserId="+str(userId)+"&LineId="+str(selectedLineId)+"&WorkOrderId="+str(selectedWOId)  
																									
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)	
	resultData= system.util.jsonDecode(data)
	myList=[]
	for i in resultData:
		machineName = i.get("MachineName")	
		machineId = i.get("MachineId")	
		dataList = [machineId,machineName]	
		myList.append(dataList)	
	headers = ["MachineId","MachineName"]
	resultDetails = system.dataset.toDataSet(headers,myList)
	return resultDetails	


#------------------------------
def getMachineIdFromMachineName(userId,selectedLineId,WoNumber,machineName):
    apiPath = "OperatorConsole/GetPDAWorkorderAutoOperationDetailsOperatorConsole"
    url = URLPath + apiPath
    params = {    
      "workOrderNo": WoNumber,    
      "lineId": selectedLineId,    
      "userId": userId    
    }
    jsonParams = system.util.jsonEncode(params)        
    result = 1
    try:
        postReturn = system.net.httpPost(url,'application/json',jsonParams)    
    except:        
        result = 0        
        pass
    else:
        resultData= system.util.jsonDecode(postReturn)    
        for i in resultData:            
            machineNameFromList = i.get("MachineName")
            if str(machineName).upper() == str(machineNameFromList).upper():
                machineId = i.get("MachineId")
        return machineId
#------------------------------
def getAllPDADetailsForSelMachine(userId,selectedLineId,WoNumberId,machineName):
	apiPath = "OperatorConsole/GetPDAWorkorderSingleOperationDetailsOperatorConsole"
	url = URLPath + apiPath
	params = {	
	  "workOrderId": WoNumberId,
	  "lineId": selectedLineId,	
	  "userId": int(userId),	
	  "machineName": machineName	
	}
	
	jsonParams = system.util.jsonEncode(params)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except:		
		result = 0
		postReturn = ''
		pass
	
	resultData= system.util.jsonDecode(postReturn)
	return resultData
	

def getAutoOprMachineListForSelectedWO(userId,selectedLineId,WoNumber):
	apiPath = "OperatorConsole/GetPDAWorkorderAutoOperationDetailsOperatorConsole" 
	url = URLPath + apiPath
	params = {	
	  "workOrderNo": WoNumber,	
	  "lineId": selectedLineId,	
	  "userId": userId	
	}
	jsonParams = system.util.jsonEncode(params)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except:		
		result = 0
		postReturn = ''
		pass
	
	resultData= system.util.jsonDecode(postReturn)
	dataList = []
	for i in resultData:
		WorkflowOperationsId = i.get("WorkflowOperationsId")		 		
		dataList.append(WorkflowOperationsId)
	return dataList
	
def getMachineNameFromOprId(userId,selectedLineId,WoNumber,operationId):
	apiPath = "OperatorConsole/GetPDAWorkorderAutoOperationDetailsOperatorConsole" 
	url = URLPath + apiPath
	params = {	
	  "workOrderNo": WoNumber,	
	  "lineId": selectedLineId,	
	  "userId": userId	
	}
	jsonParams = system.util.jsonEncode(params)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except:		
		result = 0		
		pass
	else:
		resultData= system.util.jsonDecode(postReturn)
		machineList = []
		for i in resultData:
			if (i.get("WorkflowOperationsId")== operationId):
				MachineName= (i.get("MachineName"))
				machineList.append(MachineName)
			else:
				pass
		return set(machineList)
#--------------------------------------------------------------------------------------
def getMachineNameListFromWO(userId,selectedLineId,WoNumber):
	apiPath = "OperatorConsole/GetPDAWorkorderAutoOperationDetailsOperatorConsole"
	url = URLPath + apiPath
	params = {    
	  "workOrderNo": WoNumber,    
	  "lineId": selectedLineId,    
	  "userId": userId    
	}
	jsonParams = system.util.jsonEncode(params)        
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)    
	except:        
		result = 0        
		pass
	else:
		resultData= system.util.jsonDecode(postReturn)
		machineNameList = []
		for i in resultData:            
			machineName = i.get("MachineName")
			machineNameList.append(machineName)
		machineNameList = list(set(machineNameList))
		return machineNameList
#--------------------------------------------------------------------------------------
	
def getMoldAssignmentDetails(WoNumber,machineID):	
	apiPath = "OperatorConsole/OperatorconsoleMoldAssignmentCheck?WorkOrderNo="+str(WoNumber)+"&MachineId="+str(machineID)	
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)		
	resultData= system.util.jsonDecode(data)
	dataList = []		
	for i in resultData:		
		isCountMold = i.get("isCountMold")	
		if isCountMold==1:
			WoNumber = i.get("WorkOrderNo")
			MachineId = i.get("MachineId")
			cavity = i.get("Cavity")
			productPiece = i.get("ProductPiece")		
			isMoldLinked = i.get("isMoldLinked")			
			isCountMold = i.get("isCountMold")		
			
			myList = [WoNumber,MachineId,cavity,productPiece,isMoldLinked] 		
			dataList.append(myList)	
		else:
			pass				

	return dataList
#--------------------------------------- Get Good Count For CNS Machines -------------------------------
# Author: Sushant Chavan
# Updated On: 19-02-2023
def getGoodCountForCNS(WoNumber,machineIdList,shotCount):
	WoNumber = "CL13859568"
	machineIdList = [28,29]
	shotCount = 100	
	
	FinalSum = 0
	for machineId in machineIdList:	
		try:
			moldDetails = WorkOrderDetailsAPI.getMoldAssignmentDetails(WoNumber,machineId)
		except:
			return 0
		else:		
			for i in moldDetails:
				cavity = i[2]
				pieces = i[3]
				try:		
					finalGoodQty = (float(shotCount) * float(cavity))/float(pieces)
				except:
					finalGoodQty = 0
					pass
				FinalSum = FinalSum + finalGoodQty	
				
			return int(FinalSum)
#-------------------------------------------------------------------------------------------------------------
#--------------------------------------- Get Mold Details for CNS Carousal -------------------------------
# Author: Sushant Chavan
# Updated On: 19-02-2023
def getLoadedMoldDetails(WoNumber,machineId,machineName):	
	apiPath = "OperatorConsole/OperatorconsoleMoldAssignmentCheck?WorkOrderNo="+str(WoNumber)+"&MachineId="+str(machineId)	
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)		
	resultData= system.util.jsonDecode(data)
	dataList = []		
	for i in resultData:		
		isCountMold = i.get("isCountMold")	
		isLoaded = i.get("isLoaded")	
		
		if isLoaded==1:
			WoNumber = i.get("WorkOrderNo")
			MachineId = i.get("MachineId")
			cavity = i.get("Cavity")
			productPiece = i.get("ProductPiece")		
			isMoldLinked = i.get("isMoldLinked")			
			isCountMold = i.get("isCountMold")	
			MaxLife = i.get("MaxLife")	
			MoldCode = i.get("MoldCode")
#			MoldCode = i.get("MoldCode")	
				
						
			myList =  [MoldCode,cavity,productPiece,MaxLife,MachineId,machineName]		
			dataList.append(myList)	
		else:
			pass				

	return dataList

#Created By : Hari 
#Purpose : To show Machine Shots 
def getLoadedMoldDetails1(WoNumber,machineId,machineName):	
	apiPath = "OperatorConsole/OperatorconsoleMoldAssignmentCheck?WorkOrderNo="+str(WoNumber)+"&MachineId="+str(machineId)	
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)		
	resultData= system.util.jsonDecode(data)
	dataList = []		
	for i in resultData:		
		isCountMold = i.get("isCountMold")	
		isLoaded = i.get("isLoaded")	
		
		if isLoaded==1:
			WoNumber = i.get("WorkOrderNo")
			MachineId = i.get("MachineId")
			cavity = i.get("Cavity")
			productPiece = i.get("ProductPiece")		
			isMoldLinked = i.get("isMoldLinked")			
			isCountMold = i.get("isCountMold")	
			MaxLife = i.get("MaxLife")	
			MoldCode = i.get("MoldCode")
			MachineShots = i.get("Shots")	
				
						
			myList =  [MoldCode,cavity,productPiece,MaxLife,MachineId,machineName,MachineShots]		
			dataList.append(myList)	
		else:
			pass				

	return dataList


def getPDAExpiredComponents(WoNumber,workflowId,operation,process):
	apiPath = "OperatorConsole/GetAttachedWorkFlowProcessComponentsWithSubstituteForOperatorConsole"
	url = URLPath + apiPath
	params = {
	  "workOrderNo":WoNumber,
	  "workflowId": workflowId,
	  "workflowOperationId": operation,
	  "workflowProcessId": process,
	  "headerName": "ADD PARTS TO BE consumed"
		}
	
	jsonParams = system.util.jsonEncode(params)			 
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)			
	except:		
		result = 0
		postReturn = ''
		pass
	try:
		resultData= system.util.jsonDecode(postReturn)		
	except:
		resultData = []				
	k=1
	dataList = []
	for i in resultData:
		IsExpired = 1
	#Get Component Expiry Date by API 
	#	ComponentExpiryDate = i.get("ComponentExpiryDate")
	#	today = system.date.now()
	#	TodayDate= system.date.format(today, "dd/MM/yyyy,HH:mm:ss")
	#	if ComponentExpiryDate >= TodayDate or ComponentExpiryDate == None:
	#		IsExpired = 0
	#	else:
	#		IsExpired = 1
		if IsExpired == int(1):
			SrNo = k
			partNumber = i.get("PartNo")
			revision = i.get("Revision")
			componentName = str(partNumber)+"_"+str(revision)
			uom = i.get("UOMName")
			ComponentExpiryDate = system.date.now()
									
			myList = [SrNo,componentName,uom,ComponentExpiryDate] 		
			print myList
			dataList.append(myList)	
			k = k+1
			
	headers = ["SrNo","ComponentName","uom","ComponentExpiryDate"]
	resultDetails = system.dataset.toDataSet(headers,dataList)	
	print "resultDetails", resultDetails
	return resultDetails

#----------------------Material Request ALL API's  from Operator Console------------------------
def getExpiredComponentsDetails(workOrderId,FGCount):
	try:
		scriptName = "Get Expired Components Details"
		apiPath = "OperatorConsole/MaterialRequestFromOperatorConsole?WorkOrderId="+str(workOrderId)+"&FGQty="+str(FGCount)
		url = URLPath + apiPath
		
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		dataList = []
		j=1
		for i in resultData:
			#Get Component Expiry Date by API 
			ComponentExpiryDate = i.get("ComponentExpiryDate")
			today = system.date.now()
			TodayDate= system.date.format(today, "dd/MM/yyyy,HH:mm:ss")
			if ComponentExpiryDate >= TodayDate or ComponentExpiryDate == None:
				IsExpired = 0
			else:
				IsExpired = 1

			if IsExpired == int(1) or IsExpired == 1:
				srNo = j
				WorkorderNo = i.get("WorkOrderNumber")
				partNumber = i.get("PartNumber")
				description = i.get("Description")	
				uom = i.get("UOM")		
				woPartNumber = i.get("WoPartNumber")
				ComponentExpiryDate = i.get("ComponentExpiryDate")
				
				myList = [srNo,WorkorderNo,partNumber,description,uom,woPartNumber,ComponentExpiryDate]
				dataList.append(myList)	
				j = j+1
				
		headers = ["SrNo","WorkorderNo","PartNumber","Description","UOM","WoPartNumber","ComponentExpiryDate"]		
		resultDetails = system.dataset.toDataSet(headers,dataList) 
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)	

def getOprConsoleMaterialRequestDetails(workOrderId,FGCount):
	try:
		scriptName = "getOprConsoleMaterialRequestDetails"
		apiPath = "OperatorConsole/MaterialRequestFromOperatorConsole?WorkOrderId="+str(workOrderId)+"&FGQty="+str(FGCount)
		url = URLPath + apiPath
		
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
	
		dataList = []
		j=1
		
		for i in resultData:	
			iD = j
			mfgOrderName = i.get("WorkOrderNumber")
			partNumber = i.get("PartNumber")
			partNumberId = i.get("PartNumberId")	
			uom = i.get("UOM")		
			bomQTY = i.get("BOMQTY")
			totalRequiredQty = i.get("TotalRequiredQty")
			description = i.get("Description")
			spq = i.get("SPQ")
			SPQRequired = i.get("SPQRequired")
			totalPendingReqCount = i.get("TotalPendingReqCount")
			totalPendingReqestedQty = i.get("TotalPendingReqestedQty")
			woPartNumber = i.get("WoPartNumber")
			requestComponentCode = i.get("RequestComponentCode")
			componentRevison = i.get("ComponentRevison")
			mfgLINE = i.get("MFGLINE")
			locatorName = i.get("LocatorName")
			subInventoryCode = i.get("SubInventoryCode")
			transferOrganization = i.get("TransferOrganization")
			employeeNumber = i.get("EmployeeNumber")
			reason = i.get("Reason")
			requestStatus = i.get("RequestStatus")
			requestCloseddate = i.get("RequestCloseddate")	
			requestStatus = i.get("RequestStatus")
			requestCloseddate = i.get("RequestCloseddate")
			ledger = i.get("Ledger")
			ou = i.get("OU")
			workOrderType = i.get("WorkOrderType")
			requestQty = 0
			selectionId = 1
			SPQCount = i.get("SPQCount")
			Flag = i.get("isSPQNull")

			
			ComponentExpiryDate = i.get("ComponentExpiryDate")
			today = system.date.now()
			TodayDate= system.date.format(today, "dd/MM/yyyy,HH:mm:ss")
			print "Expire Date " +str(partNumber)+ "-> ", ComponentExpiryDate
			print "Today  Date -> ", TodayDate
			
			if ComponentExpiryDate >= TodayDate or ComponentExpiryDate == None:
				IsExpired = 0
				print "Not Expired--->"
			else:
				IsExpired = 1
				print "Expired-------> "
			
			if Flag == int(1):
				selectionId = 0
			else:
				selectionId = 1
			
			myList = [iD,mfgOrderName,partNumber,description,uom,bomQTY,totalPendingReqCount,totalPendingReqestedQty,totalRequiredQty,requestQty,spq,SPQRequired,selectionId,partNumberId,SPQCount,woPartNumber,requestComponentCode,componentRevison,mfgLINE,workOrderType,locatorName,subInventoryCode,employeeNumber,reason,ledger,ou,Flag,IsExpired]
			dataList.append(myList)	
			j = j+1
		
		headers = ["ID","WorkOrderName","Material","Description","UOM","BOMQty","TotalPendingCount","TotalPendingQty","TotalRequiredQty","RequestQty","SPQNumber","SPQRequired","Action","partID","SPQCount","woPartNumber","requestComponentCode","componentRevison","mfgLINE","workOrderType","locatorName","subInventoryCode","employeeNumber","reason","ledger","ou","Flag","IsExpired"]		
		resultDetails = system.dataset.toDataSet(headers,dataList) 
		return resultDetails
		
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		
#------------------------Request MAterial For MES Export --------------------------------Get All Details ---->
def getOprConsoleMaterialRequestDetailsForMESExport(workOrderId,FGCount):
	try:
		scriptName ="getOprConsoleMaterialRequestDetailsForMESExport"
		apiPath =  "OperatorConsole/MaterialRequestFromOperatorConsole?WorkOrderId="+str(workOrderId)+"&FGQty="+str(FGCount)
		url = URLPath + apiPath
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)	
		resultData = system.util.jsonDecode(data)
		return resultData
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)

#------------------Save Request Qty
def saveRequestMaterial(resultData,workOrderId,userID,requestedDate,ShiftId):
	try:
		scriptName ="saveRequestMaterial"
		resultDetails = system.util.jsonDecode(resultData)
		arrayJson = []
		
		for part in resultDetails:
			PartID = int(part[13])
			SPQCount =int(part[11])
			IsSelected = int(part[12])
			IsExpired = part[27]
			
			if IsExpired ==int(1):
				IsExpired = True
			else:
				IsExpired = False
			
			if IsSelected != int(1) or IsSelected != True:
				IsSelected = False
			else:
				IsSelected = True
				
			jsonformat =  {
				"workOrderId": int(workOrderId),
				"partId": PartID,
				"spqCount": SPQCount,
				"isSubmit": False,
				"isSelected": IsSelected,
				"requestDate": str(requestedDate),
				"createdBy": int(userID),
			    "isExpired": IsExpired,
			    "shiftId": ShiftId
				}
				
			arrayJson.append(jsonformat)
			
		params = {
				"operatorConsoleRequestMateriallist": arrayJson
				 }
			
		apiPath = "OperatorConsole/AddMaterialFromOperatorConsole"
		
		url = URLPath + apiPath	
		jsonParams = system.util.jsonEncode(params)
		result = 1
		try:
			postReturn1 = system.net.httpPost(url,'application/json',jsonParams)
			system.perspective.print("postReturn1 : " + str(postReturn1))
		except:		
			result = 0		
			pass
		return result
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)

#-------------Submit Requested Qty ----------------------------
def submitRequestMaterial(resultData,workOrderId,userID,requestedDate,ShiftId):
	try:
		scriptName = "submitRequestMaterial"
		resultDetails = system.util.jsonDecode(resultData)
		arrayJson = []
		
		for part in resultDetails:	
			PartID = int(part[13])
			SPQCount =int(part[11])
			IsSelected = int(part[12])
			IsExpired = part[27]
			
			if IsExpired ==int(1):
				IsExpired = True
			else:
				IsExpired = False
			
			if IsSelected != int(1) or IsSelected != True:
				IsSelected = False
			else:
				IsSelected = True
				
				jsonformat =  {
					"workOrderId": int(workOrderId),
					"partId": PartID,
					"spqCount": SPQCount,
					"isSubmit": True,
					"isSelected": IsSelected,
					"requestDate": str(requestedDate),
					"createdBy": int(userID),
				    "isExpired": IsExpired,
				    "shiftId": ShiftId
					}
					
				arrayJson.append(jsonformat)
		
		params = {
			"operatorConsoleRequestMateriallist": arrayJson
			 }
		
		apiPath = "OperatorConsole/AddMaterialFromOperatorConsole"
		
		url = URLPath + apiPath
		
		jsonParams = system.util.jsonEncode(params)	
		result = 1
		try:
			postReturn1 = system.net.httpPost(url,'application/json',jsonParams)
		except:		
			result = 0		
			pass
		return result
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)

#---------------POST TO ERP DB-------------------------------
def postOprConsoleMaterialRequestDetailsToERP(resultData):
	try:
		scriptName = "postOprConsoleMaterialRequestDetailsToERP"
		componentDataList = []
		for i in resultData:				
			requestQty = 0				           # Request Qty is missing from Mohits API . Need to update API--> Mohit	
			selectionId = i.get("IsSelected")
			print"SelectionID", selectionId
			if selectionId == True:
			
				WorkorderDetails =  {
						"io": "string",
						"workOrderNumber": str(i.get("WorkOrderNumber")),
						"partNumber": str(i.get("WoPartNumber")),
						"revision": str(i.get("ComponentRevison")),
						"datetime": " ",
						"woqty": str(i.get("TotalRequiredQty")),
						"requestComponentCode": str(i.get("RequestComponentCode")),
						"componentRevison": str(i.get("ComponentRevison")),
						"qty": str(i.get("SPQCount")),
						"uom": str(i.get("UOM")),
						"mfgLine": str(i.get("MFGLINE")),
						"locatorName": str(i.get("LocatorName")),
						"transferOrganization": str(i.get("TransferOrganization")),
						"subInventoryCode": str(i.get("SubInventoryCode")),
						"requestedDateTime": " ",
						"employeeNumber":str(i.get("EmployeeNumber")),
						"reason":str(i.get("Reason")),
						"requestStatus":str(i.get("RequestStatus")),
						"requestCloseddate": " ",
						"ledger": str(i.get("Ledger")),
						"ou": str(i.get("OU")),
						"workOrderType":str(i.get("WorkOrderType")),
						"sourceCode": "MES"
					  }
					  
				componentDataList.append(WorkorderDetails)				
				
			print "componentDataList"	,componentDataList				
			apiPath = "MaterialRequest/AddMaterialRequest"
			url = URLPath + apiPath		
			jsonParams = system.util.jsonEncode(componentDataList)
			result = 1
			try:
				postReturn = system.net.httpPost(url,'application/json',jsonParams)	
			except Exception as e:		
				result = 0
				scriptName = "Operator Console:Post Operator Console Material Request Details.."
				errorMessage=scriptName  +' Exception - '+  str(e)
				Authentication.exceptionLogger(errorMessage)
			print "result",result
			return result
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
#----------------Get Submitted Requested material  WorkOrders

#----------------Get Submitted Requested material  WorkOrders
def GetPrevioussubmittedRequest(LineId):
	try:
		scriptName = "API: Get Previous Requested Material Workorder List"
		apiPath = "OperatorConsole/GetWorkordersForViewRequestsForOperatorConsole?LineId="+str(LineId)
		url = URLPath + apiPath
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		print "resultData",resultData
		dataList = []
		j = 1
		for i in resultData:	
			SrNo = j
			WorkorderNo = i.get("WorkorderNo")
			WorkOrderId = i.get("WorkOrderId")
#			RequestedDate = ""
			ViewDetails = ""
			j= j+1
			myList = [SrNo,WorkorderNo,WorkOrderId,ViewDetails]
			dataList.append(myList)
		
		headers = ["SrNo","WorkorderNo","WorkOrderId","ViewDetails"]
		resultDetails = system.dataset.toDataSet(headers,dataList)	
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)

#-------------------Get Submitted Requested Qty by WorkOrder Number---------------------
def GetsubmitedRequest(WoNumber):
	try:
		scriptName = "API: Get Previous Requested Material Workorder List"
		apiPath = "OperatorConsole/GetWorkordersMaterialRequestsForOperatorConsole?WorkOrderNo="+str(WoNumber)
		url = URLPath + apiPath
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		print "resultData",resultData
		dataList = []
		j = 1
		for i in resultData:	
			SrNo = j
			WorkorderNo = i.get("WorkorderNo")
			ComponentName = i.get("PartNo")
			Description = i.get("Description")
			UOMName = i.get("UOMName")
			BOMQTY = i.get("BOMQTY")
			SPQ = i.get("SPQ")
			SPQCount = i.get("SPQCount")
			PartId = i.get("PartId")
			j= j+1
			myList = [SrNo,WorkorderNo,ComponentName,Description,UOMName,BOMQTY,SPQ,SPQCount,PartId] 
			dataList.append(myList)
		
		headers = ["SrNo","WorkorderNo","ComponentName","Description","UOMName","BOMQTY","SPQ","SPQCount","PartId"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)

def getshiftId():
	scriptName="API:Get ShiftId "
	apiPath = "Shifts/GetShift/0"
	url = URLPath + apiPath		
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData=data.json
	print "resultData",resultData
	
	dataList = []
	for i in resultData:	
		shiftStartTime1 =  i.get("startDate")
		shiftEndTime1 = i.get("endDate")
		shiftStartTime = shiftStartTime1.replace("T"," ")
		shiftEndTime = shiftEndTime1.replace("T"," ")
		shiftId = i.get('Id')
		
		currentDateTime = system.date.now()
		TodayDate = system.date.format(currentDateTime,"yyyy-MM-dd HH:mm:ss")
		if ((TodayDate < shiftEndTime) and (TodayDate > shiftStartTime)):
			print"ShiftID is " ,shiftId
			return shiftId
			break
#-------------------------------Save Change Over------------------------------
def postComponentDetails(WorkflowOperationsId,WoNumber,WorkflowId,operatorConsoleComponentId,selectedItemId,serialNo,lotNo,consumeQty,userId,IsExpired):
	apiPath = "OperatorConsole/CreateOperatorConsoleComponent"
	url = URLPath + apiPath		
	
	if IsExpired == int(1) or IsExpired == 1:
		IsExpired = True
	else:
		IsExpired = False	
	
	writeData = {	
	  "operatorConsoleComponents": [
	    {
	      "operatorConsoleComponentId": 0,
	      "selectedItemId": int(selectedItemId),
	      "serialNo": str(serialNo),
	      "lotNo": str(lotNo),
	      "consumedQty": int(consumeQty),
	      "operationId": WorkflowOperationsId,
	      "workflowId": WorkflowId,
	      "createdBy": userId,
	      "workOrderNo": WoNumber,
	      "IsActive": True,
	      "IsExpired": IsExpired
	    }
	  ]
	}
	
	
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except Exeption as e:		
		result = 0
		scriptName = "Operator Console:Post Component Details.."
		errorMessage=scriptName  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)
	return postReturn
	

def getWorkInstructionAttachmentDetails_WorkOrderIdWise(WorkflowId,Header,WorkOrderNo,WorkOrderId,UserId):
	try:
		scriptName='getWorkInstructionAttachmentDetails_WorkOrderIdWise'
		apiPath ="OperatorConsole/GetAttachedWorkFlowProcessActionLinksForOperatorConsole_WorkOrderIdWise/"+str(WorkflowId)+"/"+str(Header)+"/"+str(WorkOrderNo)+"/"+str(WorkOrderId)+"/"+str(UserId)
		url = URLPath + apiPath
		system.perspective.print(url)
#		url="http://hnjmesjedev/FactoryMagixWebAPI/api/OperatorConsole/GetAttachedWorkFlowProcessActionLinksForOperatorConsole_WorkOrderIdWise/147/Add20Work20Instruction/PD53374436/83070/63"
		resultData=None
		client = system.net.httpClient() 
		data = client.get(url)
		if data.good:
			resultData=data.json
		dataList = []
		
		
		if str(Header)=='1' or str(Header)==1:
			k = 1
			dataList = []
			for i in resultData:
				ID = i.get("Links")	
				print 'ID-->'+str(ID)
				parameter = i.get("Parameter")
				isSelected = i.get("IsSelected")
				Operation = i.get("Operation")
				operationID = i.get("operationID")
				Notes = i.get("Notes")
#				operationID = i.get("operationID")
				if isSelected==1 or str(isSelected)=='1':
					YesNo = True
				else:
					YesNo = False
				convertedDict = json.loads(ID)
				print "Convertd Dict--->"+str(convertedDict)	
				for j in convertedDict:
					Id = j.get("id")	
					SrNo = k	
					dataValues = j.get("name")
					checklistType = j.get("type")
											
					myList = [SrNo,Id,dataValues,parameter,checklistType,YesNo,Operation,operationID,Notes] 		
					dataList.append(myList)		
					k = k+1
			headers = ["SrNo","Id","Name","Parameter","checklistType","Yes_No","Operation","operationID","Notes"]
			resultDetails = system.dataset.toDataSet(headers,dataList)	
		else:
		
			headers = ["SrNo","dataValues","fileName","filePath","Link","MachineName","Operation"]
			SrNo=1
			for i in resultData:		
			
				ID = i.get("Links")				
				convertedDict = json.loads(ID)	
				print convertedDict
				for j in convertedDict:
					dataValues = j.get("name")
				MachineName = i.get("MachineName")
				fileName = i.get("FileName")	
				filePath = i.get("Path")	
				Link='View'	
				Operation= i.get("Operation")
				dataValues = j.get("name")	
				myList = [SrNo,dataValues,fileName,filePath,Link,MachineName,Operation] 
				dataList.append(myList)		
				SrNo=SrNo+1
			resultDetails = system.dataset.toDataSet(headers,dataList)	
		
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		print errorMessage
		Authentication.exceptionLogger(errorMessage)		
		print(errorMessage)
		return None