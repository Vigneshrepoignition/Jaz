import smtplib	
import system
import re
import json
import urllib2, urllib

URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value

def GetCLRIWorkflowByMachine(machineId,UserId):
	try: 
		scriptName="API:GetCLRIWorkflowByMachine"
#		machineId='15'
#		system.perspective.print("machineId "+str(machineId))
#		system.perspective.print("UserId "+str(UserId))
		if machineId==None or str(machineId).strip()=='' or str(machineId).strip().lower()=='none':
			machineId=0
		if UserId==None or str(UserId).strip()=='' or str(UserId).strip().lower()=='none':
			UserId=0
		apiPath = "CLRIWorkFlow/GetCLRIWorkflowByMachine/"+str(machineId)+"/"+str(UserId)+"/"+str('0')
		url = URLPath + apiPath
		system.perspective.print("url "+str(url))
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData=data.json
		SrNo=0
		dataList = []

		for i in resultData:			
			
			SrNo=SrNo+1	
			id = i.get("id")
			name = i.get("name")
			
			makeName = i.get("makeName")
			modelName = i.get("modelName")
			sbcNumber = i.get("sbcNumber")
			revision = i.get("revision")
			comment = i.get("comment")
			LastModifiedBy = i.get("modifiedBy")
			LastModifiedOn = i.get("modifiedOn")
			makeId = i.get("makeId")
			View = ""
			modelId = i.get("modelId")
			isassign = i.get("IsAssign")
			Status = i.get("Status")
			StatusId = i.get("StatusId")
			MachineName = i.get("MachineName")
			MachineId = i.get("MachineId")
			AssignUserId = i.get("AssignUserId")
			EnterpriseId = i.get("EnterpriseId")
			EnterpriseName = i.get("EnterpriseName")
			PlantId = i.get("PlantId")
			PlantName = i.get("PlantName")
			AreaId = i.get("AreaId")
			AreaName = i.get("AreaName")
			LineId = i.get("LineId")
			LineName = i.get("LineName")
			IsCompleted = i.get("IsCompleted")
			if IsCompleted==1 or str(IsCompleted)=='1':
				IsCompleted='Yes'
			else:
				IsCompleted='No'
			
			
			if str(LastModifiedOn).strip()==None or str(LastModifiedOn).strip()=='None' or  str(LastModifiedOn).strip()=='' or str(LastModifiedOn).lower().strip()=='null':
				LastModifiedOn=''		
			if str(LastModifiedBy).strip()==None or  str(LastModifiedBy).strip()=='None' or str(LastModifiedBy).strip()=='' or str(LastModifiedBy).lower().strip()=='null':
				LastModifiedBy=''	
			
			myList = [SrNo,id, name, sbcNumber,revision,MachineName,Status,makeName,modelName,comment,isassign,"","",modelId,MachineId,makeId,StatusId,AssignUserId,EnterpriseId,EnterpriseName,PlantId,PlantName,AreaId,AreaName,LineId,LineName,LastModifiedOn,LastModifiedBy,IsCompleted]
			dataList.append(myList)
			
		headers = ["SrNo","ID", "Name", "SBCNumber", "Rivision","Machine","Status","Make", "Model", "Comment","Assign","View_Details","History","modelId","MachineId","makeId","StatusId","AssignUserId","EnterpriseId","EnterpriseName","PlantId","PlantName","AreaId","AreaName","LineId","LineName","LastModifiedOn","LastModifiedBy","IsCompleted"]	
		resultDetails = system.dataset.toDataSet(headers,dataList)
		resultDetails = system.dataset.toPyDataSet(resultDetails)
		
		return resultDetails
	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)	
		system.perspective.print("errorMessage "+str(errorMessage))
		print errorMessage
		return None

def GetCLRIWorkflowByLine(machineId,lineID,UserId):
	try: 
		scriptName="API:GetCLRIWorkflowByMachine"
		if machineId==None or str(machineId).strip()=='' or str(machineId).strip().lower()=='none':
			machineId=0
		if UserId==None or str(UserId).strip()=='' or str(UserId).strip().lower()=='none':
			UserId=0
		apiPath = "CLRIWorkFlow/GetCLRIWorkflowByMachine/"+str(machineId)+"/"+str(UserId)+"/"+str(lineID)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData=data.json
		SrNo=0
		dataList = []

		for i in resultData:			
			
			SrNo=SrNo+1	
			id = i.get("id")
			name = i.get("name")
			
			makeName = i.get("makeName")
			modelName = i.get("modelName")
			sbcNumber = i.get("sbcNumber")
			revision = i.get("revision")
			comment = i.get("comment")
			LastModifiedBy = i.get("modifiedBy")
			LastModifiedOn = i.get("modifiedOn")
			makeId = i.get("makeId")
			View = ""
			modelId = i.get("modelId")
			isassign = i.get("IsAssign")
			Status = i.get("Status")
			StatusId = i.get("StatusId")
			MachineName = i.get("MachineName")
			MachineId = i.get("MachineId")
			AssignUserId = i.get("AssignUserId")
			EnterpriseId = i.get("EnterpriseId")
			EnterpriseName = i.get("EnterpriseName")
			PlantId = i.get("PlantId")
			PlantName = i.get("PlantName")
			AreaId = i.get("AreaId")
			AreaName = i.get("AreaName")
			LineId = i.get("LineId")
			LineName = i.get("LineName")
			IsCompleted = i.get("IsCompleted")
			if IsCompleted==1 or str(IsCompleted)=='1':
				IsCompleted='Yes'
			else:
				IsCompleted='No'
			
			
			if str(LastModifiedOn).strip()==None or str(LastModifiedOn).strip()=='None' or  str(LastModifiedOn).strip()=='' or str(LastModifiedOn).lower().strip()=='null':
				LastModifiedOn=''		
			if str(LastModifiedBy).strip()==None or  str(LastModifiedBy).strip()=='None' or str(LastModifiedBy).strip()=='' or str(LastModifiedBy).lower().strip()=='null':
				LastModifiedBy=''	
			
			myList = [SrNo,id, name, sbcNumber,revision,MachineName,Status,makeName,modelName,comment,isassign,"","",modelId,MachineId,makeId,StatusId,AssignUserId,EnterpriseId,EnterpriseName,PlantId,PlantName,AreaId,AreaName,LineId,LineName,LastModifiedOn,LastModifiedBy,IsCompleted]
			dataList.append(myList)
			
		headers = ["SrNo","ID", "Name", "SBCNumber", "Rivision","Machine","Status","Make", "Model", "Comment","Assign","View_Details","History","modelId","MachineId","makeId","StatusId","AssignUserId","EnterpriseId","EnterpriseName","PlantId","PlantName","AreaId","AreaName","LineId","LineName","LastModifiedOn","LastModifiedBy","IsCompleted"]	
		resultDetails = system.dataset.toDataSet(headers,dataList)
		resultDetails = system.dataset.toPyDataSet(resultDetails)

		
		return resultDetails
	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)	
		print errorMessage
		return None		
		
def OperationStatusConformation(CLRIId,StatusId,MachineId,UserId,ReasonCategoryId,ReasonCodeId,ReasonCodeComments):
	try:
		if ReasonCodeComments==None or str(ReasonCodeComments).strip()=='' or str(ReasonCodeComments).strip().lower()=='none':
				ReasonCodeComments=''
		scriptName="API:CLIR OperationStatusConformation"
		apiPath = "CLRIWorkFlow/OperationStatusConformation"
		apiPath = "CLRIWorkFlow/OperationStatusConformation"
		url = URLPath + apiPath	

		writeData = {
				"CLRIId": int(CLRIId),
				"StatusId": StatusId,
				"MachineId": int(MachineId),
				"UserId": int(UserId),
				"ReasonCategoryId": int(ReasonCategoryId),
				"ReasonCodeId": int(ReasonCodeId),
				"ReasonCodeComments": ReasonCodeComments
			}
		jsonParams = system.util.jsonEncode(writeData)		

		system.perspective.print('jsonParams : ' + str(jsonParams))
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
			print("PostReturn",postReturn)
		except:		
			result = 0
			pass
		print "result",result
		return result
	
	
	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)	
#		system.perspective.print(errorMessage)
		print errorMessage
		return None
		
def AddCLRINotes(clriNotes,clriId,userId,MachineId):
	scriptName="API:PostAddCLRINotes"
	apiPath = "CLRIWorkFlow/AddCLRINotes"
	url = URLPath + apiPath	
	writeData = {
		  "isActive": True,
		  "userId": userId,
		  "clriNotes": clriNotes,
		  "clriId": int(clriId),
		  "machineId": int(MachineId)
		  
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
	
def getCLRINotes(CLRIID,MachineId):
	scriptName="API:Get CLRI Notes by CLRIID"
	apiPath ="CLRIWorkFlow/GetAddCLRINotes/"+str(CLRIID)+"/"+str(MachineId)
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
		CLRINotes =  i.get("CLRINotes")
		CreatedOn = i.get("CreatedOn")
		myList = [SrNo,CLRINotes,CreatedOn]	
		dataList.append(myList)
		j = j+1
		
	headers =  ["Sr No","CLRINotes","CreatedOn"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	print "resultDetails",resultDetails
	return resultDetails	

		
def GetActionForCLRIWorkflow(CLRIID):
	scriptName="API:Get CLRI Notes by CLRIID"
	apiPath ="CLRIWorkFlow/GetActionForCLRIWorkflow/"+str(CLRIID)
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
		id =  int(i.get("id"))
		taskName = (i.get("taskName"))
		taskType = (i.get("taskType"))
		taskDescription = (i.get("taskDescription"))
		taskComment = (i.get("taskComment"))
		AttachmentsName = (i.get("AttachmentsName"))
		AttachmentsPath = (i.get("AttachmentsPath"))
		AttachmentsId = i.get("AttachmentsId")
		taskQty = i.get("taskQty")
#		IsCompleted = i.get("IsCompleted")
		IsCompleted = int(i.get("IsCompleted"))
		FrequencyName = (i.get("FrequencyName"))
		visualAction = i.get("visualAction")
		physicalAction = i.get("physicalAction")
		IsEnabled = i.get("isEnabled")

		if IsEnabled==True or str(IsEnabled).lower()=='true' or str(IsEnabled)==str('1') :
			myList = [SrNo,id,taskName,taskType,taskDescription,taskComment,"",AttachmentsName,AttachmentsPath,AttachmentsId,taskQty,IsCompleted,FrequencyName,[visualAction,physicalAction],'',visualAction,physicalAction]	
			dataList.append(myList)
			j = j+1
		
	headers =  ["SrNo","id","taskName","taskType","taskDescription","taskComment","Attachments","AttachmentsName","AttachmentsPath","AttachmentsId","taskQty","IsCompleted","FrequencyName","visualActionAndphysicalAction","Action","visualAction","physicalAction"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	resultDetails = system.dataset.toPyDataSet(resultDetails)
	return resultDetails	
	
def UpdateActionForCLRIWorkflowOperatorConsole(actionID,isCompleted,visualAction,physicalAction,userId):
	try:
		scriptName="API:Post UpdateActionForCLRIWorkflowOperatorConsole"
		apiPath = "CLRIWorkFlow/UpdateActionForCLRIWorkflowOperatorConsole"
		url = URLPath + apiPath	
		writeData = {
			  "actionID": actionID,
			  "isCompleted": isCompleted,
			  "visualAction": visualAction,
			  "physicalAction": int(physicalAction),
			  "userId": int(userId)
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
	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)	
		system.perspective.print(errorMessage)
		print errorMessage
		return 0
		
#def GetCLRIWorkflowHistory(CLRIID,UserID):
#	scriptName="API:Get CLRI GetCLRIWorkflowHistory by CLRIID"
#	apiPath ="CLRIWorkFlow/GetCLRIWorkflowHistory/"+str(CLRIID)+"/"+str(UserID)
#	url = URLPath + apiPath		
#	resultData=None
#	client = system.net.httpClient()
#	data = client.get(url)
#	if data.good:    
#		resultData=data.json
#	print "resultData",resultData
#	dataList = []
#	j = 1 
#	for i in resultData:	
#		SrNo = j
#		Name =  i.get("Name")
#		SBCNumber =  i.get("SBCNumber")
#		Status =  i.get("Status")
#		comment =  i.get("comment")
#		LoginId =  i.get("LoginId")
#		CreatedOn = i.get("CreatedOn")
#		myList = [SrNo,Name,SBCNumber,Status,comment,LoginId,CreatedOn]	
#		dataList.append(myList)
#		j = j+1
#		
#	headers =  ["Sr No","Name","SBCNumber","History","Comments","CreatedBy","CreatedOn"]
#	resultDetails = system.dataset.toDataSet(headers,dataList)
#	print "resultDetails",resultDetails
#	return resultDetails			

def GetCLRIWorkflowHistory(CLRIID,UserID,MachineID):
	try: 
		scriptName="API:Get CLRI GetCLRIWorkflowHistory by CLRIID"
		system.perspective.print("CLRIID "+str(CLRIID))
		system.perspective.print("UserID "+str(UserID))
		apiPath ="CLRIWorkFlow/GetCLRIWorkflowHistory/"+str(CLRIID)+"/"+str(UserID)+"/"+str(MachineID)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData=data.json
		print "resultData",resultData
		SrNo=0
		dataList = []

		for i in resultData:			
			
			SrNo=SrNo+1	
			id = i.get("id")
			name = i.get("name")
			
			makeName = i.get("makeName")
			modelName = i.get("modelName")
			sbcNumber = i.get("sbcNumber")
			revision = i.get("revision")
			comment = i.get("comment")
			LastModifiedBy = i.get("modifiedBy")
			LastModifiedOn = i.get("modifiedOn")
			makeId = i.get("makeId")
			View = ""
			modelId = i.get("modelId")
			isassign = i.get("IsAssign")
			Status = i.get("Status")
			StatusId = i.get("StatusId")
			MachineName = i.get("MachineName")
			MachineId = i.get("MachineId")
			StartDate = i.get("StartDate")
			EndDate = i.get("EndDate")
			LoginId = i.get("LoginId")


			if str(LastModifiedOn).strip()==None or str(LastModifiedOn).strip()=='None' or  str(LastModifiedOn).strip()=='' or str(LastModifiedOn).lower().strip()=='null':
				LastModifiedOn=''		
			if str(LastModifiedBy).strip()==None or  str(LastModifiedBy).strip()=='None' or str(LastModifiedBy).strip()=='' or str(LastModifiedBy).lower().strip()=='null':
				LastModifiedBy=''	
			
			myList = [SrNo,id, name, sbcNumber,revision,MachineName,Status,makeName,modelName,comment,isassign,"","",modelId,MachineId,makeId,StatusId,StartDate,EndDate,LoginId,LastModifiedBy,LastModifiedOn]
			dataList.append(myList)
			
		headers = ["SrNo","ID", "Name", "SBCNumber", "Rivision","Machine","Status","Make", "Model", "Comment","Assign","View_Details","History","modelId","MachineId","makeId","StatusId","StartDate","EndDate","LoginId","LastModifiedBy","LastModifiedOn"]	
		resultDetails = system.dataset.toDataSet(headers,dataList)
		resultDetails = system.dataset.toPyDataSet(resultDetails)	
		return resultDetails
	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)	
		print errorMessage
		return None											