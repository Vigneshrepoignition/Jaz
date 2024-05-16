import re
import json
import urllib2, urllib
from datetime import datetime

defaultPath=system.tag.read("[default]JMES_InternalTags/DafaultTagPath").value		
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
openingUrl = URLPath.replace('WebAPIQA/api/', 'QA/')
#openingUrl = 'http://172.19.16.91/FactoryMagixQA/'
#URLPath = system.tag.read("[default]JMES_InternalTags/urlSITAPI").value

#-----------Function Start -- Get Complete RM Details for Users --------->

def GetResultData(userId,TypeId):
#	apiPath = "MaintenanceOperatorConsoleRM/GetMaintenanceOperatorConsoleWorkOrdersdefault?UserId="+str(userId)	
	apiPath	= "MaintenanceOperatorConsoleRM/GetMaintenanceOperatorConsoleWorkOrdersdefault?UserId="+str(userId)+"&maintenanceType="+str(TypeId)
	url = URLPath + apiPath		
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if TypeId == int(1) or TypeId == 1 or TypeId == str('1'):
		if data.good:    
			resultData=data.json
		return resultData
	else:
		if data.good:
			resultData=data.json
		return resultData

def getCompleteRMDetailsForUser(UserID,TypeId):
	try: 
		scriptName="API:getCompleteRMDetailsForUser"
#		apiPath = "MaintenanceOperatorConsoleRM/GetMaintenanceOperatorConsoleWorkOrdersdefault?UserId="+str(UserID)	
		apiPath	= "MaintenanceOperatorConsoleRM/GetMaintenanceOperatorConsoleWorkOrdersdefault?UserId="+str(UserID)+"&maintenanceType="+str(TypeId)
		url = URLPath + apiPath		
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		system.perspective.print('resultData :' + str(resultData))
		if TypeId == int(1) or TypeId == 1 or TypeId == str('1'):
			dataList = []
			j=1
			for i in resultData:			
				ID = j
				WoNumber = i.get("WO Number")
				Line = i.get("Line")
				RmType = i.get("RM Type")
				Machine = i.get("Machine")
				MachineId = i.get("MachineId")
				Status = i.get("Status")		
				ReasonCode = i.get("Reason Code")
				ReasonCodeID = i.get("ReasonCodeID")
				ActualStartDate = i.get("Actual Start Time")
				if str(ActualStartDate) == str("null") or ActualStartDate == None: 
					ActualStartDate = ''							
				DueDateTime = i.get("Due Date Time")
				priority = i.get("PriorityName")
				ActualCmpDateTime = i.get("Actual Completion Date Time")
				RMOrderID = i.get("RMOrderId")
				Assign = ""
				viewDetails = ""
				Enterprise = i.get("Enterprise")
				Area = i.get("Area")
				Plant = i.get("Plant")
				WarehouseName = i.get("WarehouseName")
				WarehouseId = i.get("WarehouseId")
				CreatedBy = i.get("CreatedBy")
				myList = [ID,WoNumber,Line,RmType,Machine,MachineId,Status,ReasonCode,ReasonCodeID,ActualStartDate,DueDateTime,priority,ActualCmpDateTime,RMOrderID,Assign,viewDetails,Enterprise,Area,Plant,WarehouseName,WarehouseId,CreatedBy]		
				dataList.append(myList)
				j = j+1
				
			headers =  ["ID","WoNumber","Line","RM Type","Machine","MachineId","Status","ReasonCode","ReasonCodeID","ActualStartDate","DueDateTime","Priority","ActualCmpDateTime","RMOrderID","Assign","View_Details","Enterprise","Area","Plant","WarehouseName","WarehouseId","CreatedBy"]
			resultDetails = system.dataset.toDataSet(headers,dataList)
			return resultDetails 
		else:
			dataList = []
			j=1
			for i in resultData:			
				ID = j
				WoNumber = i.get("WO Number")
#				Line = i.get("Line")
#				RmType = i.get("RM Type")
				ToolName = i.get("Machine")
				ToolId = i.get("MachineId")
				Status = i.get("Status")		
				ReasonCode = i.get("Reason Code")
				ReasonCodeID = i.get("ReasonCodeID")
				ActualStartDate = i.get("Actual Start Time")
				if str(ActualStartDate) == str("null") or ActualStartDate == None: 
					ActualStartDate = ''							
				DueDateTime = i.get("Due Date Time")
				priority = i.get("PriorityName")
				ActualCmpDateTime = i.get("Actual Completion Date Time")
				RMOrderID = i.get("RMOrderId")
				Assign = ""
				viewDetails = ""
				WarehouseName = i.get("WarehouseName")
				WarehouseId = i.get("WarehouseId")
				CreatedBy = i.get("CreatedBy")
				myList = [ID,WoNumber,ToolName,ToolId,Status,ReasonCode,ReasonCodeID,ActualStartDate,DueDateTime,priority,ActualCmpDateTime,RMOrderID,Assign,viewDetails,WarehouseName,WarehouseId,CreatedBy]		
				dataList.append(myList)
				j = j+1
				
			headers =  ["ID","WoNumber","ToolName","ToolId","Status","ReasonCode","ReasonCodeID","ActualStartDate","DueDateTime","Priority","ActualCmpDateTime","RMOrderID","Assign","View_Details","WarehouseName","WarehouseId","CreatedBy"]
			resultDetails1 = system.dataset.toDataSet(headers,dataList)
			return resultDetails1
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		system.perspective.print('errorMessage :' + str(errorMessage))
		Authentication.exceptionLogger(errorMessage)
#-----------Function End -- Get Complete RM Details for Users --------->	

#-----------Function Start -- Get getRMListByFilterSearch RM Details for Users --------->	

def getRMListByFilterSearch(enterpriseID,plantID,areaID,lineID,machineID,UserId):    
    try:
		scriptName="API:getRMListByFilterSearch"
		apiPath = "MaintenanceOperatorConsoleRM/GetMaintenanceOperatorConsoleWorkOrdersonInput?EnterpriseId="+str(enterpriseID)+"&PlantId="+str(plantID)+"&AreaId="+str(areaID)+"&LineId="+str(lineID)+"&MachineId="+str(machineID)+"&UserId="+str(UserId)
		url = URLPath + apiPath
		#        request = urllib2.Request(url)
		#        response = urllib2.urlopen(request)
		#        data = system.net.httpGet(url)
		#        resultData= system.util.jsonDecode(data)
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		dataList = []
		j=1
		for i in resultData:            
		    ID = j
		    WoNumber = i.get("WO Number")
		    Line = i.get("Line")
		    RmType = i.get("RM Type")
		    Machine = i.get("Machine")
		    MachineId = i.get("Machineid")
		    Status = i.get("Status")        
		    ReasonCode = i.get("Reason Code")
		    ReasonCodeID = i.get("ReasonCodeID")
		    ActualStartDate = i.get("Actual Start Time")
		    if str(ActualStartDate).lower() == str("null").lower() or ActualStartDate == None:
		    	ActualStartDate = ''
		    DueDateTime = i.get("Due Date Time")
		    priority = i.get("PriorityName")
		    ActualCmpDateTime = i.get("Actual Completion Date Time")
		    RMOrderID = i.get("RMOrderId")
		    Assign = ""
		    viewDetails = ""
		    Enterprise = i.get("Enterprise")
		    Area = i.get("Area")
		    Plant = i.get("Plant")
		    WarehouseName = i.get("WarehouseName")
		    WarehouseId = i.get("WarehouseId")
		    CreatedBy = i.get("CreatedBy")
		    
		    myList = [ID,WoNumber,Line,RmType,Machine,MachineId,Status,ReasonCode,ReasonCodeID,ActualStartDate,DueDateTime,priority,ActualCmpDateTime,RMOrderID,Assign,viewDetails,Enterprise,Area,Plant,WarehouseName,WarehouseId,CreatedBy]
		    dataList.append(myList)
		    j = j+1
		headers = ["ID","WoNumber","Line","RM Type","Machine","MachineId","Status","ReasonCode","ReasonCodeID","ActualStartDate","DueDateTime","Priority","ActualCmpDateTime","RMOrderID","Assign","View_Details","Enterprise","Area","Plant","WarehouseName","WarehouseId","CreatedBy"]
		resultDetails = system.dataset.toDataSet(headers,dataList)    
		return resultDetails
    except:
        import sys, os
        errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
        Authentication.exceptionLogger(errorMessage)




#-----------Function Start -- Get Single Row RM Details for Users -------------	

def getSingleWORow(WoNumber):
 	try: 
		scriptName="API:getSingleWORow"
		apiPath = "MaintenanceOperatorConsoleRM/GetOperatorConsolesingle"
		url = URLPath + apiPath
		params = {
			"WorkOrderNo": WoNumber,
			"OrderId" :"",
			"WorkflowOperationsId": 0
			}
				  
		jsonParams = system.util.jsonEncode(params)
		print("jsonParams:",jsonParams)	
		result = 1
		try:
			postReturn1 = system.net.httpPost(url,'application/json',jsonParams)	
			print(postReturn1)
		except:		
			result = 0		
			pass
			
		resultData = system.util.jsonDecode(postReturn1)
		print(resultData)
		dataList = []
		j=1
		for i in resultData:
		
			ID = j
			WoNumber = i.get("WO Number")
			Machine = i.get("Machine")
			Status = i.get("Status")
			Line = i.get("Line")
			RMType = i.get("RM Type")
			RMOrderID = i.get("RMOrderID")
			ActualStartDate = i.get("Actual Start Time")
			PriorityName = i.get("PriorityName")#DueDate
			ActualCompletionDate = i.get("Actual Completion Date Time")
	
			myList = [ID,WoNumber,Line,RMType,Machine,Status,ActualStartDate,PriorityName,ActualCompletionDate,RMOrderID]		
			dataList.append(myList)	
			j = j+1
			print(myList)
		headers = ["ID","WoNumber","Line","RM Type","Machine","Status","ActualStartDate","PriorityName","ActualCmpDateTime","RMOrderID"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
#-----------Function End -- Get single Row RM Details for Users ------------------------------

#-----------Function Start-- Start Operation of RM Order ------------------------------
def startOperation(RMOrderID,WoNumber,userID):	
	try: 
		scriptName="API:startOperation"
		apiPath = "MaintenanceOperatorConsoleRM/OperationStatusConformation"
		url = URLPath + apiPath		
		writeData = {
		  "CreatedBy": int(userID),
		  "rmOrderID" : int(RMOrderID),
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
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
#-----------Function End-- Start Operation of RM Order ------------------------------

#-----------Function Start-- Hold Operation of RM Order ------------------------------

def holdOperation(WoNumber,RMOrderID,holdReasonId,holdComment,userID):
	try: 
		scriptName="API:holdOperation"
		apiPath = "MaintenanceOperatorConsoleRM/OperationStatusConformation"	
		url = URLPath + apiPath
		writeData = {
		  "isActive": True,
		  "createdBy": int(userID),
		  "workOrderNo": str(WoNumber),
		  "reasonCodeId": int(holdReasonId),
		  "reasonCodeComments": holdComment,	
		  "RMOrderID" : int(RMOrderID),
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
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)	

#-----------Function END-- Hold Operation of RM Order ------------------------------

#-----------Function Start-- Resume Operation of RM Order ------------------------------
	
def resumeHoldOperation(RMOrderID,WoNumber,resumeComment,userID):
	try: 
		scriptName="API:resumeHoldOperation"
		apiPath = "MaintenanceOperatorConsoleRM/OperationStatusConformation"	
		url = URLPath + apiPath
		system.perspective.print('Resume Comment is ' + str(resumeComment))
		writeData = {
		  "isActive": True,
		  "createdBy": int(userID),
		  "workOrderNo": str(WoNumber),	
		  "reasonCodeComments": resumeComment,	
		  "RMOrderID" : int(RMOrderID),	
		  "statusId": 1
		}
		
		jsonParams = system.util.jsonEncode(writeData)		
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
			print("PostReturn",postReturn)
			dataPosted= system.util.jsonDecode(postReturn)
		except:		
			result = 0
			pass
		startOpsId = dataPosted.get("startOpsId")
		return startOpsId
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
#-----------Function End-- Resume Operation of RM Order ------------------------------

#-----------Function Start--Complete Operation of RM Order ------------------------------

def completeOperation(WoNumber,RMOrderID,commentText,holdReasonId,CompleteCategoryID,userID):
	try: 
		scriptName="API:completeOperation"
		apiPath = "MaintenanceOperatorConsoleRM/OperationStatusConformation" 
		url = URLPath + apiPath
		writeData = {
		  "isActive": True,
		  "createdBy": int(userID),
		  "modifiedBy": int(userID),
		  "workOrderNo": str(WoNumber),	
		  "reasonCodeComments": commentText,
		  "reasonCodeId": int(holdReasonId),
		  "reasonCategoryId": str(CompleteCategoryID),	
		  "RMOrderID" : int(RMOrderID),	
		  "statusId": 3
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
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		
#-----------Function End--Complete Operation of RM Order ------------------------------

#-----------Function Start--Assign RM Order ------------------------------
def AssignRmOrder(RMOrderID,WoNumber,userID,ReasonCodeID):
	try: 
		scriptName="API:startOperation"
		apiPath = "MaintenanceOperatorConsoleRM/OperationStatusConformation"
		url = URLPath + apiPath		
		writeData = {
		  "CreatedBy": int(userID),
		  "RMOrderID" : int(RMOrderID),
		  "statusId": 7,
		  "reasonCodeId": int(ReasonCodeID)
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
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)

#-----------Function End--Assign RM Order ------------------------------

#ADD RM NOTES

def AddRMNotes(comment,RMOrderID,shiftId,userId):
	scriptName="API:PostRMNotes"
	apiPath = "MaintenanceOperatorConsoleRM/AddRMNotes"
	url = URLPath + apiPath	
	writeData = {
		  "isActive": True,
		  "createdBy": userId,
		  "rmNotes": comment,
		  "rmOrderId": int(RMOrderID),
		  "shiftId": int(shiftId)
		}
	jsonParams = system.util.jsonEncode(writeData)		

	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		print("PostReturn",postReturn)
	except:		
		result = 0
		pass
	print "result",result
	return result
	
def getRMNotes(RMOrderID):
	scriptName="API:Get PM Notes by RMOrderID"
	apiPath ="MaintenanceOperatorConsoleRM/GetRMNotesTechnicianConsole/"+str(RMOrderID)
	url = URLPath + apiPath		
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData=data.json
	print "resultData",resultData
	dataList = []
	j = 1 
	for i in resultData:	
		SrNo = j
		RMNotes =  i.get("RMNotes")
		CreatedOn = i.get("CreatedOn")
		system.perspective.print('CreatedOn : ' + str(CreatedOn))
		ShiftId = i.get("ShiftId")
		myList = [SrNo,RMNotes,CreatedOn,ShiftId]	
		dataList.append(myList)
		j = j+1
		
	headers =  ["Sr No","RMNotes","CreatedOn","ShiftId"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	print "resultDetails",resultDetails
	return resultDetails
	
def assignCoOperator(RMOrderID,assignedUserId,userId,statusId):
	scriptName="API:CoorperatorAssign"
	apiPath = "MaintenanceOperatorConsole/AssignMaintenanceCooperator"
	url = URLPath + apiPath		
	writeData = {
				  "workOrderId": int(RMOrderID),
				  "assignedTo": int(assignedUserId),
				  "assignedBy": int(userId),
				  "maintenanceTypeId": 2,#For Reactive Maintenance
				  "statusId": statusId
				}
		
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		print("PostReturn",postReturn)
	except:		
		result = 0
		pass
	print "result",result
	return result

def getAssignedOperators(RMOrderId,userId):
	maintenanceTypeId = 2 #Reactive Maintenance Type
	apiPath = "MaintenanceOperatorConsole/GetMaintennaceAssignedOperator?woOrderId="+str(RMOrderId)+"&maintenanceTypeId="+str(maintenanceTypeId)+"&userId="+str(userId)
	url = URLPath + apiPath		
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData=data.json	
	print "resultData",resultData
	dataList = []
	j = 1 
	for i in resultData:	
		SrNo = j
		AssignedName =  i.get("AssignedName")
		AssignedOn = i.get("AssignedOn")
		UserId = i.get("UserId")
	
		myList = [SrNo,AssignedName,AssignedOn,UserId]
		dataList.append(myList)
		j = j+1
		
	headers =  ["Sr No","Co-OperatorName","AssignedOn","UserId"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	print "resultDetails",resultDetails
	return resultDetails

# This will be used for Both Reactive & Preventive Maintenance 

#----------Function Start--Get SpareParts by MAchineID--------------------
def getSparePartsByMachineID(MachineID,WarehouseId,WoNumber):
	try: 
		scriptName="API:getSparePartsByMachineID"
		apiPath = apiPath = "MaintenanceOperatorConsoleRM/GetSparePartByMachine/"+str(MachineID)+"/"+str(WarehouseId)+"/"+str(WoNumber)
		url = URLPath + apiPath
		
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		
		j=1
		dataList = []
		for i in resultData:			
			SrNo = j
			sparePartID = i.get("id")
			sparePartName = i.get("sparePartName")
			onHandQty = i.get("onHandQty")
			RequestQty = i.get("RequestQty")
			ImagePath = i.get('ImagePath')
			TotalRequestedQty = i.get("TotalRequestedQuanity")
	
			myList = [SrNo,sparePartName,onHandQty,RequestQty,sparePartID,ImagePath,TotalRequestedQty]
			dataList.append(myList)
			j=j+1
			
		headers =  ["SrNo","sparePartName","onHandQty","RequestedQty","sparePartID","ImagePath","TotalRequestedQty"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
	
#----------Function End--Get SpareParts by MAchineID--------------------

#----------Function Start--Update SparePart Details --------------------
def updateSparePartDetails(resultData,WoNumber,userID,warehouseId):
	try: 
		scriptName="API:updateSparePartDetails"
		sparePartDataset = system.util.jsonDecode(resultData)

		arrayJson = []
		
		for sparePart in sparePartDataset:
		
			if sparePart[3] != int(0):
			
				jsonformat = {
				    "id": int(sparePart[4]),  #SparePartId
					"woNumber":WoNumber,
					"sparePartNo":sparePart[1], #Sparepart Name
					"onHandQty":int(sparePart[2]), #OnHandSty
					"requestedQty":int(sparePart[3]) #requestedQty
					}
				arrayJson.append(jsonformat)
			

		params = {
				"createdBy": userID,
				"warehouseId": warehouseId,
				"spareType": 2, #Sparepart Type is Maintenance
				"woNumber" : WoNumber,
				"requestSparePartDetailsListRM" : arrayJson
				}
				
		apiPath = "MaintenanceOperatorConsoleRM/SubmitRequestSparepart"
		url = URLPath + apiPath

		jsonParams = system.util.jsonEncode(params)

		resultDetails = 1
		
		try:
			system.perspective.print("API URL:"+str(url))
			system.perspective.print("API Input Data:"+str(jsonParams))
			system.perspective.print("API Method: Post")
		except:
			pass
		try:
			postReturn1 = system.net.httpPost(url,'application/json',jsonParams)
		except:		
			resultDetails = 0		
			pass
		system.perspective.print('Post Result Data: '+ str(resultDetails))			
		return resultDetails 
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)


#----------Function Start--Get History by RMOrderID--------------------
def getHistorybyRMOrderID(RMOrderID):
	apiPath = "MaintenanceOperatorConsoleRM/GetRMOrderHistory/" + str(RMOrderID)
	url = URLPath + apiPath
		
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData=data.json
	dataList = []
	j=1
	for i in resultData:
		ID = j
		WoNumber = i.get("WorkOrderNo")
		RMNumber = i.get("RMNumber")
		History = i.get("History")
		Comments = i.get("Comments")
		CreatedOn  = i.get("CreatedOn")
		CreatedBy = i.get("CreatedBy")
		j = j+1
		myList = [ID,WoNumber,RMNumber,History,Comments,CreatedOn,CreatedBy] 		
		dataList.append(myList)		
	headers = ["SrNo","WoNumber","RMNumber","History","Comments","CreatedOn","CreatedBy"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	print "resultDetails",resultDetails
	return resultDetails

#----------Function End--Get History by RMOrderID-----------------------
		
#----------Function Start--Get Consumed Spare Parts by RM-Number--------------------
def getConsumedSparePartsByWoNumber(WoNumber,IsHistory):
	try: 
		scriptName="API:getConsumedSparePartsByWoNumber"
		apiPath = "MaintenanceOperatorConsoleRM/GetRequestSpareDetailsinConsumedSparePart/"+str(WoNumber)
		url = URLPath + apiPath
		try:
			system.perspective.print("API URL:"+str(url))
#			system.perspective.print("API Input Data:"+str(jsonParams))
			system.perspective.print("API Method: Get")
		except:
			pass
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		
		if IsHistory == int(1) or IsHistory == 1 or IsHistory == str('1'):	
			dataList = []
			j=1
			for i in resultData:			
				IsHistory = i.get("IsHistory")
				if IsHistory == int(1) or IsHistory == 1 or IsHistory == str(1):
					ID = j
					sparePartName = i.get("SparepartName")
					consumedQty = i.get("ConsumedQty")
					consumedBy = i.get("ConsumedBy")
					consumedOn = i.get("ConsumedOn")
					comments = i.get("Comment")
#					system.perspective.print('consumedOn : ' + str(consumedOn))
					
#					parsed_timestamp = datetime.strptime(consumedOn, "%Y-%m-%dT%H:%M:%S.%f%z")
#					desired_format = "%Y-%m-%d %H:%M:%S"
#					consumedOn = parsed_timestamp.strftime(desired_format)

					system.perspective.print('consumedOn : ' + str(consumedOn))
					
					myList = [ID,sparePartName,consumedQty,consumedBy,consumedOn,comments]
					dataList.append(myList)
					j = j+1
				
			headers =  ["Sr No","Sparepart Name","Consumed Qty","Consumed By","Consumed On","Comments"]
			resultDetails = system.dataset.toDataSet(headers,dataList)
			newData = system.dataset.sort(resultDetails, "Consumed On", False)
			return newData
			print "resultDetails for Consumed History",newData
		else:
			dataList = []
			j=1
			for i in resultData:
				IsHistory = i.get("IsHistory")
				print'IsHistory',IsHistory
				if str(IsHistory).lower() == "null" or str(IsHistory).lower() == "none":
					IsHistory = 0
				if IsHistory == int(0) or IsHistory == 0 or IsHistory == str(0):			
					print "Is history == 0"
					ID = j
					sparePartName = i.get("SparepartName")
					sparePartCode = i.get("SparePartNo")
					requestedQty = i.get("RequestedQty")
					allocatedQty  =i.get("AllocatedQty")
					consumedQty =i.get("ConsumedQty")
					TotalConsumedQty = i.get("TotalConsumedQty")
					RequestId = i.get("RequestId")
					IsHistory = i.get("IsHistory")

					AvailableQty = int(allocatedQty) - int(TotalConsumedQty)
					consumedQty = AvailableQty
					comments= ""
				
				
					myList = [ID,sparePartName,sparePartCode,requestedQty,allocatedQty,consumedQty,TotalConsumedQty,RequestId,IsHistory,AvailableQty,comments]		
					dataList.append(myList)
					j = j+1
				
				
			headers =  ["ID","SparePart","SparePartCode","RequestedQty","AllocatedQty","ConsumedQty","TotalConsumedQty","RequestId","IsHistory","AvailableQty","Comments"]
			resultDetails = system.dataset.toDataSet(headers,dataList)	
			return resultDetails
			print "resultDetails To Consume SpareParts",resultDetails
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: CLRI:: Area Dropdown: On Action Performed :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)


def getRequestedSparePartsByWoNumber(WoNumber):
	try: 
		scriptName="API:getRequestedSparePartsByWoNumber"	
		apiPath = "MaintenanceOperatorConsoleRM/GetRequestSpareDetailsinRequestSparePart/"+str(WoNumber)
		url = URLPath + apiPath	
		try:
			system.perspective.print("API URL:"+str(url))
#			system.perspective.print("API Input Data:"+str(jsonParams))
			system.perspective.print("API Method: Get")
		except:
			pass	
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json	
		dataList = []
		j=1
		for i in resultData:	
			SrNo = j
			sparePartName = i.get("SparepartName")
#			sparePartCode = i.get("SparePartNo")
#			OnHandQty = i.get("ONHandQty")
#			AllocatedQty = i.get("AllocatedQty")
#			AllocatedQty = "" #Changed by Omkar on 28th-Nov-2022 (Allocated Qty is not needed for Requested Qty)
			RequestedQty = i.get("RequestedQty")
			RequestedBy = i.get("RequestedBy")
			RequestedOn =i.get("RequestedOn")
			RequestNumber = i.get("requestNumber")

			system.perspective.print('RequestedOn : ' + str(RequestedOn))

			myList = [SrNo,sparePartName,RequestedQty,RequestedBy,RequestedOn,RequestNumber]
			dataList.append(myList)
			j = j+1
			
		headers =  ["SrNo","SparepartName","RequestedQty","RequestedBy","RequestedOn","RequestNumber"]
		resultDetails = system.dataset.toDataSet(headers,dataList)	
		print ("resultDetails")
		newData = system.dataset.sort(resultDetails, "RequestedOn", False)
		return newData
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)	
		
#----------Function End--Get Requested Spare Parts by RM-Number----------------------------------------->

#----------Function Start--Submit Consumed Parts -------------------------------------------------------->
def submitConsumedParts(resultData,WoNumber,userId,warehouseId):
	system.perspective.print("submitConsumedParts Inside Function submit: ")
	try: 
		scriptName="API:submitConsumedParts"
		sparePartDataset = system.util.jsonDecode(resultData)
		arrayJson = []
		
		for sparePart in sparePartDataset :
			requestId = int(sparePart[7])
			Comments = sparePart[10]
			system.perspective.print("requestId:: " + str(requestId))
			system.perspective.print("Comments:: " + str(Comments))
			jsonformat = {
				
#				"sparePartNo":sparePart[2], #"P001"
				"sparePartNo":sparePart[1], #"P001"
				"requestedQty":sparePart[3], #sparePart[5]
				"serialNo": "",#sparePart[5], #Not Needed now
				"lotNo": "",#sparePart[6],#Not Needed now
				"consumedQty":sparePart[5],
				"comment" : Comments
				}

			arrayJson.append(jsonformat)
		
		system.perspective.print("arrayJson:: " + str(arrayJson))
		
		params = {
				"createdBy" : userId,
				"warehouseId": warehouseId,
				"requestId" : requestId,
				"woNumber" : WoNumber,
				"requestSparePartDetailsListRM" : arrayJson
				}
		apiPath = "MaintenanceOperatorConsoleRM/SubmitConsumedSparepart"
		url = URLPath + apiPath
		jsonParams = system.util.jsonEncode(params)
		system.perspective.print("jsonParams:: " + str(jsonParams))
		
		result = 1
		try:
			system.perspective.print("API URL:"+str(url))
			system.perspective.print("API Input Data:"+str(jsonParams))
			system.perspective.print("API Method: Post")
		except:
			pass
		try:
			postReturn1 = system.net.httpPost(url,'application/json',jsonParams)
			system.perspective.print("postReturn1:: " + str(postReturn1))
		except:		
			result = 0		
			pass
			
		resultData = system.util.jsonDecode(postReturn1)
		return result
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: PMTC:: Submit Consume parts :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)
# IMAGE APIS________________________________________________________________

def GetUploadedFilesMaintaince(mId,typeId,toolId):
	try: 
		scriptName="API:GetUploadedFilesMaintaice Get URL Path"	
		apiPath = "MaintenanceLeadConsole/GetUploadedFiles/"+str(mId)+"/"+str(typeId)+"/"+str(toolId)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json	
		dataList = []
		j=1
		for i in resultData:	
			SrNo = j	
			mId = i.get("id")
			name = i.get("fileName")
			name =name.replace('\\','/')
			name =name.replace('\\','/')
			name =name.replace('//','/')		
#			openingUrl="http://172.28.3.206/FactoryMagix/"  
			fileName = openingUrl+name    
			
			myList = [SrNo,mId,fileName]
			dataList.append(myList)
			j = j+1
			
		headers =  ["SrNo","Id","fileName"]
		resultDetails = system.dataset.toDataSet(headers,dataList)	
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		print errorMessage
		Authentication.exceptionLogger(errorMessage)	
		return None
#----------Function End--Get Image path--------------------


#----------Function Start--submitUploadedFilesMaintenanceLeadConsole --------------------


#----------Function Start--Get Image Path  --------------------
def GetUploadedFilesMaintaince(mId,typeId,toolId):
	try: 
		scriptName="API:GetUploadedFilesMaintaice Get URL Path"	
		system.perspective.print("mId = "+str(mId))
		system.perspective.print("typeId = "+str(typeId))
		system.perspective.print("toolId = "+str(toolId))
		apiPath = "MaintenanceLeadConsole/GetUploadedFiles/"+str(mId)+"/"+str(typeId)+"/"+str(toolId)
		url = URLPath + apiPath
		system.perspective.print("url = "+str(url))
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json	
		dataList = []
		j=1
		for i in resultData:	
			SrNo = j	
			mId = i.get("id")
			name = i.get("fileName")
			name =name.replace('\\','/')
			name =name.replace('\\','/')
			name =name.replace('//','/')		
#			openingUrl="http://172.28.3.206/FactoryMagix/"  
			fileName = openingUrl+name    
			
			myList = [SrNo,mId,fileName]
			dataList.append(myList)
			j = j+1
			
		headers =  ["SrNo","Id","fileName"]
		resultDetails = system.dataset.toDataSet(headers,dataList)	
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		print errorMessage
		Authentication.exceptionLogger(errorMessage)	
		return None
#----------Function End--Get Image path--------------------


#----------Function Start--submitUploadedFilesMaintenanceLeadConsole --------------------


def submitUploadedFilesMaintenanceLeadConsole(userID,mId,typeId,maintenanceTypeId,myObj):
	try: 
		scriptName="API:submitUploadedFilesMaintenanceLeadConsole"
		apiPath = "MaintenanceLeadConsole/CreateFile"
		system.perspective.print("call submitUploadedFilesMaintenanceLeadConsole")
		system.perspective.print("mId = "+str(mId))
		system.perspective.print("userID = "+str(userID))
		system.perspective.print("typeId Sagar = "+str(typeId))
		system.perspective.print("maintenanceTypeId = "+str(maintenanceTypeId))
		url = URLPath + apiPath	
		system.perspective.print("url inside  = "+str(url))
#		system.perspective.print("url" +str(url))
		writeData = {
			"isActive": True,
			"createdBy": userID,
			"createdOn": "2022-12-14T11:36:36.985Z",
		    "modifiedBy": 0,
			 "modifiedOn": "2022-12-14T11:36:36.985Z",
		    "isArchive": True,
			"id": mId,
			"typeId": maintenanceTypeId,
			"maintenanceTypeId":typeId ,
			"imgPath": myObj		
		}
		
		jsonParams = system.util.jsonEncode(writeData)		
#	"typeId": typeId,
#					"maintenanceTypeId": maintenanceTypeId,	
		resultDetails = None
		try:
#			system.perspective.print("url myObj "+str(myObj))
			resultDetails = system.net.httpPost(url,'application/json',jsonParams)
			system.perspective.print("resultDetails= "+str(resultDetails))
			system.perspective.print("call message handler")
			messageType = 'msgHandMainImageDisplay'
			system.perspective.sendMessage(messageType, scope='page')
		except:
			import sys, os		
			errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
			Authentication.exceptionLogger(errorMessage)
			
			system.perspective.print("errorMessage= ",errorMessage)
			return None
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		print errorMessage
		system.perspective.print("errorMessage= ",errorMessage)
		return None
#----------Function End--submitUploadedFilesMaintenanceLeadConsole --------------------		

#----------Function Start delete--UploadedFilesMaintenanceLeadConsole --------------------


def deleteUploadedFilesMaintenanceLeadConsole(Id):
	try: 
		scriptName="API:deleteUploadedFilesMaintenanceLeadConsole"
		apiPath = "MaintenanceLeadConsole/DeleteFile/"+str(Id)

		url = URLPath + apiPath		
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		result = 1
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		print errorMessage
		return 0
#----------Function End delete--UploadedFilesMaintenanceLeadConsole --------------------

def GetPMOrderDetailsForImageUpload(pmOrderId):
    try:
		scriptName = "API: Get Get PM OrderDetailsForImageUpload"
		apiPath = "MaintenanceOperatorConsole/GetPMOrderDetailsForImageUpload?pmOrderId="+str(pmOrderId)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		dataList = []
		j=1
		for i in resultData:        
			ID = j
			PMOrderId = i.get("PMOrderId")
			Name = i.get("Name")
			MaintenanceType=i.get("MaintenanceType")
			MaintenanceTypeName=''
			if MaintenanceType==1 or  str(MaintenanceType)=='1':
				MaintenanceTypeName='Equipment'
			if MaintenanceType==2  or  str(MaintenanceType)=='2':	
				MaintenanceTypeName='Tool'
				
				
			myList = [PMOrderId,Name,MaintenanceType,MaintenanceTypeName]
			
			dataList.append(myList)    
			j = j+1
                
		headers = ["PMOrderId","Name","MaintenanceType","MaintenanceTypeName"]
		
		resultDetails = system.dataset.toDataSet(headers,dataList)
		resultDetails = system.dataset.toPyDataSet(resultDetails)
		return resultDetails
    except:        
        import sys, os
        errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
        Authentication.exceptionLogger(errorMessage)
        
        
def GetRMOrderDetailsForImageUpload(rmOrderId):
    try:
		scriptName = "API: Get GetRMOrderDetailsForImageUpload"
		apiPath = "MaintenanceOperatorConsole/GetRMOrderDetailsForImageUpload?rmOrderId="+str(rmOrderId)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		dataList = []
		j=1
		for i in resultData:        
			ID = j
			PMOrderId = i.get("RMOrderId")
			Name = i.get("Name")
			MaintenanceType=i.get("MaintenanceType")
			MaintenanceTypeName=''
			if MaintenanceType==1 or  str(MaintenanceType)=='1':
				MaintenanceTypeName='Equipment'
			if MaintenanceType==2  or  str(MaintenanceType)=='2':	
				MaintenanceTypeName='Tool'
				
				
			myList = [PMOrderId,Name,MaintenanceType,MaintenanceTypeName]
			
			dataList.append(myList)    
			j = j+1
                
		headers = ["RMOrderId","Name","MaintenanceType","MaintenanceTypeName"]
		
		resultDetails = system.dataset.toDataSet(headers,dataList)
		resultDetails = system.dataset.toPyDataSet(resultDetails)
		return resultDetails
    except:        
        import sys, os
        errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
        Authentication.exceptionLogger(errorMessage)     


def GetRMOrdersUploadedFiles(mId,typeId,toolId):
	try: 
		scriptName="API:GetUploadedFilesMaintaice Get URL Path"	
		apiPath = "MaintenanceLeadConsole/GetRMOrdersUploadedFiles/"+str(mId)+"/"+str(typeId)+"/"+str(toolId)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json	
		dataList = []
		j=1
		for i in resultData:	
			SrNo = j	
			mId = i.get("id")
			name = i.get("fileName")
			name =name.replace('\\','/')
			name =name.replace('\\','/')
			name =name.replace('//','/')		
#			openingUrl="http://172.28.3.206/FactoryMagix/"  
			fileName = openingUrl+name    
			
			myList = [SrNo,mId,fileName]
			dataList.append(myList)
			j = j+1
			
		headers =  ["SrNo","Id","fileName"]
		resultDetails = system.dataset.toDataSet(headers,dataList)	
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		print errorMessage
		Authentication.exceptionLogger(errorMessage)	
		return None
#----------Function End--Get Image path--------------------    

def submitUploadedFilesRMMaintenanceLeadConsole(userID,mId,typeId,maintenanceTypeId,myObj):
   	try: 
   		scriptName="API:submitUploadedFilesRMMaintenanceLeadConsole"
   		apiPath = "MaintenanceLeadConsole/RMOrdersImageUpload"
   		system.perspective.print("call submitUploadedFilesRMMaintenanceLeadConsole")
   		system.perspective.print("mId = "+str(mId))
   		system.perspective.print("userID = "+str(userID))
   		system.perspective.print("typeId Sagar = "+str(typeId))
   		system.perspective.print("maintenanceTypeId = "+str(maintenanceTypeId))
   		url = URLPath + apiPath	
   		system.perspective.print("url inside  = "+str(url))
   #		system.perspective.print("url" +str(url))
   		writeData = {
   			"isActive": True,
   			"createdBy": userID,
   			"createdOn": "2022-12-14T11:36:36.985Z",
   		    "modifiedBy": 0,
   			 "modifiedOn": "2022-12-14T11:36:36.985Z",
   		    "isArchive": True,
   			"id": mId,
   			"typeId": maintenanceTypeId,
   			"maintenanceTypeId":typeId ,
   			"imgPath": myObj		
   		}
   		
   		jsonParams = system.util.jsonEncode(writeData)		
   #	"typeId": typeId,
   #					"maintenanceTypeId": maintenanceTypeId,	
   		resultDetails = None
   		try:
   #			system.perspective.print("url myObj "+str(myObj))
   			resultDetails = system.net.httpPost(url,'application/json',jsonParams)
   			system.perspective.print("resultDetails= "+str(resultDetails))
   			system.perspective.print("call message handler")
   			messageType = 'msgHandMainImageDisplay'
   			system.perspective.sendMessage(messageType, scope='page')
   		except:
   			import sys, os		
   			errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
   			Authentication.exceptionLogger(errorMessage)
   			
   			system.perspective.print("errorMessage= ",errorMessage)
   			return None
   		return resultDetails
   	except:
   		import sys, os
   		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
   		Authentication.exceptionLogger(errorMessage)
   		print errorMessage
   		system.perspective.print("errorMessage= ",errorMessage)
   		return None
   #----------Function End--submitUploadedFilesMaintenanceLeadConsole --------------------
   
def deleteUploadedFilesRMMaintenanceLeadConsole(Id):
   	try: 
   		scriptName="API:deleteUploadedFilesRMMaintenanceLeadConsole"
   		apiPath = "MaintenanceLeadConsole/DeleteRMOrderUploadedFile/"+str(Id)
   
   		url = URLPath + apiPath		
   		request = urllib2.Request(url)
   		response = urllib2.urlopen(request)
   		data = system.net.httpGet(url)
   		resultData= system.util.jsonDecode(data)
   		result = 1
   	except:
   		import sys, os
   		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
   		Authentication.exceptionLogger(errorMessage)
   		print errorMessage
   		return 0
   #----------Function End delete--UploadedFilesMaintenanceLeadConsole --------------------   		          
#Below Two functions are used in Production Operator console SCreen 

def getOperationsbyWorkorderId(selectedWorkorderId):
	apiPath = "ProductionOperatorConsole/GetOperationByWorkOrderId/workOrderId:int?workOrderId="+str(selectedWorkorderId)
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
		OperationId = i.get("OperationId")
		OperationName = i.get("Operation Name")	
		myList = [OperationId,OperationName] 
		print myList
		if OperationId not in oprList:	
			dataList.append(myList)	
			oprList.append(OperationId)
		else:
			continue
	headers = ["WorkflowOperationsId","Operation"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	print resultDetails
	return resultDetails


def getMachinesbyWorkorderId(selectedWorkorderId,selectedOperationId):
   	apiPath = "ProductionOperatorConsole/GetOperationByWorkOrderId/workOrderId:int?workOrderId="+str(selectedWorkorderId)
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
   		OperationId = i.get("OperationId")
   		if int(OperationId) == int(selectedOperationId):
   			MachineId = i.get("MachineId")	
   			MachineName = i.get("Machine Name")	
   			myList = [MachineId,MachineName]
   			if MachineId not in oprList:	
   				dataList.append(myList)	
   				oprList.append(MachineId)
   			else:
   				continue
   	headers = ["MachineId","MachineName"]
   	resultDetails = system.dataset.toDataSet(headers,dataList)
   	print resultDetails
   	return resultDetails	
   	
def GetSkilledUserByMaintenanceType(maintenanceTypeId,RMOrderId,userId):
   	AssigendData=MaintenanceRMAPI.getAssignedOperators(RMOrderId,userId)
   	Index= AssigendData.getColumnIndex('UserId')
   	print 'Index',Index
   	AssinedUserList = AssigendData.getColumnAsList(Index)
   	print 'AssinedUserList',AssinedUserList
   	
   	apiPath = "MaintenanceOperatorConsole/GetUsersByMaintenanceType?maintenanceTypeId="+str(maintenanceTypeId)+"&userId="+str(userId)
   	url = URLPath + apiPath
   	
   	request = urllib2.Request(url)
   	response=urllib2.urlopen(request)
   	data = system.net.httpGet(url)
   	
   	resultData= system.util.jsonDecode(data)
   	
   	dataList = []
   	for i in resultData:	
   		UserID = i.get("UserId")
   		if UserID  not in AssinedUserList:
   			UserName = i.get("FullName")
   			myList = [UserID,UserName] 
   			print 'myList',myList
   			dataList.append(myList)
   	
   	headers = ["EmployeeId","Username"]
   	resultDetails = system.dataset.toDataSet(headers,dataList)
   	print 'resultDetails',resultDetails
   	return resultDetails 
   	

def GetToolList(WorkorderId):
  	apiPath = "MaintenanceOperatorConsoleRM/GetToolList/"+str(WorkorderId)  	
  	url = URLPath + apiPath
  	print url
 	
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData=data.json
  	print resultData
  	dataList = []
  	for i in resultData:
  		ToolId = i.get("ToolId")
  		ToolName = i.get("ToolName")
  		ToolCode = i.get("ToolCode")
  		myList = [ToolId,ToolName]
  		dataList.append(myList)	  	
  	headers = ["ToolId","ToolName"]
  	resultDetails = system.dataset.toDataSet(headers,dataList)
  	return resultDetails
  	

def GetMakeModel(ToolId):
 	apiPath = "MaintenanceOperatorConsoleRM/GetMakeModelByToolId/"+str(ToolId)   	
 	url = URLPath + apiPath
 	print url     	
  	client = system.net.httpClient()
  	data = client.get(url)
  	if data.good:    
  		resultData=data.json
     	print resultData

 	return resultData 	                  		                           

def ChangeDatetimeFormat(parameter):
	parsed_timestamp = datetime.strptime(input_timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
	desired_format = "%Y-%m-%d %H:%M:%S"
	formatted_timestamp = parsed_timestamp.strftime(desired_format)
	return formatted_timestamp