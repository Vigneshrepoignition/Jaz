import re
import json
import urllib2, urllib
global system
import system   
import java.lang.Exception
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
#URLPath = system.tag.read("[default]JMES_InternalTags/urlSITAPI").value
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

#This is user for both RM and PM (Maintenance Type Id = 1 for Preventive Maintenance and 2 for Reactive Maitenance)
def GetSkilledUserByMaintenanceType(maintenanceTypeId,userId):
	apiPath = "MaintenanceOperatorConsole/GetUsersByMaintenanceType?maintenanceTypeId="+str(maintenanceTypeId)+"&userId="+str(userId)
	url = URLPath + apiPath

	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)
	
	resultData= system.util.jsonDecode(data)
	dataList = []
	for i in resultData:	
		UserID = i.get("UserId")
		UserName = i.get("FullName")
		myList = [UserID,UserName] 		
		dataList.append(myList)

	headers = ["EmployeeId","Username"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails



def getPMType():
	headers = ["TypeID", "PMTypeName"]
	data = []
	data.append(["1", "Machine Type"])
	data.append(["2", "Tool Type"])
	Types = system.dataset.toDataSet(headers, data)
	return Types

def getPMOrderDetailsforAssign(userID,TypeId):
	try:
		scriptName = "PMORderDetails"
		apiPath = "MaintenanceOperatorConsole/GetPMOperatorConsoleWorkOrders?UserId="+str(userID)+"&maintenanceType="+str(TypeId)
		url = URLPath + apiPath
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
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)

def getCompleteWODetailsForUser(userID,TypeId):
	try:
		scriptName = "API: Get Complet PM Orders by UserID"
		apiPath = "MaintenanceOperatorConsole/GetPMOperatorConsoleWorkOrders?UserId="+str(userID)+"&maintenanceType="+str(TypeId)
		url = URLPath + apiPath
		system.perspective.print("API URL:"+str(url))
		system.perspective.print("API Method: Get")
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		
		if TypeId == int(1) or TypeId == 1 or TypeId == str('1'):
			dataList = []
			j=1
			for i in resultData:			
				ID = j
				PMNumber = i.get("WO Number")
				Type = i.get("Type")
				lineName= i.get("LineName")
				Name = i.get("Name")
				Workflow= i.get("Workflow")
				Status = i.get("Status")
				StartDate = i.get("Start Date")	
				ActualStartDate = i.get("Actual Start Date")	
				DueDate = i.get("Due Date")
				ActualCompletionDate = i.get("Actual Completion Date")
				Assign = ""
				viewDetails = ""
				EquipmentID= i.get("EquipmentID")
				WorkflowId= i.get("WorkflowId")
				StatusId= i.get("StatusId")
				EnterpriseName = i.get("Enterprise Name")	
				PlantName = i.get("Plant Name")
				PlantID = i.get("PlantID")			
				areaID= i.get("AreaId")
				areaName= i.get("AreaName")
				lineID= i.get("LineId")	
				machineID= i.get("MachineId")
				machineName= i.get("Machine Name")
				PMOrderID= i.get("PMOrder ID")
				WorkflowOperationsId= i.get("OperationID")
				Process= i.get("Process")
				WarehouseName = i.get("WarehouseName")
				WarehouseId = i.get("WarehouseId")
				
				if str(ActualStartDate) == str("null") or ActualStartDate == None: 
					ActualStartDate = ''
				else:
					ActualStartDate = ActualStartDate					
				
				myList = [ID,PMNumber,Type,lineName,Name,Workflow,Status,StartDate,ActualStartDate,DueDate,ActualCompletionDate,Assign,viewDetails,EquipmentID,WorkflowId,StatusId,EnterpriseName,PlantName,PlantID,areaID,areaName,lineID,machineID,machineName,PMOrderID,WorkflowOperationsId,Process,WarehouseName,WarehouseId]	
				
				dataList.append(myList)	
				j = j+1
			
			headers = ["ID","PMNumber","Type","lineName","Name","Workflow","Status","StartDate","ActualStartDate","DueDate","ActualCompletionDate","Assign","View_Details","EquipmentID","WorkflowId","StatusId","EnterpriseName","PlantName","PlantID","areaID","areaName","lineID","machineID","machineName","PMOrderID","WorkflowOperationsId","Process","WarehouseName","WarehouseId"]
			resultDetails = system.dataset.toDataSet(headers,dataList)
			return resultDetails
		else:
			dataList = []
			j=1
			for i in resultData:			
				ID = j
				MaintenanceWorkflowName= i.get("Workflow")
				PMNumber = i.get("WO Number")
				ToolName= i.get("Tool Name")
				Status = i.get("Status")
				StartDate = i.get("Start Date")	
				ActualStartDate = i.get("Actual Start Date")	
				ActualCompletionDate = i.get("Actual Completion Date")
				Assign = ""
				viewDetails = ""
				WorkflowId= i.get("WorkflowId")
				PMOrderID= i.get("PMOrder ID")
				ToolId = i.get("ToolId")
				StatusId= i.get("StatusId")
				WarehouseName = i.get("WarehouseName")
				WarehouseId = i.get("WarehouseId")
				
				if str(ActualStartDate) == str("null") or ActualStartDate == None: 
					ActualStartDate = ''
				else:
					ActualStartDate = ActualStartDate	

				
				myList = [ID,MaintenanceWorkflowName,PMNumber,ToolName,Status,StartDate,ActualStartDate,ActualCompletionDate,Assign,viewDetails,WorkflowId,PMOrderID,ToolId,StatusId,WarehouseName,WarehouseId]
				dataList.append(myList)	
				j = j+1
			
			headers = ["ID","MaintenanceWorkflowName","PMNumber","ToolName","Status","StartDate","ActualStartDate","ActualCompletionDate","Assign","viewDetails","WorkflowId","PMOrderID","ToolId","StatusId","WarehouseName","WarehouseId"]
			resultDetails = system.dataset.toDataSet(headers,dataList)
			return resultDetails
	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
#-------------------------------------------------------------------------Function END --------------------------------------------------------------------------------------------------------------------------	
def getUserAssignedWOList(enterpriseID,plantID,areaID,lineID,machineID,userId):
    try:
		scriptName = "API: Get User Assigned WO List"
		apiPath = "MaintenanceOperatorConsole/GetMaintenanceOperatorConsoleWorkOrdersonInput?EnterpriseId="+str(enterpriseID)+"&PlantId="+str(plantID)+"&AreaId="+str(areaID)+"&LineId="+str(lineID)+"&MachineId="+str(machineID)+"&UserId="+str(userId)                
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
			PMNumber = i.get("WO Number")
			Type = i.get("Type")
			Name = i.get("Name")
			#            Operation = i.get("Operation")
			Workflow= i.get("Workflow")
			Status = i.get("Status")    
			StartDate = i.get("Start Date")    
			ActualStartDate = i.get("Actual Start Date")  
			if str(ActualStartDate) == str("null") or ActualStartDate == None: 
				ActualStartDate = ''
			else:
				ActualStartDate = ActualStartDate	
			    
			DueDate = i.get("Due Date")
			ActualCompletionDate = i.get("Actual Completion Date")
			Assign = ""
			viewDetails = ""
			EquipmentID= i.get("EquipmentID")
			WorkflowId= i.get("WorkflowId")
			StatusId= i.get("StatusId")    
			EnterpriseName = i.get("Enterprise Name")
			PlantName = i.get("Plant Name")
			PlantID = i.get("PlantID")    
			areaID= i.get("AreaId")
			areaName= i.get("AreaName")
			lineID= i.get("LineId")
			lineName= i.get("LineName")
			machineID= i.get("MachineId")
			machineName= i.get("Machine Name")
			PMOrderID= i.get("PMOrder ID")
			WorkflowOperationsId= i.get("OperationID")
			Process= i.get("Process")
			WarehouseName = i.get("WarehouseName")
			
			myList = [ID,PMNumber,Type,Name,Workflow,Status,StartDate,ActualStartDate,DueDate,ActualCompletionDate,Assign,viewDetails,EquipmentID,WorkflowId,StatusId,EnterpriseName,PlantName,PlantID,areaID,areaName,lineID,lineName,machineID,machineName,PMOrderID,WorkflowOperationsId,Process,WarehouseName]    
			
			dataList.append(myList)    
			j = j+1
                
		headers = ["ID","PMNumber","Type","Name","Workflow","Status","StartDate","ActualStartDate","DueDate","ActualCompletionDate","Assign","View_Details","EquipmentID","WorkflowId","StatusId","EnterpriseName","PlantName","PlantID","areaID","areaName","lineID","lineName","machineID","machineName","PMOrderID","WorkflowOperationsId","Process","WarehouseName"]
		
		resultDetails = system.dataset.toDataSet(headers,dataList)
		resultDetails = system.dataset.toPyDataSet(resultDetails)
		return resultDetails
    except:        
        import sys, os
        errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
        Authentication.exceptionLogger(errorMessage)

#-----------Function Start--Assign PM Order ------------------------------
def AssignPmOrder(PMOrderID,WoNumber,userID):	
	try: 
		scriptName="API:AssignPMOrder"
		apiPath = "MaintenanceOperatorConsole/OperationStatusConformation"
		url = URLPath + apiPath		
		writeData = {
		  "CreatedBy": int(userID),
		  "pmOrderID" : int(PMOrderID),
		  "statusId": 7
			}
		jsonParams = system.util.jsonEncode(writeData)		
		result = 1
		try:
			system.perspective.print("API URL:"+str(url))
			system.perspective.print("API Input Data:"+str(jsonParams))
			system.perspective.print("API Method: Post")
		except:
			pass
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

		#-----------Function End--Assign PM Order ------------------------------
def startOperation(PMOrderID,WoNumber,userID):	
	try:
		scriptName = "API: Start Operation Post"
		apiPath = "MaintenanceOperatorConsole/OperationStatusConformation"
		url = URLPath + apiPath		
		writeData = {
		  "CreatedBy": int(userID),
		  "pmOrderID" : int(PMOrderID),
		  "statusId": 1
			}
		jsonParams = system.util.jsonEncode(writeData)		
		result = 1
		try:
			system.perspective.print("API URL:"+str(url))
			system.perspective.print("API Input Data:"+str(jsonParams))
			system.perspective.print("API Method: Post")
		except:
			pass
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
		
def holdOperation(WoNumber,PMOrderID,holdReasonId,holdComment,userID):
	try:
		scriptName="API:Hold Operations"
		apiPath = "MaintenanceOperatorConsole/OperationStatusConformation"	
		url = URLPath + apiPath
		writeData = {
		  "isActive": True,
		  "createdBy": int(userID),
		  "createdOn": "2022-07-14T07:11:53.757Z",
		  "modifiedBy": int(userID),
		  "modifiedOn": "2022-07-14T07:11:53.757Z",
		  "workOrderNo": str(WoNumber),
		  "reasonCodeId": int(holdReasonId),
		  "reasonCodeComments": holdComment,	
		  "actualHoldDate": "2022-07-14T07:11:53.758Z",	
		  "pmOrderID" : int(PMOrderID),
		  "statusId": 2
		}
		jsonParams = system.util.jsonEncode(writeData)		
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)	
		except:		
			result = 0
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		
				
def getSingleWORow(PMOrderID):
	try:
		scriptName="API:Get Single PM Order Row"
		apiPath ="MaintenanceOperatorConsole/GetPMOperatorConsoleWorkOrderDetails?pmOrderId="+str(PMOrderID)
		url = URLPath + apiPath	
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		print "data",data
		if data.good:    
			resultData=data.json
			print "resultData",resultData
		return resultData
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)

def resumeHoldOperation(PMOrderID,WoNumber,resumeComment,userID):
	try: 
		scriptName="API:Resume Hold Operation"
		apiPath = "MaintenanceOperatorConsole/OperationStatusConformation"	
		url = URLPath + apiPath
		writeData = {
		  "isActive": True,
		  "createdBy": int(userID),
		  "createdOn": "2022-07-14T07:52:06.677Z",
		  "modifiedBy": int(userID),
		  "workOrderNo": str(WoNumber),	
		  "reasonCodeComments": resumeComment,	
		  "actualResumeDate": "2022-07-14T07:52:06.678Z",	
		  "pmOrderID" : int(PMOrderID),	
		  "statusId": 1
		}
		
		jsonParams = system.util.jsonEncode(writeData)		
		result = 1
		try:
			system.perspective.print("API URL:"+str(url))
			system.perspective.print("API Input Data:"+str(jsonParams))
			system.perspective.print("API Method: Post")
		except:
			pass
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)	
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
			
def completeOperation(WoNumber,PMOrderID,commentText,holdReasonId,CompleteCategoryID,userID):
	try:
		scriptName = "API : Complete Operation Post"
		apiPath = "MaintenanceOperatorConsole/OperationStatusConformation" 
		url = URLPath + apiPath
		writeData = {
		  "isActive": True,
		  "createdBy": int(userID),
		  "createdOn": "2022-07-14T07:56:52.652Z",
		  "modifiedBy": int(userID),
		  "modifiedOn": "2022-07-14T07:56:52.652Z",
		  "workOrderNo": str(WoNumber),	
		  "reasonCodeComments": commentText,
		  "reasonCodeId": int(holdReasonId),
		  "reasonCategoryId": str(CompleteCategoryID),	
		  "actualCompletionDate": "2022-07-14T07:56:52.652Z",	
		  "pmOrderID" : int(PMOrderID),	
		  "statusId": 3	
		}
		
		jsonParams = system.util.jsonEncode(writeData)		
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
			
		except:		
			result = 0
			pass
		return result
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		
# Get PM Order History by PMOrderID
def getHistorybyPMOrderID(PMOrderID):
	try:
		scriptName = "API: Get History By PM Order ID"
		apiPath = "MaintenanceOperatorConsole/GetPMOrderHistory/"+str(PMOrderID)
		url = URLPath + apiPath
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		data = system.net.httpGet(url)
		#print(data)
		resultData= system.util.jsonDecode(data)
		dataList = []
		j=1
		for i in resultData:
			ID = j
			PMNumber = i.get("PMNumber")
			History = i.get("History")
			Comments = i.get("Comments")
			CreatedOn  = i.get("CreatedOn")
			CreatedBy = i.get("CreatedBy")
			j = j+1
			myList = [ID,PMNumber,History,Comments,CreatedOn,CreatedBy] 		
			dataList.append(myList)		
		headers = ["SrNo","PMNumber","History","Comments","CreatedOn","CreatedBy"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		print "resultDetails",resultDetails
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
	
#--------------------Get Task List By TaskTypeID ----------------------------------------------------------------
def GetTasksListbyType(MaintenanceworkflowId,PMOrderID,TaskTypeId):
	try:
		scriptName = "API : Get TaskList By Type"
		apiPath ="MaintenanceOperatorConsole/GetPMTasksForOperatorConsoleWorkOrder?maintenanceWorkflowId="+str(MaintenanceworkflowId)+"&pmOrderId="+str(PMOrderID)
		url = URLPath + apiPath	
		system.perspective.print('GetPMTasksForOperatorConsoleWorkOrder url :' + str(url))
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		dataList = []
		j = 1 
		if TaskTypeId == 1:
			for i in resultData:	
				SrNo = j
				TaskID =  i.get("id")
				TaskName = i.get("name")
				TaskDescription = i.get("TaskDescription")
				Action = i.get("TaskRemark") #Comment Field for text Type 
				OkSelected = i.get("OkSelected") #OK Field
				TaskTypeID = i.get("type")
				TaskRemarkId = i.get("TaskRemarkId")
				
				if str(OkSelected).lower().strip()=='true' or str(OkSelected)=='True' or str(OkSelected)=='1':
					OkSelected=True
				else:
					OkSelected=False

				if TaskTypeID == 1:  #TaskTypeID ==1 for Text Type 
					myList = [SrNo,TaskID,TaskName,TaskDescription,Action,TaskTypeID,TaskRemarkId,OkSelected]	
					dataList.append(myList)
					j = j+1

			headers =  ["SrNo","TaskID","TaskName","TaskDescription","Action","TaskTypeID","TaskRemarkId","OkSelectedTxt"]
			resultDetails = system.dataset.toDataSet(headers,dataList)
			return resultDetails
		else:
			for i in resultData:	
				SrNo = j
				TaskID =  i.get("id")
				TaskName = i.get("name")
				TaskDescription = i.get("TaskDescription")
				Action = i.get("TaskRemark")  #NOk Field
				OkSelected = i.get("OkSelected") #OK Field
				TaskTypeID = i.get("type")
				TaskRemarkId = i.get("TaskRemarkId")

				system.perspective.print('Action  Nok Columns: ' + str(Action))
				system.perspective.print('OkSelected        : ' + str(OkSelected))
	
				if str(OkSelected).lower().strip()=='true' or str(OkSelected)=='True' or str(OkSelected)=='1':
					OkSelected=True
#					Action = False
				else:
					OkSelected=False
#					Action = True


				if str(Action).lower().strip()=='true' or str(Action)=='True' or str(Action)=='1':
					Action=True
#					Action = False
				else:
					Action=False
#					Action = True

				if TaskTypeID == 2: # TaskTypeID ==2 for Bool Type 
					myList = [SrNo,TaskID,TaskName,TaskDescription,Action,TaskTypeID,TaskRemarkId,OkSelected]
					print "myList",myList	
					dataList.append(myList)
					j = j+1
			headers =  ["SrNo","TaskID","TaskName","TaskDescription","Action","TaskTypeID","TaskRemarkId","OkSelected"]
			resultDetails1 = system.dataset.toDataSet(headers,dataList)
			return resultDetails1	
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print('GetTasksListbyType errorMessage :' + str(errorMessage))

#-------------------- END Get Task List By TaskTypeID ----------------------------------------------------------------

#--------------------Get Task Attachments By TaskID ----------------------------------------------------------------

def GetTaskAttachments(TaskID):
	try:
		scriptName="API:Get Tasks Attachment by TaskId"
		apiPath ="MaintenanceOperatorConsole/GetPMTasksAttachmentsForOperatorConsoleWorkOrder?taskId=" + str(TaskID)
		url = URLPath + apiPath		
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		dataList = []
		j = 1 
		for i in resultData:	
			SrNo = j
			FileName =  i.get("fileName")
			FilePath = i.get("filePath")
			FilePathID = i.get("id")
			viewAttachment = ""
			myList = [SrNo,FileName,FilePath,FilePathID,viewAttachment]	
			dataList.append(myList)
			j = j+1
			
		headers =  ["SrNo","FileName","FilePath","FilePathID","viewAttachment"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)	

#--------------------END Get Task Attachments By TaskID ----------------------------------------------------------------

#--------------------Update Tasks --------------------------------------------------------------------------

def updateTaskDetails(MaintenanceWorkflowID,UserID,TaskRemarkID,TaskID,Remarks,PMOrderID,okSelected):
	try:
		scriptName = "API: Update Task List"
		apiPath = "MaintenanceOperatorConsole/AddUpdateTaskCommentFromPMOperatoConsole"
		url = URLPath + apiPath		
		writeData = {
		  "isActive": True,
		  "createdBy": int(UserID),
		  "taskRemarkId": int(TaskRemarkID),
		  "taskId": int(TaskID),
		  "maintenanceWorkFlowID": int(MaintenanceWorkflowID),
		  "remarks": str(Remarks),
		  "pmOrderId": int(PMOrderID),
		  "okSelected" : str(okSelected)

		}
		jsonParams = system.util.jsonEncode(writeData)		
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
			print("PostReturn",postReturn)
		except:		
			result = 0
			pass
	except:	
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)


#ADD PM NOTES

def AddPMNotes(comment,PMOrderID,shiftId,userId):
	scriptName="API:PostPMNotes"
	apiPath = "MaintenanceOperatorConsole/AddPMNotes"
	url = URLPath + apiPath		
	writeData = {
		  "isActive": True,
		  "createdBy": userId,
		  "pmNotes": comment,
		  "pmOrderId": int(PMOrderID),
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
	
def getPMNotes(PMOrderID):
	scriptName="API:Get PM Notes by RMOrderID"
	apiPath ="MaintenanceOperatorConsole/GetPMNotesTechnicianConsole/"+str(PMOrderID)
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
		PMNotes =  i.get("PMNotes")
		CreatedOn = i.get("CreatedOn")
		system.perspective.print('CreatedOn : ' + str(CreatedOn))
		ShiftId = i.get("ShiftId")
		myList = [SrNo,PMNotes,CreatedOn,ShiftId]	
		dataList.append(myList)
		j = j+1
		
	headers =  ["Sr No","PMNotes","CreatedOn","ShiftId"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	print "resultDetails",resultDetails
	return resultDetails
	

def assignCoOperator(PMOrderID,assignedUserId,userId,statusId):
	scriptName="API:CoorperatorAssign"
	apiPath = "MaintenanceOperatorConsole/AssignMaintenanceCooperator"
	url = URLPath + apiPath		
	writeData = {
				  "workOrderId": int(PMOrderID),
				  "assignedTo": int(assignedUserId),
				  "assignedBy": int(userId),
				  "maintenanceTypeId": 1, #For Preventive Maintenance
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
	
def getAssignedOperators(PMOrderId,userId):
	maintenanceTypeId = 1 #Preventive Maintenance Type
	apiPath = "MaintenanceOperatorConsole/GetMaintennaceAssignedOperator?woOrderId="+str(PMOrderId)+"&maintenanceTypeId="+str(maintenanceTypeId)+"&userId="+str(userId)
	url = URLPath + apiPath		
#	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	print "data ,",data
	if data.good:    
		resultData=data.json	
	dataList = []
	j = 1 
	for i in resultData:
		SrNo = j
		AssignedName =  i.get("AssignedName")
		AssignedOn = i.get("AssignedOn")
		UserId = i.get("UserId")

		system.perspective.print('AssignedOn :' + str(AssignedOn))
		myList = [SrNo,AssignedName,AssignedOn,UserId]
		dataList.append(myList)
		j = j+1
		
	headers =  ["Sr No","Co-OperatorName","AssignedOn","UserId"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	print "resultDetails",resultDetails
	return resultDetails
	
def getSparePartsbymachineToolId(MachineID,pmTypeId,WarehouseId,WoNumber):
	try: 
		scriptName="API:getSparePartsByMachineID"
		apiPath = 'MaintenanceOperatorConsole/GetSparepartByTool/'+str(MachineID)+'/'+str(pmTypeId)+'/'+str(WarehouseId)+'/'+str(WoNumber)
		
		
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
		print "resultData",resultData
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
			print "myList",myList
			dataList.append(myList)
			j=j+1
			
		headers =  ["SrNo","sparePartName","onHandQty","RequestedQty","sparePartID","ImagePath","TotalRequestedQty"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		print "resultDetails",resultDetails
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
	
	
def GetIsOperatorActive(userId,orderId,maintenanceTypeId):
	apiPath = "MaintenanceOperatorConsole/IsOperatorActive/"+str(userId)+"/"+str(orderId)+"/"+str(maintenanceTypeId)
	url = URLPath + apiPath		
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData=data.json
	print "resultData",resultData
	myList = []
	for i in resultData:
		result = i.get('result')
		Name = i.get('openedBy')
		myList = [result,Name]
		break
	return myList
	

def ReleaseOperatorActiveScreen(userId,orderId,maintenanceTypeId):
	apiPath = "MaintenanceOperatorConsole/ReleaseOperatorActiveScreen/"+str(userId)+"/"+str(orderId)+"/"+str(maintenanceTypeId)
	url = URLPath + apiPath		
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData=data.json
	return resultData
	
	
def GetSkilledUserByMaintenanceType(maintenanceTypeId,PMOrderId,userId):
   	AssigendData=MaintenanceOCAPI.getAssignedOperators(PMOrderId,userId)
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