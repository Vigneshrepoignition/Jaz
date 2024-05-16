import re
import json
import urllib2, urllib
import datetime
#URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
URLPath = "http://10.5.176.164/jemesvnext/JemesFMWebApi/api/"
defaultPath=system.tag.read("[default]JMES_InternalTags/DafaultTagPath").value

#-------------------------Component Details Against WO--------------------------------------
def GetMachineDetails(userId,WONO):	
 	apiPath = "OperatorConsole/GetOperatorConsoleWorkOrdersonInput?EnterpriseId="+str(0)+"&PlantId="+str(0)+"&AreaId="+str(0)+"&LineId="+str(0)+"&MachineId="+str(0)+"&UserId="+str(userId)	
	url = URLPath + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
#		system.perspective.print("API InputData is: "+str(jsonParams))
		system.perspective.print("API Method is: Get ")
	except:
		pass
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	print resultData
	dataList = []
	SrNo=0
	for i in resultData:					
		WoNumber = i.get("WorkOrderNo")
		if WONO==WoNumber:			
			machineName= i.get("MachineName")
			machineID= i.get("MachineId")
			Status = i.get("Status")                    				
			Operation = i.get("Operations")
			Workflow = i.get("WorkflowName")
			defaultPath=system.tag.read("[default]JMES_InternalTags/DafaultTagPath").value
			TagPathMachineStatus = defaultPath + str(machineName)+"/MachineStatus"
			MachineStatus = system.tag.read(TagPathMachineStatus).value
			TagPathMachineGoodQty = defaultPath + str(machineName)+"/GoodQty"
			MachineGoodQty = system.tag.read(TagPathMachineGoodQty).value
			TagPathMachineNotGoodQty = defaultPath + str(machineName)+"/NGQty"
			MachineNotGoodQty = system.tag.read(TagPathMachineNotGoodQty).value
			SrNo=SrNo+1
			myList=[SrNo,machineName,Operation,Status,MachineGoodQty,MachineNotGoodQty,machineID]			
			dataList.append(myList)
#			print dataList
		else:
			pass
#			print('No Data Found for selected WO :'+ str(WONO))
	header=	('Sr No','Equipment Code','Operation','Equipment Status','Good Qty','Bad Qty','machineID')
	print dataList
	resultDetails = system.dataset.toDataSet(header,dataList)
	return resultDetails
	
#---------------------------------------------Get List Of Operations--------------------------------------------
def getOperationsForWo(userId,WONO):	
 	apiPath = "OperatorConsole/GetOperatorConsoleWorkOrdersonInput?EnterpriseId="+str(0)+"&PlantId="+str(0)+"&AreaId="+str(0)+"&LineId="+str(0)+"&MachineId="+str(0)+"&UserId="+str(userId)	
	url = URLPath + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
#		system.perspective.print("API InputData is: "+str(jsonParams))
		system.perspective.print("API Method is: Get ")
	except:
		pass
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
#	print"ResultData",(resultData)
	dataList = []
	j=1
	oprList = []
	for i in resultData:			
		WoNumber = i.get("WorkOrderNo")		
		if WoNumber == WONO:	
			Operation = i.get("Operations")
			WorkflowId = i.get("WorkflowId")					
			myList = [Operation] 
			if Operation not in 	oprList:	
				dataList.append(myList)	
				oprList.append(Operation)
			else:
				continue
	print 'dataList',dataList
	headers = ["Operation"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails
	




def getWorkflowOperationId(userId,WONO):	
 	apiPath = "OperatorConsole/GetOperatorConsoleWorkOrdersonInput?EnterpriseId="+str(0)+"&PlantId="+str(0)+"&AreaId="+str(0)+"&LineId="+str(0)+"&MachineId="+str(0)+"&UserId="+str(userId)	
	url = URLPath + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
#		system.perspective.print("API InputData is: "+str(jsonParams))
		system.perspective.print("API Method is: Get ")
	except:
		pass
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	print"ResultData",(resultData)
	dataList = []
	j=1
	oprList = []
	for i in resultData:			
		WoNumber = i.get("WorkOrderNo")		
		if WoNumber == WONO:	
			Operation = i.get("Operations")
			WorkflowOperationsId = i.get("WorkflowOperationsId")		
			WorkflowId = i.get("WorkflowId")					
			myList = [WorkflowOperationsId,Operation] 
			if Operation not in oprList:	
				dataList.append(myList)	
				oprList.append(Operation)
			else:
				continue
	print dataList 
	headers = ["WorkflowOperationsId","Operation"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails

# Get Reactive Maintenance Priorities 
def getRMpriorities():	
 	apiPath = "MaintenanceLeadConsole/GetRMOrderPriorityStatus"
	url = URLPath + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
#		system.perspective.print("API InputData is: "+str(jsonParams))
		system.perspective.print("API Method is: Get ")
	except:
		pass
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	print"ResultData",(resultData)
	dataList = []
	for i in resultData:			
		priorityId = i.get("id")
		print "priorityId"
		priorityName = i.get("name")				
		myList = [priorityId,priorityName] 
		dataList.append(myList)	

	headers = ["Priority Id", "Priority Name"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails			


def getWoNumbersByLine(userId,selectedLine):
	apiPath = "OperatorConsole/GetOperatorConsoleWorkordersPDA?UserId="+str(userId)+"&LineId="+str(selectedLine)  
	url = URLPath + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
#		system.perspective.print("API InputData is: "+str(jsonParams))
		system.perspective.print("API Method is: Get ")
	except:
		pass
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	print"ResultData",(resultData)
	dataList=[]
	for i in resultData:
		workOrderId = i.get("ID")
		woNumber = i.get("WorkOrderNo")
		myList = [workOrderId,woNumber]
		myList = [woNumber]  		
		dataList.append(myList)
	headers = ["WorkOrderId","WoNumber"]
	headers = ["WoNumber"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails
			
def getOperationsbyuserID(userId,WONO):
	apiPath = "OperatorConsole/GetOperatorConsoleWorkOrdersonInput?EnterpriseId="+str(0)+"&PlantId="+str(0)+"&AreaId="+str(0)+"&LineId="+str(0)+"&MachineId="+str(0)+"&UserId="+str(userId)	
	url = URLPath + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
#		system.perspective.print("API InputData is: "+str(jsonParams))
		system.perspective.print("API Method is: Get ")
	except:
		pass
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	dataList = []
	oprList = []
	for i in resultData:			
		WoNumber = i.get("WorkOrderNo")		
		if WoNumber == WONO:	
			Operation = i.get("Operations")
			WorkflowOperationsId = i.get("WorkflowOperationsId")
					
			myList = [WorkflowOperationsId,Operation] 
			print myList
			if Operation not in 	oprList:	
				dataList.append(myList)	
				oprList.append(Operation)
			else:
				continue
	headers = ["WorkflowOperationsId","Operation"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return 	resultDetails
	
def getOperationsForChecklist(WorkorderId,userId):
	try:
	 	apiPath = ("OperatorConsole/GetWorkflowOperationsByWorkOrder?WorkorderId=")+str(WorkorderId)+("&UserId=")+str(userId)	
		url = URLPath + apiPath
		try:
			system.perspective.print("API URL is: "+str(url))
	#		system.perspective.print("API InputData is: "+str(jsonParams))
			system.perspective.print("API Method is: Get ")
		except:
			pass
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)

		if data.good:    
		  resultData=data.json
	#	print"ResultData",(resultData)
		dataList = []
		j=1
		oprList = []
		for i in resultData:			
				Operation = i.get("Operations")
				OperationId = i.get("operationID")					
				myList = [OperationId,Operation] 
				if Operation not in 	oprList:	
					dataList.append(myList)	
					oprList.append(Operation)
				else:
					continue
		print 'dataList',dataList
		headers = ["OperationId","Operation"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:
		print"Exception: "+str(data)
		return 0
		
	
	
def getEquipments(userId,operationId,WoNumber):
	apiPath = "OperatorConsole/GetOperatorConsoleWorkOrdersonInput?EnterpriseId="+str(0)+"&PlantId="+str(0)+"&AreaId="+str(0)+"&LineId="+str(0)+"&MachineId="+str(0)+"&UserId="+str(userId)	
	url = URLPath + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
#		system.perspective.print("API InputData is: "+str(jsonParams))
		system.perspective.print("API Method is: Get ")
	except:
		pass
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	print "resultData",resultData
	dataList = []
	for i in resultData:			
		WorkOrderNo = i.get('WorkOrderNo')
		if WorkOrderNo == str(WoNumber):
			WorkflowOperationsId =int(i.get("WorkflowOperationsId"))
			if WorkflowOperationsId == operationId:	
				MachineId = i.get("MachineId")
				MachineName = i.get("MachineName")
				myList = [MachineId,MachineName] 
				dataList.append(myList)	
	
	headers = ["MachineId","MachineName"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails


def getMachineNamebyMachineId(userId,machineId):	
	apiPath = "OperatorConsole/GetOperatorConsoleWorkOrdersonInput?EnterpriseId="+str(0)+"&PlantId="+str(0)+"&AreaId="+str(0)+"&LineId="+str(0)+"&MachineId="+str(0)+"&UserId="+str(userId)	
	url = URLPath + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
#		system.perspective.print("API InputData is: "+str(jsonParams))
		system.perspective.print("API Method is: Get ")
	except:
		pass
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	print "resultData",resultData
	
	for i in resultData:
		MachineID = int(i.get('MachineId'))
		if MachineID == machineId:
			machineName = i.get('MachineName')
			break
	return machineName
	
def getReasonsCodes(mainReasonTypeId,subReasonTypeId,userId):
	#system.perspective.print("getReasonsCodes   mainReasonTypeId"+str(mainReasonTypeId))
	#system.perspective.print("subReasonTypeId   subReasonTypeId"+str(subReasonTypeId))
	
	apiPath = "OperatorConsole/GetReasonCodeByInput?ReasontypeId="+str(mainReasonTypeId)+"&ReasaonsubtypeId="+str(subReasonTypeId)+"&UserId="+str(userId)
	
	url = URLPath + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
#		system.perspective.print("API InputData is: "+str(jsonParams))
		system.perspective.print("API Method is: Get ")
		pass
	except:
		pass
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	
	dataList = []
	for i in resultData:	
		reasonCodeId = i.get("Id")
		reasonCodeName = i.get("Name")
		myList = [reasonCodeId,reasonCodeName] 		
		dataList.append(myList)	
		
	headers = ["ReasonCodeId","ReasonCodeName"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails
	
def getMakeModelbyMachineId(machineId):
	apiPath = "ProductionOperatorConsole/GetMakeModelByMachineId/"+str(machineId).strip()
	url = URLPath + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
#		system.perspective.print("API InputData is: "+str(jsonParams))
		system.perspective.print("API Method is: Get ")
	except:
		pass
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	return resultData

		


def createRMorder(machineId,makeId,modelId,reasonTypeId,reasonSubtypeId,reasoncodeId,priorityId,userId,remarks,RMType):
	apiPath = "MaintenanceLeadConsole/CreateManualOrder"
	url = URLPath + apiPath
	
	writeData = {
	  "id": 0,
	  "alert": "0",
	  "workOrderNo": "",
	  "line": 0,
	  "assignTo": 0,
	  "userRemark": remarks,
	  "createdBy": userId,
	  "modifiedBy": 0,
	  "isActive": True,
	  "priorityId": priorityId,
	  "machineId": machineId,
	  "reasonCodeId": reasoncodeId,
	  "make": makeId,
	  "model": modelId,
	  "reasonTypeId": 0,
	  "reasonTypeName": "",
	  "reasonSubType": reasonSubtypeId,
	  "imgPathBefore": "",
	  "imgPathAfter": "",
      "maintenanceType": RMType    #------RMType= 1 for machine 2 for Tool
	}
	
	
	jsonParams = system.util.jsonEncode(writeData)
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API InputData is: "+str(jsonParams))
		system.perspective.print("API Method is: Post ")
	except:
		pass	
	createRMStatus = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
	except:		
		createRMStatus = 0
		pass
	return createRMStatus

#------------------------------List of WorkOrder for Main Landing Page In Production Operator Console----------------
#---------------------------------------------------------------------------------------------------------------------

def getUserAssignedWOList(entId,plantId,areaId,lineId,userId):	
#	apiPath='ProductionOperatorConsole/GetProductionUserAssignList/'+str(entId)+'/'+str(plantId)+'/'+str(areaId)+'/'+str(lineId)+'/'+str(userId)+'/'+str(woNo)
	apiPath='OperatorConsole/GetOperatorConsoleWorkOrdersDetails?EnterpriseId='+str(entId)+'&PlantId='+str(plantId) + '&AreaId='+str(areaId)+'&LineId='+str(lineId)+'&MachineId='+str(0)+'&UserId='+str(userId)
	url = URLPath + apiPath
	system.perspective.print("API URL is: "+str(url))
	try:
		pass
		#system.perspective.print("API URL is: "+str(url))
#		system.perspective.print("API InputData is: "+str(jsonParams))
		#system.perspective.print("API Method is: Get ")
	except:
		pass
	print url
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  APIResult=data.json
#	  APIResult=[{'WONo':'12976156','WOQty':432,'PartNo':'1339-10E0023','Revision':'A','WOCompletion':0,'WoStatus':'Not-Started','WorkFlow':'P_AA_2022-1020456EP_B_CNS','WorkFlowId':97,'WorkFlowOperation':'Molding','WorkFlowOperationId':97,'StartDate':'2021-03-27T23:22:00','EndDate':'2021-03-29T23:22:00','ActualStartDate':'2021-03-27T23:22:00','ActualEndDate':'2021-03-29T23:22:00','UOM':'EA','EntName':'JohnsonElectric','EntID':0,'PlantName':'Jiangmen','PlantId':0,'AreaName':'CNS','AreaId':6,'LineName':'AA','LineId':8,'CycleTime':2,'shift':'Shift-A'}]
	print"ResultData",(APIResult)	
	WODetailList=[]
	Id=0
	for i in (APIResult):
		Id=Id+1
		WONo=i.get('WONo')
		WorkorderID=i.get('WorkOrderId')
		
		WOQty=i.get('WOQty')
		WorkFlow=i.get('WorkFlow')
		WorkFlowId=i.get('WorkFlowId')
		WorkFlowOperation=i.get('WorkFlowOperation')
		WorkFlowOperationId=i.get('WorkFlowOperationId')
		StartDate=i.get('StartDate')
#		StartDate=system.date.format(StartDate1,"DD/MM/YYYY hh:mm:ss")
		EndDate=i.get('EndDate')
		ActualStartDate=i.get('ActualStartDate')
		ActualEndDate=i.get('ActualEndDate')
		if str(ActualStartDate) == str("null") or ActualStartDate == None: 
			ActualStartDate = ''
		ActualEndDate=i.get('ActualEndDate')
		if str(ActualEndDate) == str("null") or ActualEndDate == None: 
			ActualEndDate = ''
		WoStatus=i.get('WoStatus')
		WOCompletion=i.get('WOCompletion')
		PartNo=i.get('PartNo')
		Revision=i.get('Revision')
		UOM=i.get('UOM')
		EntName=i.get('EnterpriseName')
		EntID=i.get('EnterpriseId')
		PlantName=i.get('PlantName')
		PlantId=i.get('PlantId')
		AreaName=i.get('AreaName')
		AreaId=i.get('AreaId')
		LineName=i.get('LineName')
		LineId=i.get('LineId')
		#system.perspective.print(LineId)
		a = fpsi_ignition01.identify_auto_or_manual(lineid=LineId)
		system.perspective.print(a)
		LineType = a
		CycleTime=i.get('Cycletime')
		Factory=i.get('Factory')
		shiftId=i.get('ShiftId')
		shift=i.get('Shift')
		#stdHC=i.get('Manpower')
		stdHC = 0 
		#print(stdHC)
		stdHC = float(stdHC)
		actHC=i.get('ActualHeadCount')
		actHC = float(actHC)
		salesOrder=i.get('SalesOrder')		
#		shift='Shift A'
		WOType=i.get('WorkOrderType')
		#WOType = 2
		ShiftCapacity=i.get('ShiftCapacity')
		ViewDetails=''
		Assembytype = 'A'
		DataList=[Id,WONo,WOQty,PartNo,Revision,WOCompletion,WoStatus,WorkFlow,WorkFlowId,WorkFlowOperation,WorkFlowOperationId,StartDate,EndDate,ActualStartDate,ActualEndDate,UOM,EntName,EntID,PlantName,PlantId,AreaName,AreaId,LineName,LineId,CycleTime,shift,ViewDetails,Factory,stdHC,actHC,salesOrder,shiftId,WOType,ShiftCapacity,WorkorderID,Assembytype,LineType]
		WODetailList.append(DataList)
	print 'API Result:-->' +str(WODetailList)
	header=['Sr No','WONo','WOQty','PartNo','Revision','WOCompletion','WoStatus','WorkFlow','WorkFlowId','WorkFlowOperation','WorkFlowOperationId','StartDate','EndDate','ActualStartDate','ActualEndDate','UOM','EntName','EntID','PlantName','PlantId','AreaName','AreaId','LineName','LineId','CycleTime','shift','ViewDetails','Factory','stdHC','actHC','salesOrder','shiftId',"WOType","ShiftCapacity","WorkorderID","Assembytype","LineType"]	
#		
#		ViewDetails=''
#		DataList=[Id,WONo,WOQty,PartNo,Revision,WOCompletion,WoStatus,WorkFlow,WorkFlowId,WorkFlowOperation,WorkFlowOperationId,StartDate,EndDate,ActualStartDate,ActualEndDate,UOM,EntName,EntID,PlantName,PlantId,AreaName,AreaId,LineName,LineId,CycleTime,shift,ViewDetails,Factory,stdHC,actHC,salesOrder,shiftId,WOType]
#		WODetailList.append(DataList)
#	print 'API Result:-->' +str(WODetailList)
#	header=['Sr No','WONo','WOQty','PartNo','Revision','WOCompletion','WoStatus','WorkFlow','WorkFlowId','WorkFlowOperation','WorkFlowOperationId','StartDate','EndDate','ActualStartDate','ActualEndDate','UOM','EntName','EntID','PlantName','PlantId','AreaName','AreaId','LineName','LineId','CycleTime','shift','ViewDetails','Factory','stdHC','actHC','salesOrder','shiftId',"WOType"]
	Result = system.dataset.toDataSet(header,WODetailList)	
	return Result
	
#-------------------------List Running Workorders---------------------------------------------------------

def getProductionRunningWos(entId,plantId,areaId,lineId,userId):	
#	apiPath='ProductionOperatorConsole/GetProductionUserAssignList/'+str(entId)+'/'+str(plantId)+'/'+str(areaId)+'/'+str(lineId)+'/'+str(userId)+'/'+str(woNo)
	apiPath='OperatorConsole/GetOperatorConsoleWorkOrdersDetails?EnterpriseId='+str(entId)+'&PlantId='+str(plantId) + '&AreaId='+str(areaId)+'&LineId='+str(lineId)+'&MachineId='+str(0)+'&UserId='+str(userId)
	url = URLPath + apiPath
	print url
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  APIResult=data.json
#	  APIResult=[{'WONo':'12976156','WOQty':432,'PartNo':'1339-10E0023','Revision':'A','WOCompletion':0,'WoStatus':'Not-Started','WorkFlow':'P_AA_2022-1020456EP_B_CNS','WorkFlowId':97,'WorkFlowOperation':'Molding','WorkFlowOperationId':97,'StartDate':'2021-03-27T23:22:00','EndDate':'2021-03-29T23:22:00','ActualStartDate':'2021-03-27T23:22:00','ActualEndDate':'2021-03-29T23:22:00','UOM':'EA','EntName':'JohnsonElectric','EntID':0,'PlantName':'Jiangmen','PlantId':0,'AreaName':'CNS','AreaId':6,'LineName':'AA','LineId':8,'CycleTime':2,'shift':'Shift-A'}]
	print"ResultData",(APIResult)	
	WODetailList=[]
	Id=0
	for i in (APIResult):
		Id=Id+1
		WoStatus=i.get('WoStatus')
#		if WoStatus=='In-Progress':
		WONo=i.get('WONo')
		WOQty=i.get('WOQty')
		LineName=i.get('LineName')
		WoStatus=i.get('WoStatus')
		WorkOrderId=i.get('WorkOrderId')
		
		DataList=[WONo,WoStatus,WOQty,LineName,WoStatus,WorkOrderId]
		WODetailList.append(DataList)
#		else:
#			pass
		
	print 'API Result:-->' +str(WODetailList)
	header=['WONo','WoStatus','WOQty','LineName','WoStatus','WorkOrderId']
	Result = system.dataset.toDataSet(header,WODetailList)	
	return Result

#---------------------------------------------List of CNS Wo----------------------------------------------------------
def getUserAssignedCNSWOList(entId,plantId,areaId,lineId,userId):	
#	apiPath='ProductionOperatorConsole/GetProductionUserAssignList/'+str(entId)+'/'+str(plantId)+'/'+str(areaId)+'/'+str(lineId)+'/'+str(userId)+'/'+str(woNo)
	apiPath='OperatorConsole/GetOperatorConsoleWorkOrdersDetails?EnterpriseId='+str(entId)+'&PlantId='+str(plantId) + '&AreaId='+str(areaId)+'&LineId='+str(lineId)+'&MachineId='+str(0)+'&UserId='+str(userId)
	url = URLPath + apiPath
	print url
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  APIResult=data.json
#	  APIResult=[{'WONo':'12976156','WOQty':432,'PartNo':'1339-10E0023','Revision':'A','WOCompletion':0,'WoStatus':'Not-Started','WorkFlow':'P_AA_2022-1020456EP_B_CNS','WorkFlowId':97,'WorkFlowOperation':'Molding','WorkFlowOperationId':97,'StartDate':'2021-03-27T23:22:00','EndDate':'2021-03-29T23:22:00','ActualStartDate':'2021-03-27T23:22:00','ActualEndDate':'2021-03-29T23:22:00','UOM':'EA','EntName':'JohnsonElectric','EntID':0,'PlantName':'Jiangmen','PlantId':0,'AreaName':'CNS','AreaId':6,'LineName':'AA','LineId':8,'CycleTime':2,'shift':'Shift-A'}]
	print"ResultData",(APIResult)	
	WODetailList=[]
	Id=0
	for i in (APIResult):
		AreaName=i.get('AreaName')
		if AreaName=='CNS':
			Id=Id+1
			WONo=i.get('WONo')
			WOQty=i.get('WOQty')
			WorkFlow=i.get('WorkFlow')
			WorkFlowId=i.get('WorkFlowId')
			WorkFlowOperation=i.get('WorkFlowOperation')
			WorkFlowOperationId=i.get('WorkFlowOperationId')
			StartDate=i.get('StartDate')
	#		StartDate=system.date.format(StartDate1,"DD/MM/YYYY hh:mm:ss")
			EndDate=i.get('EndDate')
			ActualStartDate=i.get('ActualStartDate')
			if str(ActualStartDate) == str("null") or ActualStartDate == None: 
				ActualStartDate = ''
			ActualEndDate=i.get('ActualEndDate')
			if str(ActualEndDate) == str("null") or ActualEndDate == None: 
				ActualEndDate = ''
			WoStatus=i.get('WoStatus')
			WOCompletion=i.get('WOCompletion')
			PartNo=i.get('PartNo')
			Revision=i.get('Revision')
			UOM=i.get('UOM')
			EntName=i.get('EnterpriseName')
			EntID=i.get('EnterpriseId')
			PlantName=i.get('PlantName')
			PlantId=i.get('PlantId')
			
			AreaId=i.get('AreaId')
			LineName=i.get('LineName')
			LineId=i.get('LineId')
			CycleTime=i.get('Cycletime')
			Factory=i.get('Factory')
			shift=i.get('Shift')
			stdHC=i.get('Manpower')
			actHC=i.get('ActualHeadCount')
			salesOrder=i.get('SalesOrder')		
			shift='Shift A'
			ViewDetails=''
			DataList=[Id,WONo,WOQty,PartNo,Revision,WOCompletion,WoStatus,WorkFlow,WorkFlowId,WorkFlowOperation,WorkFlowOperationId,StartDate,EndDate,ActualStartDate,ActualEndDate,UOM,EntName,EntID,PlantName,PlantId,AreaName,AreaId,LineName,LineId,CycleTime,shift,ViewDetails,Factory,stdHC,actHC,salesOrder]
			WODetailList.append(DataList)
		else:
			pass
	print 'API Result:-->' +str(WODetailList)
	header=['Sr No','WONo','WOQty','PartNo','Revision','WOCompletion','WoStatus','WorkFlow','WorkFlowId','WorkFlowOperation','WorkFlowOperationId','StartDate','EndDate','ActualStartDate','ActualEndDate','UOM','EntName','EntID','PlantName','PlantId','AreaName','AreaId','LineName','LineId','CycleTime','shift','ViewDetails','Factory','stdHC','actHC','salesOrder']
	Result = system.dataset.toDataSet(header,WODetailList)	
	return Result
#------------------------------Production hourly report Data for production operator console ----------------
#---------------------------------------------------------------------------------------------------------------------

def getProductionDetails(shiftId,shiftDate,woNo):	
# 	apiPath = "ProductionOperatorConsole/GetShiftProductionDetails/1/123/123"	
 	apiPath ="ProductionOperatorConsole/GetShiftProductionDetails/"+str(shiftId)+"/"+str(shiftDate)+"/"+str(woNo)
	url = URLPath + apiPath
	print url
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	return resultData
	
def assignedUserListagainstWo(woNo,shift):
 	apiPath = 'LineUserAssignment/GetAssignedUsersByWorkOrderForProductionOperatorConsole?WorkOrderId='+str(woNo)+('&Shift=')+str(shift)
#/LineUserAssignment/GetAssignedUsersByWorkOrderForProductionOperatorConsole?WorkOrderId=211167&Shift=2
 		
	url = URLPath + apiPath
	system.perspective.print(url)
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	return resultData
	
#-------------------------------------------------------Shift Details------------------------
def getShiftDetails(userId):
 	apiPath = "Report/GetShift/"+str(userId)	
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	return resultData	
	
def AddAutoDowntime(TagMachineName):
	print "inside Add downtime script: ",TagMachineName
	TagPath = str(defaultPath)+str(TagMachineName)
	TagRepairValue = system.tag.read(str(TagPath)+'/Repair.value').value
	system.tag.write("[default]JEMESMachines/MYE_WIND_110A_012/TotalQty.value",TagRepairValue)
	if TagRepairValue == int(2) or TagRepairValue == 2:
		scanBadgeText = "Machine"
		downtimeReasonId = 13
		commentText = "Machine Generated  Downtime"	
		userID = 1
		
		Result = PackingAndLabelling.getActiveWorkOrderMachineList()
		print "ResultData",Result
		for row in Result:
			machineName = row.get("MachineName")
			StatusId = row.get("StatusId")
			if str(machineName).strip() == str(TagMachineName).strip():
				machineId = row.get("MachineId")
				machineName = row.get("MachineName")	
				WorkflowId = row.get("WorkflowId")
				WorkflowOperationsId = row.get("WorkflowOperationsId")
				WoNumber = row.get("WorkOrderNo")
				lineID = row.get("LineId")
				break
			else:
				pass
	
		tagPath = str(defaultPath)+str(machineName)
		repairValue = system.tag.read(str(tagPath)+'/Repair.value').value
		print "Repair Value before Update",repairValue
		if repairValue == int(2):
			import time
			time.sleep(60)
			afterRepairValue = system.tag.read(str(tagPath)+'/Repair.value').value
			system.tag.write("[default]JEMESMachines/MYE_WIND_110A_012/TotalQty",9890)
			if afterRepairValue == int(2):
				saveResult = WorkOrderDetailsAPI.updateDowntimes(WorkflowOperationsId,WoNumber,scanBadgeText,downtimeReasonId,commentText,lineID,machineId,userID)		
				AddDowntime= WorkOrderDetailsAPI.AddDowntime(WorkflowOperationsId,WoNumber,WorkflowId,userID,machineId)
				system.tag.write("[default]JEMESMachines/MYE_WIND_110A_012/TotalQty",2)
				print "Breakdown Alert is Created"
			else:
				print "Failed the condition"
				pass
		else:
			pass
	else:
		pass
		
#-----------------------------------------------------Mold Details Against WO No and Machine ID---------------------------------

#-----------------------------------------------------Mold Details Against WO No and Machine ID---------------------------------
	
def getMoldAssignmentDetails(WoNumber,machineID):	
	apiPath = "OperatorConsole/OperatorconsoleMoldAssignmentCheck?WorkOrderNo="+str(WoNumber)+"&MachineId="+str(machineID)	
	url = URLPath + apiPath
	resultData = None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData = data.json
	dataList = []	
	print'moldDetails API Result'+str(resultData)	
	for i in resultData:
		isLoaded = (i.get("isLoaded"))
		print'IsLoaded'+str(isLoaded)
		if isLoaded==1 or isLoaded=='1' or isLoaded=='True' or isLoaded==True:			
			MoldCode = i.get("MoldCode")
			MachineId = i.get("MachineId")
			cavity = i.get("Cavity")
			productPiece = i.get("ProductPiece")		
			MaxLife = i.get("MaxLife")
			MachineShots = i.get("Shots")
								
			myList = [MoldCode,cavity,productPiece,MaxLife,MachineId,MachineShots] 		
			dataList.append(myList)
								
	headers = ["MoldCode","Cavity","ProductPiece","MaxLife","MachineId","MachineShots"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails
	
#-----------------------------------------------------New Mold Details Against WO No and Machine ID---------------------------------
# Application use: Production Operator Console --> Display Mold information widget
# Developer Name: Hari Mhasalekar
# Created On: 
# Updated By : 
# Updated On :	
def NewgetMoldAssignmentDetails(WorkorderId,machineID):
	dataList = []	
	if str(WorkorderId).strip() != '' and str(WorkorderId).strip()!= None and str(WorkorderId).strip() != 'None' and str(WorkorderId).lower().strip() != 'value':
#		apiPath = "OperatorConsole/OperatorconsoleMoldAssignmentCheck?WorkOrderNo="+str(WorkorderId)+"&MachineId="+str(machineID)	
		apiPath='OperatorConsole/OperatorconsoleMoldAssignmentCheck?WorkOrderId='+str(WorkorderId)+'&MachineId='+str(machineID)
		url = URLPath + apiPath
		resultData = None
		client = system.net.httpClient()
		data = client.get(url)
#		print data
		if data.good:    
		  resultData = data.json
		for i in resultData:
			isLoaded = (i.get("isLoaded"))
			if isLoaded == 1 or isLoaded=='1' or isLoaded=='True' or isLoaded==True:	
				MachineName = i.get("MachineName")		
				MoldCode = i.get("MoldCode")
				MachineId = i.get("MachineId")
				cavity = i.get("Cavity")
				productPiece = i.get("ProductPiece")		
				MaxLife = i.get("MaxLife")
				MachineShots = i.get("Shots")
				ActualLife = i.get("ActualLife")
				AlertQty = i.get("AlertQty")
				ToolName = i.get("ToolName")
				myList = {'MachineName':MachineName,'MachineId':MachineId,'MoldCode':MoldCode,'cavity':cavity,'productPiece':productPiece,'MaxLife':MaxLife,'MachineShots':MachineShots,'ActualLife':ActualLife,'AlertQty':AlertQty,'ToolName':ToolName}						
#				myList = {'MachineName':MachineName,'MachineId':MachineId,'MoldCode':MoldCode,'cavity':cavity,'productPiece':productPiece,'MaxLife':MaxLife,'MachineShots':MachineShots,'ActualLife':ActualLife}		
				dataList.append(myList)
	return dataList	

#-------------------------------------------------------------------Srap Details--------------------------------------
def getScrapReport(PartName,Rev,Factory):	
	apiPath='ProductionOperatorConsole/GetComponentDetails/'+str(PartName)+'/'+str(Rev) + '/'+str(Factory)
	url = URLPath + apiPath
	print url
	APIResult=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  APIResult=data.json
#	  APIResult=[{'WONo':'12976156','WOQty':432,'PartNo':'1339-10E0023','Revision':'A','WOCompletion':0,'WoStatus':'Not-Started','WorkFlow':'P_AA_2022-1020456EP_B_CNS','WorkFlowId':97,'WorkFlowOperation':'Molding','WorkFlowOperationId':97,'StartDate':'2021-03-27T23:22:00','EndDate':'2021-03-29T23:22:00','ActualStartDate':'2021-03-27T23:22:00','ActualEndDate':'2021-03-29T23:22:00','UOM':'EA','EntName':'JohnsonElectric','EntID':0,'PlantName':'Jiangmen','PlantId':0,'AreaName':'CNS','AreaId':6,'LineName':'AA','LineId':8,'CycleTime':2,'shift':'Shift-A'}]
	print"ResultData",(APIResult)	
	WODetailList=[]
	Id=0
	
	for i in (APIResult):
		Id=Id+1
		BomName=i.get('BomName')
		ItemName=i.get('ComponentName')
		Revision=i.get('Revision')
		Description=i.get('Description')
		UOM=i.get('UOMName')
		UnitUsage=i.get('Qty')
#		deffectedQty=float(deffectedQty1)
#		UnitUsage= float(deffectedQty*UnitUsage1)
		OriginalRequirement=0
		OkProductionConsumption=0
		DataList=[Id,BomName,ItemName,Revision,Description,UOM,UnitUsage,OriginalRequirement,OkProductionConsumption,]
		WODetailList.append(DataList)
	print 'API Result:-->' +str(WODetailList)
	header=['Sr No','BOM Name','Item Name','Revision','Description','UOM','Unit Usage','Original Requirement','Ok Prod Consumption']
	Result = system.dataset.toDataSet(header,WODetailList)	
	return Result
	
#-----------------------------------------------------------------------------------------------------------------------
# This Function returns the linked mold Name,Mold Id,Mold Code,IsLoaded Status based on WorkorderNumber and Machine Name
# Created Date:18/01/2023
# Created By : Sushant	
def getMachineLinkedMoldDetails(WoNumber,machineID):	
		apiPath = "OperatorConsole/OperatorconsoleMoldAssignmentCheck?WorkOrderNo="+str(WoNumber)+"&MachineId="+str(machineID)	
		url = URLPath + apiPath
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)		
		resultData= system.util.jsonDecode(data)
		dataList = []		
		for i in resultData:			
			WoNumber = i.get("WorkOrderNo")
			MachineId = i.get("MachineId")
				
			isMoldLinked = i.get("isMoldLinked")					
			myList = [WoNumber,MachineId,cavity,productPiece,isMoldLinked] 		
			dataList.append(myList)	
			
#----------------------------------------------------------------------Get Direct Labour & Indirect Labour--------------------
def getdirectIndirectLabour(woNo,shift,lineId):
 	apiPath = "LineUserAssignment/GetDirectUserInDirectUserCount?WorkOrderNo="+str(woNo)+('&Shift=')+str(shift)+('&lineId=')+str(lineId)	
 	
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	return resultData
	
#------------------------------------------------------------Save Direct indirect User-------------------------------------------
def updateParameterDetailsInSQLDB(woNo,shift,lineId,dL,iDL):

	apiPath ="LineUserAssignment/AddUpdateDirectUserInDirectUserCount?WorkOrderNo="+str(woNo)+"&Shift="+str(shift)+"&lineId="+str(lineId)+"&DirectUser="+str(dL)+"&IndirectUser="+str(iDL)
	url = URLPath + apiPath	
	result = 1	
	try: 
		postReturn = system.net.httpPost(url,'application/json')		
	except:		
		result = 0
		pass
	return result 	
	
#----------------------------------------------------------------------Get List oF Quality Alerts--------------------
def getQualityAlertsList(woNo):
# 	apiPath = "OperatorConsole/GetWorkorderDefectInformation?Workorder="+str(woNo)+"&PartNo="+str(partNO)	
 	apiPath ="InspectionProcessManager/GetQualityAlerts?woNumber="+str(woNo)	
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
  	Id=0
  	QualityAlertDetailList=[]
	for i in (resultData):
			Id=Id+1
			Workorder=i.get('WorkOrderNumber')
			InspectionName=i.get('InspectionName')
			CharName=i.get('CharacteristicsName')
			MaxLim=i.get('MaximumLimit')
			MinLimi=i.get('MinimumLimit')
			NominalValue=i.get('NominalValue')
			ActualValue=i.get('ActualValue')
			CreatedOn=i.get('RaisedOn')
			CreatedBy=i.get('LoginId')
			DataList=[Id,Workorder,InspectionName,CharName,MaxLim,MinLimi,NominalValue,ActualValue,CreatedOn,CreatedBy]
			QualityAlertDetailList.append(DataList)
	print 'API Result:-->' +str(QualityAlertDetailList)
	header=['SrNo','Workorder Name','Inspection Name','Characteristics Name','Max Limit','Min Limit','Nominal Value','Actual Value',"Created On","Created By"]
	Result = system.dataset.toDataSet(header,QualityAlertDetailList)			
	return Result
	
#----------------------------------------------------------------------Get List oF deffects--------------------

#----------------------------------------------------------------------Get List oF deffects--------------------
def getdiffectList(woNo,partNO):
 	apiPath = "OperatorConsole/GetWorkorderDefectInformation?Workorder="+str(woNo)+"&PartNo="+str(partNO)		
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
  	Id=0
  	DeffectDetailList=[]
	for i in (resultData):
			Id=Id+1
			Workorder=i.get('Workorder')
			PartNo=i.get('PartNo')
			PartNo=i.get('PartNo')
			DefectQty=i.get('DefectQty')
			RaisedBy=i.get('RaisedBy')
			RaisedOn=i.get('RaisedOn')
			Comment=i.get('Comment')
			isAckbyPea=i.get('IsACKPEA')
			ReasonCodeName=i.get('ReasonCodeName')
			DefectId=i.get('DefectId')
			IsPEAAnalyzed=i.get('IsPEAAnalyzed')
			if IsPEAAnalyzed==True or IsPEAAnalyzed=='true' or IsPEAAnalyzed==1:
				pEAStatus = 'Analysed'
			else:
				pEAStatus = 'Not-Analysed'
			ReasoneCodeId=i.get('CodeId')
			Action = ''
#			OriginalRequirement=0
#			OkProductionConsumption=0
			DataList=[Id,Workorder,PartNo,DefectQty,RaisedBy,RaisedOn,isAckbyPea,Comment,ReasonCodeName,DefectId,pEAStatus,Action,ReasoneCodeId]
			DeffectDetailList.append(DataList)
	print 'API Result:-->' +str(DeffectDetailList)
	header=['SrNo','Workorder Name','Part No','Defect Qty','Raised By','Raised On','ACK By PEA','Comment','ReasonCodeName','DefectId','IsPEAAnalyzed','Action','ReasoneCodeId']	
	Result = system.dataset.toDataSet(header,DeffectDetailList)			
	return Result
#----------------------------------------------------------------------Get  deffects list for all WOs--------------------
def getAllWOdiffectList():
 	apiPath = "OperatorConsole/GetALLWorkorderDefectInformation"	
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
  	Id=0
  	woDeffectDetailList=[]
	for i in (resultData):
			Id=Id+1
			
			DefectId=i.get('DefectId')
			Workorder=i.get('Workorder')
			WorkorderStatus=i.get('WorkorderStatus')
			PartNo=i.get('PartNo')
			PartNoRev=i.get('Productrevision')
			DefectQty=i.get('DefectedQty')
			WoQty=i.get('PLANNEDQTY')
			WoStartDate=i.get('PLANNEDSTARTDATE')
			WoEndDate=i.get('PLANNEDCOMPLETIONDATE')
			LineName=i.get('LineName')
			LineId=i.get('LineId')
			RaisedOn=i.get('RaisedOn')
			RaisedBy=i.get('RaisedBy')
			Comment=i.get('Comment')			
			View=''
			DataList=[Id,DefectId,Workorder,PartNo,PartNoRev,WoQty,DefectQty,WorkorderStatus,LineName,LineId,RaisedOn,RaisedBy,Comment,View]
			woDeffectDetailList.append(DataList)
	print 'API Result:-->' +str(woDeffectDetailList)
	header=['SrNo','DefectId','Workorder Name','Part No','PartNoRev','Workorder Qty','Defect Qty','Workorder Status','Line Name','LineId',"Raised On","Raised By","Comment","View Details"]
	Result = system.dataset.toDataSet(header,woDeffectDetailList)			
	return Result
#----------------------------------------------------------------------Get  Quality Details For landing Page--------------------
def getqualityDetails(woNo,partNo,Revision):
# 	apiPath = "OperatorConsole/GetALLWorkorderDefectInformation"

 	apiPath ="OperatorConsole/GetQualityDetails?WorkOrderNo="+str(woNo)+("&partNo=")+str(partNo)+("&Revision=")+str(Revision)	
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
  	Id=0
  	WorkorderNo=woNo
  	qualityDetailList=[]
	for i in (resultData):
			Id=Id+1
			WoNo=i.get('WorkorderNo')
#			if WorkorderNo=WoNo:
			PartNo=i.get('PartNo')
			PartRev=i.get('PartRevision')
			Factory=i.get('FactoryName')
			LotNo=i.get('LotNumber')
			ProductionQty=i.get('ProductionQty')
			PEAOk=i.get('PEAOK')
			IslastLot=i.get('IsLastLot')
			CreatedBy=i.get('CreatedBy')
			CreatedOn=i.get('CreatedOn')
			Comment=i.get('Comment')
			IsProcessed=i.get('IsProcessed')
			View=''
			LineId=i.get('LineId') 
#			DataList=[Id,Workorder,PartNo,PartNoRev,WoQty,DefectQty,WorkorderStatus,LineName,LineId,RaisedOn,RaisedBy,Comment,View]
			DataList=[Id,WoNo,PartNo,PartRev,LotNo,ProductionQty,PEAOk,IslastLot,CreatedBy,CreatedOn,Comment,IsProcessed,View,Factory,LineId]
			qualityDetailList.append(DataList)
	print 'API Result:-->' +str(qualityDetailList)
	header=['SrNo','Workorder Name','Part No','PartNoRev','LotNo','Production Qty','PEAOk','IslastLot','CreatedBy',"CreatedOn","Comment","IsProcessed","View Details","Factory","LineId"]
	Result = system.dataset.toDataSet(header,qualityDetailList)			
	return Result
	
#----------------------------------------------------------------------Get  Quality Details For Lot Information--------------------
def getLotInfo(woNo):
# 	apiPath = "OperatorConsole/GetALLWorkorderDefectInformation"
 	apiPath ="OperatorConsole/GetQualityDetails"   #+str(woNo)+("&partNo=")+str(partNo)+("&Revision=")+str(Revision)	
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
  	Id=0
  	WorkorderNo=woNo
  	qualityDetailList=[]
	for i in (resultData):
			Id=Id+1
			WoNo=i.get('WorkorderNo')
#			if WorkorderNo=WoNo:
			PartNo=i.get('PartNo')
			PartRev=i.get('PartRevision')
			LotNo=i.get('LotNumber')
			ProductionQty=i.get('ProductionQty')
			PEAOk=i.get('PEAOK')
			IslastLot=i.get('IsLastLot')
			CreatedBy=i.get('CreatedBy')
			CreatedOn=i.get('CreatedOn')
			Comment=i.get('Comment')
			IsProcessed=i.get('IsProcessed')
			View=''
#			DataList=[Id,Workorder,PartNo,PartNoRev,WoQty,DefectQty,WorkorderStatus,LineName,LineId,RaisedOn,RaisedBy,Comment,View]
			DataList=[Id,WoNo,PartNo,PartRev,LotNo,ProductionQty,PEAOk,IslastLot,CreatedBy,CreatedOn,Comment,IsProcessed,View]
			qualityDetailList.append(DataList)
	print 'API Result:-->' +str(qualityDetailList)
	header=['SrNo','Workorder Name','Part No','PartNoRev','LotNo','Production Qty','PEAOk','IslastLot','CreatedBy',"CreatedOn","Comment","IsProcessed","View Details"]
	Result = system.dataset.toDataSet(header,qualityDetailList)			
	return Result


#------------------------------Create New Deffect----------------------------------------------
#------------------------------Create New Deffect----------------------------------------------
def createDeffects(woNo,partNo,deffectedQty,comment,raisedBy,lineName,lineId,ReasonId,workorderId):
	apiPath = "OperatorConsole/AddUpdateWorkorderDefect"
	url = URLPath + apiPath
	
	writeData={
				"workOrderNo": woNo,
				"partNo": partNo,
				"defectQty": deffectedQty,
				"comment": comment,
				"raisedBy": raisedBy,
				"lineName": lineName,
				"lineId": lineId,
				"CodeId": ReasonId,
				"workorderId":workorderId
				}
	
	
	jsonParams = system.util.jsonEncode(writeData)	
	createdeffect = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
	except:		
		createdeffect = 0
		pass
	return createdeffect
	
#----------------------------------------------------------------------Get Good Qty against WO No--------------------
def getGoodQty(WorkorderId):
# 	apiPath ="ProductionOperatorConsole/getWorkorderProductionCount/workOrderNo?workOrderNo="+str(WorkorderId)
	apiPath="ProductionOperatorConsole/getWorkorderProductionCount/WorkOrderId:int?WorkOrderId="+str(WorkorderId)
	url = URLPath + apiPath
	print url
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	return resultData
	
#----------------------------------------------------------------------Workorder Isprocessed in Quality--------------------
def IsprocessedInQuality(woNo):
# 	apiPath = "LineUserAssignment/GetDirectUserInDirectUserCount?WorkOrderNo="+str(woNo)+('&Shift=')+str(shift)+('&lineId=')+str(lineId)	
 	apiPath ="OperatorConsole/CheckAllLotCompletedForWorkOrder?Workorder="+str(woNo)
	url = URLPath + apiPath
	print url
#	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	return resultData
	
#----------------------------------------------------------------------Get current Shift Id--------------------
def getCurrentShiftId():
# 	apiPath = "LineUserAssignment/GetDirectUserInDirectUserCount?WorkOrderNo="+str(woNo)+('&Shift=')+str(shift)+('&lineId=')+str(lineId)	
 	apiPath ="OperatorConsole/GetCurrentShiftId"
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	return resultData
	
#------------------------------Save Production Scrap Reports----------------------------------------------
def reportProdScrap(woNo,LineId,partNo,userId,bomComponentDetails,WorkorderId):
#	apiPath = "OperatorConsole/AddUpdateProductionScrapDetails"
	try:
		apiPath = "OperatorConsole/AddUpdateProductionScrapDetails"		
		url = URLPath + apiPath	
		print url	
		writeData={
					  "workOrderNo": woNo,
					  "workorderId": WorkorderId,
					  "lineID": LineId,
					  "woPartNo": partNo,
					  "prodBomDetails":bomComponentDetails,
					  "scrapCreatedBy": userId,
					   "scrapCreatedOn": "2023-03-17T06:59:13.379Z"				  
					}			
		jsonParams = system.util.jsonEncode(writeData)	
		system.perspective.print("Production Save Scrap JSON---"+str(jsonParams))
		createdeffect = 1	
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		return createdeffect
	except:	
		postReturn=system.util.jsonEncode(writeData)
		print(postReturn)	
		createdeffect = 0

		return createdeffect
#------------------------------Save PEA Scrap Reports----------------------------------------------
def reportPEAScrap(woNo,shiftId,partNo,userId,bomComponentDetails):
	apiPath = "OperatorConsole/AddUpdatePEAScrapDetails"
	url = URLPath + apiPath
	
	writeData={
				  "workOrderNo": woNo,
				  "shiftId": shiftId,
				  "woPartNo": partNo,
				  "peaBomDetails":bomComponentDetails,
				  "scrapCreatedBy": userId 
				}	
	jsonParams = system.util.jsonEncode(writeData)	
	createdeffect = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
	except:		
		createdeffect = 0
		pass
	return createdeffect	
	
#------------------------------Save Quality Scrap Reports----------------------------------------------
def reportQualityScrap(woNo,partNo,userId,qaBomDetails):
	apiPath = "OperatorConsole/AddUpdateQAScrapDetails"
	url = URLPath + apiPath
	print url
	
	writeData={
				  "workOrderNo": woNo,
				  "woPartNo": partNo,				  
				  "qaBomDetails":qaBomDetails,
				  "scrapCreatedBy": userId 
				}
					
	jsonParams = system.util.jsonEncode(writeData)
	system.perspective.print("Quality Json" +str(jsonParams))
		
	createdeffect = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
	except :		
		createdeffect = 0
#		postReturn = system.net.httpPost(url,'application/json',jsonParams)
#		system.perspective.print (postReturn)
		pass
	return createdeffect	

#------------------------------------------------------------Save Line Lead Production Count-------------------------------------------
def updateProductionCount(WorkorderId,productionCount,userId,PartNo):
	try:
		system.perspective.print('Inside Script  the Update woNo :' + str(woNo))
		system.perspective.print('Inside Script  the Update productionCount :' + str(productionCount))
		system.perspective.print('Inside Script  the Update userId :' + str(userId))
		system.perspective.print('Inside Script  the Update PartNo :' + str(PartNo))
	except:
		pass
#	apiPath ="ProductionOperatorConsole/CreateScrapDetails/"+str(productionCount)+('/')+str(userId)+('/')+(woNo)+("/")+(PartNo)
	apiPath = "ProductionOperatorConsole/CreateScrapDetails/"+str(productionCount)+"/"+str(userId)+"/"+str(WorkorderId)+"/"+str(PartNo)
	url = URLPath + apiPath	
	result = 1
	system.perspective.print('API URL:' + str(url))	
	try: 
		postReturn = system.net.httpPost(url,'application/json')
#		result=postReturn		
		print('Inside Script  the Update postReturn' + str(postReturn))
	except:		
		result = 0
		pass
	return result

#---------------------------------------------Production Scrap History----------------------------------------------------------
def getProductionScrapHistory(screenNo,WorkorderId,partNo,factory,revision,partNoWithoutFactory,LineId,UserId):
	try:	
#		apiPath="OperatorConsole/GetScrapDetailsForProductionPEAQA?WHICHSCREEN="+str(screenNo)+("&WorkOrderNo=")+str(WorkorderId)+str("&partNo=")+str(partNo)+str("&Factory=")+str(factory)+str("&Revision=")+str(revision)+str("&PartNoWithoutDetails=")+str(partNoWithoutFactory)+str("&LineID=")+str(LineId)+str("&UserID=")+str(UserId)
		apiPath="OperatorConsole/GetScrapDetailsForProductionPEAQA?WHICHSCREEN="+str(screenNo)+"&WorkOrderId="+str(WorkorderId)+"&partNo="+str(partNo)+"&Factory="+str(factory)+"&Revision="+str(revision)+"&PartNoWithoutDetails="+str(partNoWithoutFactory)+"&LineID="+str(LineId)+"&UserID="+str(UserId)
		url = URLPath + apiPath
#		print url
		print('API Resul urlt:-->' +str(url))
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		print('API Result:-->' +str(data))
		if data.good:    
		  APIResult=data.json
#		  print('API Result:-->' +str(APIResult))
	#	  APIResult=[{'WONo':'12976156','WOQty':432,'PartNo':'1339-10E0023','Revision':'A','WOCompletion':0,'WoStatus':'Not-Started','WorkFlow':'P_AA_2022-1020456EP_B_CNS','WorkFlowId':97,'WorkFlowOperation':'Molding','WorkFlowOperationId':97,'StartDate':'2021-03-27T23:22:00','EndDate':'2021-03-29T23:22:00','ActualStartDate':'2021-03-27T23:22:00','ActualEndDate':'2021-03-29T23:22:00','UOM':'EA','EntName':'JohnsonElectric','EntID':0,'PlantName':'Jiangmen','PlantId':0,'AreaName':'CNS','AreaId':6,'LineName':'AA','LineId':8,'CycleTime':2,'shift':'Shift-A'}]
		print"ResultData",(APIResult)	
		ProdScrapHistory=[]
		Id=0
		
		for i in (APIResult):
			Id=Id+1
			BomName=i.get('BomName')			
			Revision=i.get('Revision')
			Description=i.get('Description')
	
			UOM=i.get('UOM')
			UnitUsage=i.get('UnitUsage')
			ScrapByUnit=i.get('ScrapByUnit')
			ScrapByUnit=0.000
			ScrapByFG=i.get('ScrapByFG')
			TotalScrap=i.get('TotalScrap')			
			LotNumber=i.get('LotNumber')
			Vendorlot=i.get('Vendorlot')
			BomDetailsId=i.get('BomDetailsId')
			MstItemId=i.get('MstItemId')
			BomID=i.get('BomID')
			LineID=i.get('LineID')		
			MachineID=i.get('MachineID')
			BobbinsId=i.get('BobbinsId')
			HeadName=i.get('HeadName')
			EquipmentCode=i.get('EquipmentCode')
			OperationName=i.get('OperationName')
			Cummulative=i.get('Cummulative')
			RemainingQty=i.get('RemainLotQuantity')
			IsMaterialRequest = i.get("IsMaterialRequested")
#			system.perspective.print("Cummulative; "+str(Cummulative))
			
			DataList=(Id,BomName,Revision,Description,UOM,UnitUsage,ScrapByUnit,ScrapByFG,Cummulative,LotNumber,Vendorlot,BomDetailsId,MstItemId,BomID,LineID,MachineID,BobbinsId,HeadName,EquipmentCode,OperationName,RemainingQty,IsMaterialRequest)
			ProdScrapHistory.append(DataList)
			
		system.perspective.print('API Result:-->' +str(ProdScrapHistory))
		header=['Sr No','BOM Name','Revision','Description','UOM','UnitUsage','ScrapByUnit', 'ScrapByFG','TotalScrap', 'JE Lot','Vendor Lot','BomDetailsId','MstItemId','BomID','LineID','MachineID','BobbinsId','HeadName','EquipmentCode','OperationName','RemainingQty','IsMaterialRequest']
		Result = system.dataset.toDataSet(header,ProdScrapHistory)		
		return Result
	except :
		print(data)
		return 0
#---------------------------------------------PEA Scrap History----------------------------------------------------------
def getPEAScrapHistory(woNo,partNo,factory,revision,partNoWithoutFactory,scrapByFG):	

	apiPath="OperatorConsole/GetPEAScrapDetails?WorkOrderNo="+str(woNo)+("&partNo=")+str(partNo)+("&Factory=")+str(factory)+("&Revision=")+str(revision)+("&PartNoWithoutDetails=")+str(partNoWithoutFactory)
	url = URLPath + apiPath
	print url
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  APIResult=data.json
#	  APIResult=[{'WONo':'12976156','WOQty':432,'PartNo':'1339-10E0023','Revision':'A','WOCompletion':0,'WoStatus':'Not-Started','WorkFlow':'P_AA_2022-1020456EP_B_CNS','WorkFlowId':97,'WorkFlowOperation':'Molding','WorkFlowOperationId':97,'StartDate':'2021-03-27T23:22:00','EndDate':'2021-03-29T23:22:00','ActualStartDate':'2021-03-27T23:22:00','ActualEndDate':'2021-03-29T23:22:00','UOM':'EA','EntName':'JohnsonElectric','EntID':0,'PlantName':'Jiangmen','PlantId':0,'AreaName':'CNS','AreaId':6,'LineName':'AA','LineId':8,'CycleTime':2,'shift':'Shift-A'}]
	
	ProdScrapHistory=[]
	Id=0
	scrapByFG=scrapByFG
	for i in (APIResult):
		Id=Id+1
		BomName=i.get('BomName')			
		ItemName=i.get('ItemName')
		Revision=i.get('Revision')
		ScrapByUnit=0
		UOM=i.get('UOM')
		Description=i.get('Description')
		UnitUsage=i.get('UnitUsage')
		CummulativeScrap=i.get('ScrapByUnit')
#		RemainingQty=i.get('RemainLotQuantity')
				
		ScrapByFG=float(UnitUsage*scrapByFG)
		DataList=[Id,BomName,ItemName,Revision,Description,UOM,UnitUsage,ScrapByFG,CummulativeScrap,ScrapByUnit]
		ProdScrapHistory.append(DataList)
		
	print 'API Result:-->' +str(ProdScrapHistory)
	header=['Sr No','BOM Name','Item Name','Revision','Description','UOM','Unit Usage','ScrapByFG','CumulativeScrap','Ok Prod Consumption']
	Result = system.dataset.toDataSet(header,ProdScrapHistory)		
	return Result
	
#---------------------------------------------Quality Scrap History----------------------------------------------------------
def getQualityScrapHistory(woNo,partNo,factory,revision,partNoWithoutFactory,scrapByFG,totalContainerQty,LineId,userId):	
#		apiPath="OperatorConsole/GetQAScrapDetails?WorkOrderNo="+str(woNo)+("&partNo=")+str(partNo)+("&Factory=")+str(factory)+("&Revision=")+str(revision)+("&PartNoWithoutDetails=")+str(partNoWithoutFactory)
	apiPath="OperatorConsole/GetQAScrapDetails?WorkOrderNo="+str(woNo)+("&partNo=")+str(partNo)+("&Factory=")+str(factory)+("&Revision=")+str(revision)+("&PartNoWithoutDetails=")+str(partNoWithoutFactory)+("&LineID=")+str(LineId)+str("&UserID=")+str(userId)
	
#	OperatorConsole/GetQAScrapDetails?WorkOrderNo=PE49634085&partNo=1999-1020456EP_F_JPD&Factory=JPD&Revision=F&PartNoWithoutDetails=1999-1020456EP"
	url = URLPath + apiPath
	system.perspective.print("URL:--"+str(url))
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  APIResult=data.json
	  	
	QualityScrapHistory=[]
	Id=0
	scrapByFG1=scrapByFG
	totalContainerQty1=totalContainerQty

	system.perspective.print("API Resul---->"+str(APIResult))
	for i in (APIResult):
		Id=Id+1
		BomName=i.get('BomName')		
		ItemName=i.get('ItemName')
		Revision=i.get('Revision')	
		ScrapByUnit=0
		UOM=i.get('UOM')
		Description=i.get('Description')
		UnitUsage1=i.get('UnitUsage')
		consumption=(UnitUsage1*totalContainerQty1)
		ScrapByUnit=i.get('ScrapByUnit')
		ScrapByFG=float(float(UnitUsage1)*float(scrapByFG1))		
		TotalConsumption1=i.get('TotalConsumption')
		TotalConsumption=float(consumption)
		TotalScrap=i.get('TotalScrap')
		
		LotNumber=i.get('LotNumber')
		ItemId=i.get('ItemId')
		bomdetailsID=i.get('bomdetailsID')
		BomID=i.get('BomID')
		ScrapByUnit=0.0
		DataList=[Id,BomName,ItemName,Revision,Description,UOM,UnitUsage1,ScrapByFG,ScrapByUnit,TotalConsumption,TotalScrap,LotNumber,ItemId,bomdetailsID,BomID]
		QualityScrapHistory.append(DataList)
		
	print 'API Result:-->' +str(QualityScrapHistory)
	header=['Sr No','BOM Name','Item Name','Revision','Description','UOM','Unit Usage','ScrapByFG','ScrapByUnit','Consumption','Total Scrap','LotNumber','ItemId','bomdetailsID','BomID']
	Result = system.dataset.toDataSet(header,QualityScrapHistory)		
	return Result
	


#-----------------------------------------------------------Work Order List For Line Lead

def getLineLeadWo(entId,plantId,areaId,lineId,userId):	

	apiPath="OperatorConsole/GetLineLeadWorkOrdersProductionCompleted?EnterpriseId="+str(entId)+'&PlantId='+str(plantId) + '&AreaId='+str(areaId)+'&LineId='+str(lineId)+'&MachineId='+str(0)+'&UserId='+str(userId)
	
	url = URLPath + apiPath
	print url
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  APIResult=data.json
#	  APIResult=[{'WONo':'12976156','WOQty':432,'PartNo':'1339-10E0023','Revision':'A','WOCompletion':0,'WoStatus':'Not-Started','WorkFlow':'P_AA_2022-1020456EP_B_CNS','WorkFlowId':97,'WorkFlowOperation':'Molding','WorkFlowOperationId':97,'StartDate':'2021-03-27T23:22:00','EndDate':'2021-03-29T23:22:00','ActualStartDate':'2021-03-27T23:22:00','ActualEndDate':'2021-03-29T23:22:00','UOM':'EA','EntName':'JohnsonElectric','EntID':0,'PlantName':'Jiangmen','PlantId':0,'AreaName':'CNS','AreaId':6,'LineName':'AA','LineId':8,'CycleTime':2,'shift':'Shift-A'}]
	print"ResultData",(APIResult)	
	WODetailList=[]
	Id=0
	for i in (APIResult):
		Id=Id+1
		WONo=i.get('WONo')
		WorkorderId=i.get('WorkOrderId')
		WOQty=i.get('WOQty')
		WorkFlow=i.get('WorkFlow')
		WorkFlowId=i.get('WorkFlowId')
		WorkFlowOperation=i.get('WorkFlowOperation')
		WorkFlowOperationId=i.get('WorkFlowOperationId')
		StartDate=i.get('StartDate')
#		StartDate=system.date.format(StartDate1,"DD/MM/YYYY hh:mm:ss")
		EndDate=i.get('EndDate')
		ActualStartDate=i.get('ActualStartDate')
		ActualEndDate=i.get('ActualEndDate')
		if str(ActualStartDate) == str("null") or ActualStartDate == None: 
			ActualStartDate = ''
		ActualEndDate=i.get('ActualEndDate')
		if str(ActualEndDate) == str("null") or ActualEndDate == None: 
			ActualEndDate = ''
		WoStatus=i.get('WoStatus')
		WOCompletion=i.get('WOCompletion')
		PartNo=i.get('PartNo')
		Revision=i.get('Revision')
		UOM=i.get('UOM')
		EntName=i.get('EnterpriseName')
		EntID=i.get('EnterpriseId')
		PlantName=i.get('PlantName')
		PlantId=i.get('PlantId')
		AreaName=i.get('AreaName')
		AreaId=i.get('AreaId')
		LineName=i.get('LineName')
		LineId=i.get('LineId')
		CycleTime=i.get('Cycletime')
		Factory=i.get('Factory')
		shiftId=i.get('ShiftId')
		shift=i.get('Shift')
		stdHC=i.get('Manpower')
		actHC=i.get('ActualHeadCount')
		salesOrder=i.get('SalesOrder')		
#		shift='Shift A'
		WOType=i.get('WorkOrderType')	
		
		ViewDetails=''
		DataList=[Id,WONo,WOQty,PartNo,Revision,WOCompletion,WoStatus,WorkFlow,WorkFlowId,WorkFlowOperation,WorkFlowOperationId,StartDate,EndDate,ActualStartDate,ActualEndDate,UOM,EntName,EntID,PlantName,PlantId,AreaName,AreaId,LineName,LineId,CycleTime,shift,ViewDetails,Factory,stdHC,actHC,salesOrder,shiftId,WOType,WorkorderId]
		WODetailList.append(DataList)
	print 'API Result:-->' +str(WODetailList)
	header=['Sr No','WONo','WOQty','PartNo','Revision','WOCompletion','WoStatus','WorkFlow','WorkFlowId','WorkFlowOperation','WorkFlowOperationId','StartDate','EndDate','ActualStartDate','ActualEndDate','UOM','EntName','EntID','PlantName','PlantId','AreaName','AreaId','LineName','LineId','CycleTime','shift','ViewDetails','Factory','stdHC','actHC','salesOrder','shiftId',"WOType","WorkorderId"]
	Result = system.dataset.toDataSet(header,WODetailList)	
	return Result
	
		
				
#---------------------------------------------Line Lead BOM Details----------------------------------------------------------
def getLineLeadBOMDetails(woNo,partNo):	

	apiPath="ProductionOperatorConsole/GetAllScrapDetails/"+str(woNo)+("/")+str(partNo)
	
	
#	OperatorConsole/GetQAScrapDetails?WorkOrderNo=PE49634085&partNo=1999-1020456EP_F_JPD&Factory=JPD&Revision=F&PartNoWithoutDetails=1999-1020456EP"
	url = URLPath + apiPath
	print url
	resultData=None
	client = system.net.httpClient()
	data = client.post(url)
	
	APIResult=[]
	if data.good:
		print "Data Is Good"    
		APIResult=data.json	
	lineLeadDetails=[]
	Id=0
	

	for i in (APIResult):
		Id=Id+1
		BomName=i.get('BOMNAME')			
		ItemName=i.get('ITEMNAME')
		Revision=i.get('REVISION')	
		UOM=i.get('UOM')
		Description=i.get('DESCRIPTION')
		UnitUsage=i.get('UNITUSAGE')
		productionScrap=i.get('PRODUCTIONSCRAP')
		peaScrap=i.get('PEASCRAP')
		qualityScrap=i.get('QUALITYSCRAP')
		totalScrap=i.get('ASTOTALSCRAP')
	

		DataList=[Id,BomName,ItemName,Revision,Description,UOM,UnitUsage,productionScrap,peaScrap,qualityScrap,totalScrap]
		lineLeadDetails.append(DataList)
		
	print 'API Result:-->' +str(lineLeadDetails)
	header=['Sr No','BOM Name','Item Name','Revision','Description','UOM','Unit Usage','Production Scrap','PEA Scrap','Quality Scrap','Total Scrap']
	Result = system.dataset.toDataSet(header,lineLeadDetails)		
	return Result
	
def getAvailableComponents(WoNumber):
	apiPath = "ProductionOperatorConsole/GetAvailableComponents/"+str(WoNumber)
	url = URLPath + apiPath	
	
	resultData=None
	client = system.net.httpClient()
	
	data = client.post(url)
	
	if data.good:    
	  resultData=data.json
	
	print 'resultData',resultData 
	j=1
	dataList = []
	for i in resultData:
		SrNo = j
		componentName = i.get("Component") 
		uom = i.get("UOM")
		Revision = i.get('Revision')
						
		myList = [SrNo,componentName,uom,Revision]
		dataList.append(myList)	
		j = j+1
	headers = ["SrNo","ComponentName","UOM","Revision"]
	resultDetails = system.dataset.toDataSet(headers,dataList)	
	print"resultDetails" ,resultDetails
	return resultDetails
	
def getMoldDetailsforPDA(WoNumber,machineName):
	apiPath = "ProductionOperatorConsole/GetAttachedWorkFlowProcessComponentsWithMoldForOperatorConsole/"+str(WoNumber)+"/"+str(machineName)
	
	url = URLPath + apiPath
	
	postReturn = system.net.httpPost(url,'application/json')
	resultData= system.util.jsonDecode(postReturn)
	
	dataList = []
	k = 1
	for i in resultData:
		SrNo = k
		MoldId = i.get("MoldId")
		MoldName = i.get("MoldName")
		MoldCode = i.get("MoldCode")
		MoldLife = i.get("MoldLife")
		MoldLifeUsed = ''
		Loaded = i.get("Loaded")
		machineId = i.get('PlantHierarchyMachineId')
	
		myList = [SrNo,MoldId,MoldName,MoldCode,MoldLife,MoldLifeUsed,Loaded,machineId]
		print 'myList',myList	
		dataList.append(myList)	
		k = k+1	
		
	headers = ["SrNo","MoldId","MoldName","MoldCode","MoldLife","MoldLifeUsed","Loaded","machineId"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	print 'resultDetails',resultDetails
	return resultDetails
	
def postMoldLoadingStatus(moldId,machineId,IsLoaded,userId,workorderId):
#	apiPath = 'ProductionOperatorConsole/CreateOperatorConsoleMold/'+str(moldId)+'/'+str(WoNumber)+'/'+str(IsLoaded)+'/'+str(userId)
	apiPath = 'ProductionOperatorConsole/CreateOperatorConsoleMold/'+str(moldId)+'/'+str(machineId)+'/'+str(IsLoaded)+'/'+str(userId)+'/'+str(workorderId)
#	apiPath = 'ProductionOperatorConsole/CreateOperatorConsoleMold/'+str(moldId)+'/'+str(machineId)+'/'+str(IsLoaded)+'/'+str(userId)
		
	url = URLPath + apiPath
	print('url:')+str(url)
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json')
	except:
		result = 0
		pass
	return result
	
def postChangeoverDetails(categoryId,shiftId,userId,WoNumber,startTime,endTime,comment):
	params = {
			 "changeOvers": [
							    {
							      "categoryId": categoryId,
							      "shiftId": shiftId,
							      "loginId": userId,
							      "createdDate": "2023-01-24T08:55:44.827Z",
							      "workOrderNo":str(WoNumber),
							      "startDateTime": str(startTime),
							      "endDateTime": str(endTime),
							      "remark": str(comment)
							    }
							 ]
			}
			
	apiPath = "ProductionOperatorConsole/AddChangeOver"
	
	url = URLPath + apiPath	
	jsonParams = system.util.jsonEncode(params)
	
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
	except:		
		result = 0		
		pass
	return result
	
	
#------------------------------------------------------------Approve Lot-------------------------------------------
def ApproveLot(woNo,LotNo,PartNo,UserId):
	apiPath ="OperatorConsole/FlustLotDetailsToERP?Workorder="+str(woNo)+("&LotNumber=")+str(LotNo)+("&Partno=")+str(PartNo)+("&UserId=")+str(UserId)

	url = URLPath + apiPath	
	result = 1	
	try: 
		postReturn = system.net.httpPost(url,'application/json')		
	except:
		result=0		

	return result 
	
#------------------------------------------------------------Approve Lot-------------------------------------------
def CloseDeffect(DeffectID,PEAOkQty):
	apiPath ="OperatorConsole/ACKPEAFlag?DefectId="+str(DeffectID)+("&PEAokQty=")+str(PEAOkQty)
#	WOD00000010&PEAokQty=22
	url = URLPath + apiPath	
	result = 1	
	try: 
		postReturn = system.net.httpPost(url,'application/json')		
	except:		
		result = 0
		pass
	return result 
	

#---------------------------------------------Get Container Qty----------------------------------------------------------
def getContainerQty(woNo):	
	apiPath="ProductionOperatorConsole/getContainerQuantity/workOrderNo?workOrderNo="+str(woNo)
	url = URLPath + apiPath
#	print url
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		APIResult=data.json
		return APIResult
	else:
		return 0
		
#---------------------------------------------Container List----------------------------------------------------------
def getContaineList(LotNo,WoNo):	

	apiPath="OperatorConsole/GetProductionOperatorConsoleLotWiseContainerList?LotNumber="+str(LotNo)+("&Workorder=")+str(WoNo)
	
	
#	OperatorConsole/GetQAScrapDetails?WorkOrderNo=PE49634085&partNo=1999-1020456EP_F_JPD&Factory=JPD&Revision=F&PartNoWithoutDetails=1999-1020456EP"
	url = URLPath + apiPath
	print url
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  APIResult=data.json	
	ContainerList=[]
	Id=0
	for i in (APIResult):
		Id=Id+1
		LotNumber=i.get('LotNumber')			
		ContainerName=i.get('ContainerName')
		Qty=i.get('Qty')		
		CreatedOn=i.get('CreatedOn')
		Action=True
		DataList=[Id,LotNumber,ContainerName,Qty,CreatedOn,Action]
		ContainerList.append(DataList)
		
	print 'API Result:-->' +str(ContainerList)
	header=['Sr No','Lot No','Container Name','Production Qty','Created On','Action']
	Result = system.dataset.toDataSet(header,ContainerList)		
	return Result

#------------------------------Get Collected Qty Of Container While Approving Container----------------------------------------------
def getCollectedQtyofContainer(LotNo,woNo):
	apiPath ="OperatorConsole/GetProductionQualityQtySelectedForApproval?LotNumber="+str(LotNo)+("&Workorder=")+str(woNo)
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	return resultData
#----------------------------------------------------------------------Save Container LIst To Approve --------------------
def containerListUpdate(WoNo,ContainerName,LotNo):
 	
	apiPath="OperatorConsole/UpdateProductionOperatorConsoleLotWiseContainers"
	url = URLPath + apiPath
	writeData={
				 "cDetails": [
				    {
				      "workorderNo": WoNo,
				      "containerId": ContainerName,
				      "lotNo": LotNo
				    }
				  ]
				}
	
	jsonParams = system.util.jsonEncode(writeData)	
	print("jsonParams--->"+str(jsonParams))
	createdeffect = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
	except:		
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		return postReturn
		pass
	return createdeffect

 
def getMachineParameters(machineName):
	apiPath = 'ProductionOperatorConsole/getMachineParameter?machineName='+str(machineName)	          
	url = URLPath + apiPath

#	url = "http://172.28.3.251/FactoryMagixWebAPI/api/ProductionOperatorConsole/getMachineParameter?machineName=MD275C_002"
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	dataList = []
	j = 1

	for i in resultData:
		SrNo = j			
		MachineName = i.get('MachineName')
		ParameterId = i.get("ParameterId")
		ParameterName = i.get("ParameterName")
		ParameterDescription = i.get("ParameterDescription")
		ParameterDescriptionId = i.get('ParameterDescriptionId')
		myList = [SrNo,MachineName,ParameterId,ParameterName,ParameterDescription,ParameterDescriptionId]
		print  myList
		dataList.append(myList)	
		j = j+1

	headers = ['SrNo','MachineName','ParameterId','ParameterName','ParameterDescription','ParameterDescriptionId']
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails

def getMachineDiagnostics(machineName):
	parameterDetails = system.dataset.toPyDataSet(ProductionOperatorConsole.getMachineParameters(machineName))
	paraList= []
	j = 1
	for param in parameterDetails:
		SrNo = j
		parameterName = param["ParameterName"]
		paramDescription = param["ParameterDescription"]
		if str(paramDescription).strip() != "" and str(paramDescription).strip() != None:
			valueTagpath = defaultPath+"/"+ machineName+"/"+ parameterName
			qualityTagpath = defaultPath+"/"+ machineName+"/"+ parameterName+".Quality"
			updateDateTagpath = defaultPath+"/"+ machineName+"/"+ parameterName+".Timestamp"
			
			paramValue = str(system.tag.read(valueTagpath).value)
			if paramValue=='None':
				paramValue = str('0')
			paramQuality = str(system.tag.read(qualityTagpath).value)
			if paramQuality=='None':
				paramQuality = 'Details Not Available'
			#paramUpdateDate = str(system.tag.read(updateDateTagpath).value)
			today = system.date.now()
			paramUpdateDate = system.date.format(today, "dd-MM-yyyy HH:mm:ss")
			
			tempList = [SrNo,paramDescription,paramQuality,paramValue,paramUpdateDate]
			paraList.append(tempList)		
			
			j=j+1
		else:
			pass
	headers = ["SrNo","ParameterName","Quality","Value","LastUpdate"]
	ds = system.dataset.toDataSet(headers,paraList)
	return ds
	


def getMachineLineWise(lineID):
	try:
		scriptName='getMachineLineWise'
		apiPath = "PlantHierarchyMachine/GetPlantHierarchyMachines_OnLineChange/"+str(lineID)
		Tag1 = "machineName"
		Tag2 = "machineId"
		
		url = URLPath + apiPath
		
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData=data.json
		dataList = []
		for i in resultData:	
			Name = i.get(Tag1)
			myList = [Name] 
			dataList.append(myList)	
			
		headers = ["Name"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)	
		return None

def getClubbedWorkorders(WorkorderId):
	try:
		scriptName = "API: Get Clubbed WorkOrder List"
#		apiPath = 'ProductionOperatorConsole/GetClubbedWorkOrdersbyWoNumber/WorkOrderNo?WorkOrderNo='+str(WoNumber)
		apiPath='ProductionOperatorConsole/GetClubbedWorkOrdersbyWoNumber/WorkOrderId:int?WorkOrderId='+str(WorkorderId)
		url = URLPath + apiPath
	
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

def postParameterDescription(parameterDescriptionId,Description,userId):
	apiPath = 'ProductionOperatorConsole/AddMachineParameterDescription/'+str(parameterDescriptionId)+'/'+str(Description)+'/'+str(userId)
	
	
	url = URLPath + apiPath	
	
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json')
		print 'postReturn',postReturn
	except:		
		result = 0		
		pass
	print result
	return result
	
def GetCNSWorkOrders(WoNumber):
	try:
		scriptName = "API: Get Clubbed WorkOrder List"
		apiPath = 'ProductionOperatorConsole/GetClubbedWorkOrdersbyWoNumber/WorkOrderNo?WorkOrderNo='+str(WoNumber)
		url = URLPath + apiPath
	
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData=data.json
		dataList = []
		for i in resultData:	
			WorkOrderNo = i.get('WorkOrderNo')
			WorkorderId = i.get('WorkorderId')
			myList = [WorkorderId,WorkOrderNo] 
			dataList.append(myList)	
		
		headers = ['WorkorderId','WorkOrderNo']
		resultDetails = system.dataset.toDataSet(headers,dataList)
		print	'resultDetails'	,resultDetails
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)

def GetWorkOrderPrintPackingConfigurationsDetails(workOrderName,LabelId):	
	try:
		scriptName="API:GetWorkOrderPrintPackingConfigurationsDetails Packing"
		apiPath = "PackingPrintingConfiguration/GetWorkOrderPrintPackingConfigurationsDetails/"+str(workOrderName)+"/"+str(LabelId)
		url = URLPath + apiPath
		print url
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
#		system.perspective.print("resultData:-"+str(resultData))
		SrNo=0
		dataList = []
		for i in resultData:
			template= i['template']
			label = i['label']
#			firstPrint = i['firstPrint']
			firstPrint=''
			if firstPrint==None:
				firstPrint=''
#			number = i['number']
			number = i['LotNo']
			Type = i['label']
			ContainerCount = i['ContainerCount']
			
			SrNo=SrNo+1	
			NoOfPrint=''
			PrintHistory=''
			myList = [SrNo,number,Type,template,ContainerCount,NoOfPrint,PrintHistory]		
			dataList.append(myList)	
		if LabelId==2:
			headers = ["SrNo","Lot No","Type","Template","NoOfContainer","NoOfPrint","PrintHistory"]
		elif LabelId==3:
			headers = ["SrNo","Pallet No","Type","Template","NoOfContainer","NoOfPrint","PrintHistory"]
		else:
			pass	
		resultDetails = system.dataset.toDataSet(headers,dataList)
		resultDetails = system.dataset.toPyDataSet(resultDetails)	
		return resultDetails
	except:		
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		print errorMessage
		Authentication.exceptionLogger(errorMessage)
		return None

def GetAuthMachinesbyUserId(userId):
	apiPath = 'ProductionOperatorConsole/GetMachineByUserId/UserId?UserId='+str(userId)
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:
	  resultData=data.json
	print resultData
	return resultData
	
def GetPackingLabel():
#	URLPath = 'http://localhost:58932/api/'
	apiPath = 'ProductionOperatorConsole/GetPackingLabel'
	url = URLPath + apiPath	
	
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	print 'resultData',resultData 
	
	dataList = []
	for i in resultData:
		LabelId = i.get("LabelId")			
		LabelName = i.get("LabelName") 
		myList = [LabelId,LabelName]
		dataList.append(myList)	
	
	headers = ["LabelId","LabelName"]
	resultDetails = system.dataset.toDataSet(headers,dataList)	
	print"resultDetails" ,resultDetails
	return resultDetails

def GetMoldInfo(WoNumber,machineName):
	apiPath = "ProductionOperatorConsole/GetAttachedWorkFlowProcessComponentsWithMoldForOperatorConsole/"+str(WoNumber)+"/"+str(machineName)
	
	url = URLPath + apiPath
	
	postReturn = system.net.httpPost(url,'application/json')
	resultData= system.util.jsonDecode(postReturn)
	
	dataList = []
	for i in resultData:
		Loaded = i.get("Loaded")
		MoldId = i.get("MoldId")
		MoldName = i.get("MoldName")
		MoldCode = i.get("MoldCode")
		MoldInfo = MoldName + '-'+ MoldCode
		myList = [Loaded,MoldId,MoldInfo]
		dataList.append(myList)	
	
	headers = ["Loaded","MoldId","MoldInfo"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails
	
def GetAllRunningMachines(userId,WONO):
	apiPath = "OperatorConsole/GetOperatorConsoleWorkOrdersonInput?EnterpriseId="+str(0)+"&PlantId="+str(0)+"&AreaId="+str(0)+"&LineId="+str(0)+"&MachineId="+str(0)+"&UserId="+str(userId)	
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	print"ResultData",(resultData)
	dataList = []
	j=1
	oprList = []
	for i in resultData:			
		WoNumber = i.get("WorkOrderNo")		
		if WoNumber == WONO:	
			MachineName = i.get("MachineName")				
			myList = [MachineName] 
			if MachineName not in 	oprList:	
				dataList.append(myList)	
				oprList.append(MachineName)
			else:
				continue
	print 'dataList',dataList
	headers = ["MachineName"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails


def getQualityOperatorConsole(enterpriseID,plantID,areaID,lineID,inspectionId,paramWorkOrderNo,userId):	
	try:			
		scriptName='Quality Operator Console: - getQualityOperatorConsole'
#		print MachineId
		if str(enterpriseID).strip()==None or  str(enterpriseID).strip()=='' or  str(enterpriseID).strip()=='0':
			enterpriseID=0
		if str(plantID).strip()==None or  str(plantID).strip()=='' or  str(plantID).strip()=='0':
			plantID=0
		if str(areaID).strip()==None or  str(areaID).strip()=='' or  str(areaID).strip()=='0':
			areaID=0
		if str(lineID).strip()==None or  str(lineID).strip()=='' or  str(lineID).strip()=='0':
			lineID=0		
		if str(inspectionId).strip()==None or  str(inspectionId).strip()=='' or  str(inspectionId).strip()=='0':
			inspectionId=0		
		apiPath = "InspectionProcessManager/GetInspectionProcessManagersByMachineId/"+str(inspectionId)+"/"+str(userId)+"/"+str(lineID)+"/"+str(areaID)+"/"+str(plantID)+"/"+str(enterpriseID)
#		          "InspectionProcessManager/GetInspectionProcessManagersByMachineId/{inspectionId}/{userId}/{lineId}/{areaId}/{plantId}/{enterPriseId}
		url = URLPath + apiPath		
#		system.perspective.print("url " + str(url )) 
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		
		resultData= system.util.jsonDecode(data)
		dataList = []
		j=1
		for i in resultData:			
			ID = j
			WorkOrderNo = i.get("WorkOrderNo")
			if str(WorkOrderNo).strip() == str(paramWorkOrderNo).strip():			
				InspectionProcessName = i.get("InspectionProcessName")
				ItemId = i.get("ItemId")				
				Type = i.get("InspectionType")				
				PartNumber = i.get("PartNumber")
				StartDate = i.get("StartDate")
				CompletionDate = i.get("CompletionDate")
				Status = i.get("Status")
				LastModifiedOn = i.get("LastModifiedOn")
				LastModifiedBy = i.get("LastModifiedBy")
				View = ""
				enterpriseName = i.get("EnterpriseName")
				plantName = i.get("PlantName")
				areaName = i.get("AreaName")
				lineName = i.get("LineName")
				machineName = i.get("MachineName")
				InspectionId = i.get("InspectionId")
				MachineId = i.get("MachineId")
				Operations = i.get("Operations")
				if str(LastModifiedOn).strip()==None or str(LastModifiedOn).strip()=='None' or  str(LastModifiedOn).strip()=='' or str(LastModifiedOn).lower().strip()=='null':
					LastModifiedOn=''		
				if str(LastModifiedBy).strip()==None or  str(LastModifiedBy).strip()=='None' or str(LastModifiedBy).strip()=='' or str(LastModifiedBy).lower().strip()=='null':
					LastModifiedBy=''	
	#			LastModifiedBy=''
	#			LastModifiedOn=''
				myList = [ID,InspectionProcessName,Type,WorkOrderNo,PartNumber,StartDate,CompletionDate,Status,LastModifiedOn,LastModifiedBy,View,enterpriseName,plantName,areaName,lineName,machineName,InspectionId,MachineId,Operations,ItemId] 		
				dataList.append(myList)	
				j = j+1
				break
			else:
				pass
			
		headers = ["SRNO","InspectionProcessName","Type","WorkOrderNo","PartNumber","StartDate","CompletionDate","Status","LastModifiedOn","LastModifiedBy","View_Details","EnterpriseName","PlantName","AreaName","LineName","MachineName","InspectionId","MachineId","Operations","ItemId"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		print"resultDetails",resultDetails
		return resultDetails 
	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print("errorMessage" + str(errorMessage))
		print"errorMessage",errorMessage	
		return None
	
		


	
def componentCheckValidation(WOType,workflowId,WoNumber,userId):
		try:
			scriptName = 'Validation'
			if str(WOType) == str('1') or str(WOType) == str('2'):
				WONO =WoNumber
				OperationList=ProductionOperatorConsole.getOperationsForComponentView(userId,WoNumber)
				print("OperationList" + str(OperationList))
				OperationListCount = OperationList.getRowCount()
				FalseCount= []
				TrueCount = []
				componentFlag = 0
				for i in range(OperationListCount):
					if componentFlag ==0:
						print 'IN Loop' , componentFlag
						selectedWoNumberId	=OperationList.getValueAt(i, "WorkOrderId")
						print("selectedWoNumberId" + str(selectedWoNumberId))
						operationId=OperationList.getValueAt(i, "OperationId")
						print("operationId" + str(operationId))
						ScanComponentTableDetails = PDAComponentScanning.getSubstitueComponentDetails(selectedWoNumberId,operationId)
					   	isTableEmpty = ScanComponentTableDetails.getRowCount()	
					   	isTableEmpty=int(isTableEmpty)
					   	print("isTableEmpty--->"+str(isTableEmpty))
						if isTableEmpty>0:
							for i in range(isTableEmpty):
								ConsumeQty = ScanComponentTableDetails.getColumnAsList(4)
								print("ConsumeQty" + str(ConsumeQty))
								zeroCount = ConsumeQty.count(0)
								blankCount = ConsumeQty.count(str("").strip())
								nullCount = ConsumeQty.count(str("Null").strip())
								if int(zeroCount) > int(0) or blankCount > 0 or  nullCount > 0:
									print 'Validation Fail'
									componentFlag = 1
									break
						else:
							print True
							componentFlag = 0
							
				print 'Out Loop' , componentFlag
				if str(componentFlag) == '1':
					validation = False  #Failed in vgetSubstitueComponentDetailsalidation
				else:
					validation =  True
				print 'validation',validation
				return validation
			else:
				return True
		except:		
			import sys, os
			errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
			Authentication.exceptionLogger(errorMessage)
			print("errorMessage" + str(errorMessage))
			print"errorMessage",errorMessage	
			return None	
			
#----------------------------------Component Validation For Testing -------------------
def componentValidationTesting(WOType,workflowId,WoNumber,userId):
	try:
		scriptName = 'Validation'
		if str(WOType) == str('1') or str(WOType) == str('2'):
			WONO =WoNumber
			OperationList=ProductionOperatorConsole.getOperationsForComponentView(userId,WoNumber)
			print("OperationList" + str(OperationList))
			OperationListCount = OperationList.getRowCount()
			FalseCount= []
			TrueCount = []
			IsComponent = 0
			componentFlag = 0
			isFailConsumedQty=0
			for i in range(OperationListCount):
				if componentFlag ==0:
					print 'IN Loop' , componentFlag
					selectedWoNumberId	=OperationList.getValueAt(i, "WorkOrderId")
					print("selectedWoNumberId" + str(selectedWoNumberId))
					operationId=OperationList.getValueAt(i, "OperationId")
					print("operationId" + str(operationId))
					ScanComponentTableDetails = PDAComponentScanning.getSubstitueComponentDetails(selectedWoNumberId,operationId)
					isTableEmpty = ScanComponentTableDetails.getRowCount()	
					
					isTableEmpty=int(isTableEmpty)
					print("isTableEmpty--->"+str(isTableEmpty))
					if isTableEmpty>0:
						for i in range(isTableEmpty):
							IsComponent = IsComponent +1
							ConsumedQty1=ScanComponentTableDetails.getValueAt(i,'consumeQty')
							if str(ConsumedQty1) ==None or str(ConsumedQty1).strip()=='':
								ConsumedQty1=0
									
							ConsumedQty=int(ConsumedQty1)
							print("ConsumeQty" + str(ConsumedQty))
							if ConsumedQty>0:		
								pass
							else:
								isFailConsumedQty=1
								break
					else:
#						isFailConsumedQty=1
						print"Part Not Available"
			if IsComponent == 0:
				return True
			else:
#			if IsComponent >0:
				if isFailConsumedQty==1:
					print 'Validation Failed'
					return False
				else:
					print 'Validation Pass'
					return True
								

	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)				
		Authentication.exceptionLogger(errorMessage)
		print("errorMessage" + str(errorMessage))
		print"errorMessage",errorMessage			
		return None				
			
			
	#-----------------------------------------Get Mold Life------------------------------		
def getMoldLife(woNo,MachineName,MoldCode1):
	apiPath = 'ProductionOperatorConsole/GetAttachedWorkFlowProcessComponentsWithMoldForOperatorConsole/'+str(woNo)+('/')+str(MachineName)
	
	url = URLPath + apiPath
	print url
	resultData=None
	client = system.net.httpClient()
	data = client.post(url)
#	print data
	if data.good:    
		resultData=data.json
		print 'ResultData :'+str(resultData)
#	ActualLife=0
	dataList = []
	for i in (resultData):	
		MoldName = i.get("MoldName")
		MoldCode = str(i.get("MoldCode"))
		if MoldCode1==MoldCode:		
			ActualLife = i.get("ActualLife")
			print 'MoldCode1--->'+str(MoldCode1)
			print 'ActualLife--->'+str(ActualLife)
			return ActualLife
		else:
			print 'Moldcode not Matching'
			pass						
	
	
def getAllMachineLoadedMoldData(WoNumber,machineIdList,machineNameList):
	dataList = []
	j=0
#	machineNameList = ["BA_H01_0050_0011","BA_H01_0050_0012"]
	for i in machineIdList:
		moldData = WorkOrderDetailsAPI.getLoadedMoldDetails1(WoNumber,i,machineNameList[j])
		dataList = dataList + moldData
		j = j+1	
	header = ["MoldCode","cavity","productPiece","MaxLife","MachineId","MachineName","MachineShots"]
	resultDetails = system.dataset.toDataSet(header,dataList)	
	return resultDetails	
	

def GetReasonTypeForOperator(ReasonType):
	apiPath = 'OperatorConsole/GetNameCodeForDefectedWorkorder?type='+str(ReasonType)
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:
	  resultData=data.json
	print resultData
	return resultData
	
def getOperationsForComponentView(userId,WONO):	
 	apiPath = "OperatorConsole/GetOperatorConsoleWorkOrdersonInput?EnterpriseId="+str(0)+"&PlantId="+str(0)+"&AreaId="+str(0)+"&LineId="+str(0)+"&MachineId="+str(0)+"&UserId="+str(userId)	
	url = URLPath + apiPath
	resultData=None
	system.perspective.print("API URL is: "+str(url))
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
#	print"ResultData",(resultData)
	dataList = []
	j=1
	oprList = []
	for i in resultData:			
		WoNumber = i.get("WorkOrderNo")		
		if WoNumber == WONO:	
			Operation = i.get("Operations")
			WorkOrderId = i.get("WorkOrderId")
			OperationId = i.get("OperationId")
			myList = [WorkOrderId,OperationId,Operation] 
			if Operation not in oprList:	
				dataList.append(myList)	
				oprList.append(Operation)
			else:
				continue
	print 'dataList',dataList
	headers = ["WorkOrderId","OperationId","Operation"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails
	
	
def UpdateWoOperationStatus(WorkOrderId,IsClubbed,UserId,WorkOrderStatusId,ScanBadge,HoldReasonCodeId,Comment,lineId):
	params = {
			  "workOrderId": WorkOrderId,
			  "isClubbed": IsClubbed,
			  "param1": 0,
			  "param2": "",
			  "comment": Comment,
			  "userId": UserId,
			  "workOrderStatusId": WorkOrderStatusId,
			  "scanBadge": ScanBadge,
			  "holdReasonCodeId": HoldReasonCodeId,
			  "isLineLead": False,
			  "lineId": lineId
			}
			
	apiPath = "OperatorConsole/UpdateWorkOrderOperations"
	
	url = URLPath + apiPath	
	jsonParams = system.util.jsonEncode(params)
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API InputData is: "+str(jsonParams))
		system.perspective.print("API Method is: Post ")
	except:
		pass
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
	except:		
		result = 0		
		pass
	return result
	
	
def WorkorderValidation(WorkorderId):
	try:	
	 	apiPath = "OperatorConsole/ValidateWorkorder?WorkorderId="+str(WorkorderId)	
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData=data.json
	
	
		return resultData
	except:
			
			exc_type, exc_obj,tb = sys.exc_info()
			errorMessage = "Error:"+ str(exc_obj)			
			lineno = tb.tb_lineno
			print("Script Exception: Workorder Validation")
			print(errorMessage)
			print(lineno)			
			system.perspective.print("Script Exception: Workorder Validation")
			system.perspective.print(errorMessage)
			system.perspective.print(lineno)
			
#------------------------------------------------------------------------------------------
# Application use: Operator Console Workorder Start Stop Validation		
# Developer Name: Sushant Chavan
# Created On: 18-03-2023
# Updated By : 
# Updated On :	

def validateWorkorderParameters(WorkorderId):		
	apiPath = "OperatorConsole/ValidateWorkorder?WorkorderId="+str(WorkorderId)	
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData=data.json
	if resultData:
		for i in resultData:
			IsMachineRunning = i.get('IsMachineRunning')
			IsComponentValid = i.get('IsComponentValid')
#			IsComponentValid=False
			IsAllCheckListChecked = i.get('IsAllCheckListChecked')	
			IsMoldLoadedValidation = i.get('IsMoldValid')
		return IsMachineRunning,IsComponentValid,IsAllCheckListChecked,IsMoldLoadedValidation	
#		return IsMachineRunning,IsComponentValid,IsAllCheckListChecked
	else:
		return False,False,False,False

#------------------------------------------------------------------------------------------
# Application use: Operator Console Operation List Dropdowns at Checklist,Machine Details,ets	
# Developer Name: Sushant Chavan
# Created On: 18-03-2023
# Updated By : 
# Updated On :		
def getOperationListbyWO(WorkorderId,UserId):
	apiPath = 'OperatorConsole/GetWorkflowOperationsByWorkOrder?WorkorderId='+str(WorkorderId)+'&UserId='+str(UserId)	
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData=data.json
	operationList=[]
	for i in resultData:
		id = i.get('operationID')
		operationName = i.get('Operations')
		templist = [operationName]
		operationList.append(templist)	
	header = ["Operation"]
	resultDetails = system.dataset.toDataSet(header,operationList)	
	return resultDetails

#------------------------------------------------------------------------------------------
# Application use: This function is used to get Operation List along with Operation Id. Its replica above function. Used in Checklist table Onclik property.	
# Developer Name: Sushant Chavan
# Created On: 18-03-2023
# Updated By : 
# Updated On :		
def getOperationListWithIdForWO(WorkorderId,UserId):
	apiPath = 'OperatorConsole/GetWorkflowOperationsByWorkOrder?WorkorderId='+str(WorkorderId)+'&UserId='+str(UserId)	
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData=data.json
	operationList=[]
	for i in resultData:
		id = i.get('operationID')
		operationName = i.get('Operations')
		templist = [id,operationName]
		operationList.append(templist)	
	header = ["Id","Operation"]
	resultDetails = system.dataset.toDataSet(header,operationList)	
	return operationList

#------------------------------------------------------------------------------------------
	# Application use: Production Operator Console Machine Details	(MachineOk Qty, Machine NOT OK Qty as per workorderId)
	# Developer Name: Sushant Chavan
	# Created On: 30-03-2023
	# Updated By : 
	# Updated On :		
def getMachineDetailsFromWorkorderId(WorkorderId):
#	apiPath = 'ProductionOperatorConsole/WorkorderMachineDetails/ID:int?ID='+str(WorkorderId)
	apiPath='ProductionOperatorConsole/WorkorderMachineDetails/WorkOrderId:int?WorkOrderId='+str(WorkorderId)
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	print('Data: ')+str(data)
	if data.good:    
		resultData=data.json
		print resultData
	operationList=[]
	j=1
	for i in resultData:
		SrNo = j
		MachineName = i.get('MachineName')
		
#		GoodQtyTagPath = defaultPath + MachineName + "/GoodQty"
#		MachineOkCOUNT = system.tag.read(GoodQtyTagPath).value
#		NGQtyTagPath = defaultPath + MachineName + "/NGQty"
#		MachineNGCOUNT = system.tag.read(NGQtyTagPath).value
#		MachineStatusTagPath = defaultPath + MachineName + "/MachineStatus"
#		MCStatus = int(system.tag.read(MachineStatusTagPath).value)	
			
		MachineOkCOUNT = i.get('MachineOkCOUNT')
		MachineNGCOUNT = i.get('MachineNGCOUNT')
		MCStatus = int(i.get('MachineStatus'))
		
		if MCStatus == 0 :
			MachineStatus = "Network Disconnected"
		elif MCStatus == 1 :
			MachineStatus = "Running"
		elif MCStatus == 2:
			MachineStatus = "Manual"
		elif MCStatus == 4:
			MachineStatus = "Idle"
		elif MCStatus == 5:
			MachineStatus = "Alert"
		templist = [SrNo,MachineName,MachineOkCOUNT,MachineNGCOUNT,MachineStatus]
		operationList.append(templist)	
		j = j+1
	header = ["SrNo","MachineName","MachineOkCOUNT","MachineNGCOUNT","MachineStatus"]
	resultDetails = system.dataset.toDataSet(header,operationList)	
	return resultDetails	
		
	
	
#------------------------------------------------------------------------------------------
	# Application use: Machine Disconnection alarm Filtering string
	# Developer Name: Sushant Chavan
	# Created On: 31-03-2023
	# Updated By : 
	# Updated On :		
def getMachinesStringFromWorkorderId(WorkorderId):
	apiPath = 'ProductionOperatorConsole/WorkorderMachineDetails/WorkOrderId:int?WorkOrderId='+str(WorkorderId)			   
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData=data.json		
	MachineString = ''
	if resultData:
		for i in resultData:
			MachineName = i.get('MachineName')
			if MachineString=='':
				MachineString = '*'+str(MachineName)+'*'
			else:
				MachineString = MachineString + ',*' + MachineName+'*'
		return str(MachineString)	
	else:
		return 0
#		
#		getMoldDetailsforPDA

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Application use: Get The List of running workorder to restrict the loading & Unloading Mold
	# Developer Name: Hari Mhasalekar
	# Created On: 27/04/2023
	# Updated By : 
	# Updated On :	
def GetListofrunnigWo(LineId,WorkorderNo):
	apiPath = "ProductionOperatorConsole/GetWorkOrderByLineId/LineId:int?LineId="+str(LineId)
	url = URLPath + apiPath
	WorkorderNo=str(WorkorderNo)
	worlorderisinprogress=0
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	ListOfrunningWo=[]
	if data.good:    
		resultData=data.json		
	MachineString = ''
	if resultData:
		for i in resultData:
			WorkOrderStatusId = i.get('WorkOrderStatusId')
			if WorkOrderStatusId==1:
				MfgOrderName = i.get('MfgOrderName')
				if MfgOrderName==WorkorderNo:
					worlorderisinprogress=1
					break
			else:
				worlorderisinprogress= 0
		if worlorderisinprogress==1:
			return 0
		else:
			return 1
	else:
		return 0
		

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Application use: Get The List of running workorder to restrict the loading & Unloading Mold
	# Developer Name: Hari Mhasalekar
	# Created On: 27/04/2023
	# Updated By : 
	# Updated On :	
def GetValidMoldForMachine(WorkorderNo, MachineId):
	apiPath = "ProductionOperatorConsole/GetMoldValidation/"+str(MachineId)+str("/")+str(WorkorderNo)
	url = URLPath + apiPath	
	resultData = None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData = data.json		
		return resultData
	else:
		return []
	
		
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Application use: Get the PM Tool Details
	# Developer Name: Hari Mhasalekar
	# Created On: 22/05/2023
	# Updated By : 
	# Updated On :	
def GetPMToolDetails(ToolCode):
	apiPath = "ProductionOperatorConsole/GetPMToolDetails/"+str(ToolCode)
	url = URLPath + apiPath	
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData=data.json		
		return resultData
	else:
		return []
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Application use: Get the PM MAchine Details
	# Developer Name: Hari Mhasalekar
	# Created On: 24/05/2023
	# Updated By : 
	# Updated On :	
def GetPMMachineDetails(EquipmentCode):
	apiPath = "ProductionOperatorConsole/GetPMMachineDetails/"+str(EquipmentCode)
#	
	url = URLPath + apiPath	
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData=data.json		
		return resultData
	else:
		return []


#---------------------------------------------------------------------- Other Tool Loading and Unloading --------------------------
# Application use: Get Tool List for Loading/Unloading Tool from Machine using PDA .Used in PDA Tool Dropdown.
# Developer Name: Sushant Chavan
# Created On: 23/05/2023
# Updated By : 
# Updated On :	
def getToolListDropDown(MachineName,UserId):
	apiPath = "ProductionOperatorConsole/getLinkedToolMachineList/"+str(MachineName)
	url = URLPath + apiPath	
	resultData = None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData = data.json			
	else:
		return []
	dataList = []
	for i in resultData:		
		IsLoaded = i.get('isLoaded')
		ToolId = i.get('ToolId')
		ToolCode = i.get('ToolCode')
		tempList = [IsLoaded,ToolId,ToolCode]
		dataList.append(tempList)
		print tempList
	header = ["IsLoaded","ToolId","ToolCode"]
	resultDetails = system.dataset.toDataSet(header,dataList)	
	return resultDetails
#-------------------------------------	
# Application use: Get Tool Details for Loading/Unloading Tool from Machine using PDA 
# Developer Name: Sushant Chavan
# Created On: 24/05/2023
# Updated By : 
# Updated On :	
def getToolLoadingUnloadingDetails(MachineName):
	apiPath = "ProductionOperatorConsole/getLinkedToolMachineList/"+str(MachineName)
	url = URLPath + apiPath	
	resultData = None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData = data.json			
	else:
		return []
	dataList = []
	for i in resultData:
		machineId = i.get('MachineId')
		equipmentCode = i.get('EquipmentCode')
		isLoaded = i.get('isLoaded')
		ToolName = i.get('ToolName')
		ToolId = i.get('ToolId')
		ToolCode = i.get('ToolCode')
		tempList = [machineId,equipmentCode,isLoaded,ToolName,ToolId,ToolCode]
		dataList.append(tempList)
		print tempList
	header = ["MachineId","EquipmentCode","IsLoaded","ToolName","ToolId","ToolCode"]
	resultDetails = system.dataset.toDataSet(header,dataList)	
	return resultDetails				
#---------------------------------------------------------------------- End  -----------------------------------------------------	



def IsMaintenanceOrderPresent(MachineToolId,MaintenanceTypeId):
		try:
	#		apiPath = "ProductionOperatorConsole/CheckRMOrder/machineId:int?machineId="+str(machineId)
			apiPath = "ProductionOperatorConsole/CheckAvailableMaintenanceOrdersByMachineToolId/"+str(MachineToolId)+"/"+str(MaintenanceTypeId)
		  	url = URLPath + apiPath
		  	resultData=None
		  	client = system.net.httpClient()
		   	data = client.get(url)
		  	
		  	if data.good:
		  	  resultData=data.json
		  	print resultData
		  	
		  	
		  	for i in resultData:
		  		IsRMAvailable = i.get("IsAvailable")
		  		WorkOrderNo = i.get("WorkOrderNo")
		  		MaintenanceType = i.get("MaintenanceType")
		  		myList = [IsRMAvailable,WorkOrderNo,MaintenanceType] 		
		  		break
		  	return myList 
		except:
			import sys, os
			errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
			Authentication.exceptionLogger(errorMessage)
			print errorMessage
			return 0 
			
 #---------------------Edit Delet Defect-----------------------------	
  
def EditDeleteProductionDefect(DefectId,DefectQty,ReasonId,Comment,Action):
		params = {
				  "defectId": DefectId,
				  "defectQty": DefectQty,
				  "reasonCodeId": ReasonId,
				  "comments": Comment,
				  "action": Action
				}
				
		apiPath = "ProductionOperatorConsole/EditDeleteProductionDefect"
		
		url = URLPath + apiPath	
		jsonParams = system.util.jsonEncode(params)
		
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
			system.perspective.print("jsonParams: "+str(jsonParams))
		except:		
			result = 0		
			pass
		return result
		
#----------------------------------------------------------------------Get Running Workorders agains Machine--------------------
def CheckforRunningWos(Machindid):
	apiPath="ProductionOperatorConsole/WorkOrderDetailsForMachine/"+str(Machindid)
	url = URLPath + apiPath
	#system.perspective.print("API URL:"+str(url))
	#print url
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	return resultData	 
	

def GetCavityPieces(WorkOrderId,LotNo):
	params = {
				  "workOrderId": WorkOrderId,
				  "lotNo": LotNo
			}
			
	apiPath = "ProductionOperatorConsole/GetProductPiecesForLL"
	
	url = URLPath + apiPath	
	jsonParams = system.util.jsonEncode(params)
	print (jsonParams)
#	result = 1
	postReturn = system.net.httpPost(url,'application/json',jsonParams)
	decodedData = system.util.jsonDecode(postReturn)	
	return decodedData

#-----------------------------------------------------------------------------------------	
def updateMESControls(workorderId):
	#---------------------------------------------
	apiPath = "ProductionOperatorConsole/GetMESControlMachinesDetails/WorkOrderId:int?WorkOrderId="+str(workorderId)		
	url = URLPath + apiPath
	resultData = None
	client = system.net.httpClient()
	data = client.get(url)

	if data.good:    
		resultData = data.json

	dataList = []	
	print'moldDetails API Result'+str(resultData)	
	SrNo=0
	MachineValidationOkList = []
	if 	resultData:
		for i in resultData:
			machineName = i.get("MachineName")	
			MachineId = i.get("MachineId")	
			print("machineName :- " +str(machineName))		
			defaultTagPath = system.tag.read("[default]JMES_InternalTags/DafaultTagPath.value").value	
			mesMsgTagPath = defaultTagPath + machineName + "/MESMessage.value"
			MESOnOffTagPath = str(defaultTagPath)+str(machineName)+"/MESOnOff.value"					
			MESOnOff = system.tag.read(MESOnOffTagPath).value	
			MESControlTagPath = str(defaultTagPath)+str(machineName)+"/MESControl.value"
			print("MESOnOff :- " +str(MESOnOff))	
			if 	MESOnOff==1 or MESOnOff==True:	
				isTool = i.get("IsTool")			
				if isTool==0 or isTool==False:
					isComponentFeed = 0	
					isMoldLoaded = 0		
					
					isComponentFeed = i.get("ComponentValidation")	
					if isComponentFeed == None:
						isComponentFeed = 0			
					isMoldLoaded = i.get("MoldValidation")	
	
					IsRMActive = i.get("IsRMActive")	
					RMWorkorderName = i.get("RMWorkorderName")
					
					IsPMActive = i.get("IsRMActive")	
					PMWorkorderName = i.get("RMWorkorderName")	
									
					machineStatusTagPath = str(defaultTagPath)+str(machineName)+"/MachineStatus.value"
					machineStatus = system.tag.read(machineStatusTagPath).value
					machineRepairTagPath = str(defaultTagPath)+str(machineName)+"/Repair.value"					
					machineRepair = system.tag.read(machineRepairTagPath).value					
					print("machineStatus :- " +str(machineStatus))
					print("machineRepair :- " +str(machineRepair))
					print("isComponentFeed :- " +str(isComponentFeed))
					print("isMoldLoaded :- " +str(isMoldLoaded))
					
					
					if (machineStatus==5):		
						system.tag.writeAsync(MESControlTagPath,2)
						print("MESControlTag :- 2")
						system.tag.writeAsync(mesMsgTagPath,"Machine is in Alert Mode.")
						print("Machine is in Alert Mode.")
					elif (machineRepair==2):
						system.tag.writeAsync(MESControlTagPath,2)
						print("MESControlTag :- 2")
						system.tag.writeAsync(mesMsgTagPath,"Machine is in Rapair Mode.")	
						print("Machine is in Rapair Mode.")
					elif isComponentFeed == 0 or isComponentFeed == False:	
						system.tag.writeAsync(MESControlTagPath,2)
						print("MESControlTag :- 2")			
						system.tag.writeAsync(mesMsgTagPath,"Component Validations is Not OK")	
						print("Component Validations Are Not OK")
					elif isMoldLoaded == 0:	
						system.tag.writeAsync(MESControlTagPath,2)
						print("MESControlTag :- 2")			
						system.tag.writeAsync(mesMsgTagPath,"Mold Valodation Not Ok")	
						print("Mold Validations Are Not Ok")
		#----------------------------------------------------------					
					elif IsRMActive == 1 or IsRMActive == True:	
						system.tag.writeAsync(MESControlTagPath,2)
						print("MESControlTag :- 2")			
						system.tag.writeAsync(mesMsgTagPath,"There is active RM on Machine - "+str(RMWorkorderName))					
						print("There is active RM on Machine - "+str(RMWorkorderName))					
					elif IsPMActive == 1 or IsPMActive == True:	
						system.tag.writeAsync(MESControlTagPath,2)
						print("MESControlTag :- 2")			
						system.tag.writeAsync(mesMsgTagPath,"There is active RM on Machine - "+str(RMWorkorderName))	
						print("There is active RM on Machine - "+str(RMWorkorderName))	
					
		#----------------------------------------------------------						
					else:
						system.tag.writeAsync(MESControlTagPath,1)
						print("MESControlTag :- 1")
						system.tag.writeAsync(mesMsgTagPath,"Validations Are OK")
						print("Validations Are OK")	
						MachineValidationOkList.append(MachineId)
						print MachineValidationOkList
				else:
					print("Its not machine its a Tool")	
					
					ToolName = i.get("ToolName")					
					ToolId = i.get("ToolId")
					
					IsRMActive = i.get("IsRMActive")	
					RMWorkorderName = i.get("RMWorkorderName")
					
					IsPMActive = i.get("IsRMActive")	
					PMWorkorderName = i.get("RMWorkorderName")
					
					IsLifeExpired = i.get("IsLifeExpired")	
					ACTMachineToolLife = i.get("ACTMachineToolLife")
					print MachineValidationOkList
					if MachineId in MachineValidationOkList:				
						if IsRMActive == 1 or IsRMActive == True:	
							system.tag.writeAsync(MESControlTagPath,2)
							print("MESControlTag :- 2")			
							system.tag.writeAsync(mesMsgTagPath,"There is active RM on Loaded Tool - "+str(RMWorkorderName))					
							print("There is active RM on Machine - "+str(RMWorkorderName))					
						elif IsPMActive == 1 or IsPMActive == True:	
							system.tag.writeAsync(MESControlTagPath,2)
							print("MESControlTag :- 2")			
							system.tag.writeAsync(mesMsgTagPath,"There is active RM on Loaded Tool - "+str(RMWorkorderName))	
							print("There is active RM on Machine - "+str(RMWorkorderName))	
						elif IsLifeExpired == 1 or IsLifeExpired == True:	
							system.tag.writeAsync(MESControlTagPath,2)
							print("MESControlTag :- 2")			
							system.tag.writeAsync(mesMsgTagPath,"Tool Life is expired - "+str(ACTMachineToolLife))	
							print("Tool ("+str(ToolName)+") Life is expired - "+str(ACTMachineToolLife))
						else:
							system.tag.writeAsync(MESControlTagPath,1)
							print("MESControlTag :- 1")
							system.tag.writeAsync(mesMsgTagPath,"Validations Are OK")
							print("Validations Are OK")	
					else:
						print("Need to clear Machine validations first")	
			else :
				print("Not Applicable")
				mesMsgTagPath = defaultTagPath + machineName + "/MESMessage.value"
				system.tag.writeAsync(mesMsgTagPath,"Not Applicable")	

def QtyValidation(LineId):
	apiPath="PlantHierarchyLine/GetLine/"+str(LineId)
	url = URLPath + apiPath

	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	  
	QtyValidation = resultData.get('isQuantityValidation')
	print QtyValidation
	if QtyValidation==True or QtyValidation=='True' or QtyValidation=='true' or QtyValidation ==1:
		return 1
	else:
		return 0

def GetReasonTypeForOperatorLineWise(ReasonType,LineId):
	try:
		scriptName = "API: Get GetReasonTypeForOperatorLineWise"
		system.perspective.print("ReasonType  "+str(ReasonType))
		system.perspective.print("LineId "+str(LineId))
		apiPath = 'OperatorConsole/GetNameCodeForDefectedWorkorderLineWise?type='+str(ReasonType)+"&LineId="+str(LineId)	
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:
		  resultData=data.json
		print resultData
		return resultData
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print("errorMessage "+str(errorMessage))
		print 	errorMessage
		return None	


def getProductionQualityCheck(WorkorderId):
	try:
		scriptName = "API: Get getProductionQualityCheck"
		apiPath = 'ProductionOperatorConsole/CheckProductionCharacteristicCompleted/'+str(WorkorderId)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:
		  resultData=data.json
	  	for i in resultData:			
	  		canCompleteWO = i.get("canCompleteWO")
	  		break

		return canCompleteWO
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print("errorMessage "+str(errorMessage))
		print 	errorMessage
		return None	


def UpdateConsumableMaterialForWorkOrder(selectedLineId,selectedWorkorderId,UserId):
	try:
		apiPath = "OperatorConsole/UpdateConsumableMaterialForWorkOrder"
		url = URLPath + apiPath
		params = {
		   		  "workOrderId": selectedWorkorderId,
		   		  "lineID": selectedLineId,
#		   		  "isClubbed": true,
#		   		  "param1": 0,
#		   		  "param2": "string",
#		   		  "comment": "string",
		   		  "userId": UserId
#		   		  "workOrderStatusId": 0,
#		   		  "scanBadge": "string",
#		   		  "holdReasonCodeId": 0,
#		   		  "isLineLead": true
		   		}
		
		jsonParams = system.util.jsonEncode(params)			 
		result = 1
		system.perspective.print('jsonParams  UpdateConsumableMaterialForWorkOrder : ' + str(jsonParams))
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)	
		except:
			import sys, os
			exc_type, exc_obj,tb = sys.exc_info()
			lineno = tb.tb_lineno
			errorMessage = "'Exception :: PDA :: Post Return :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
			Authentication.exceptionLogger(errorMessage)
			result =0
			pass

		resultData = system.util.jsonDecode(postReturn)
		DataToGetDetails =resultData[0]
		IsValid =DataToGetDetails['IsValid']
		return IsValid
	except:
		IsValid = 0
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: POC :: UpdateConsumableMaterialForWorkOrder :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)

def addShopNotes(WorkflowOperationsId,WoNumber,txtNotes,userID):
	try:
		apiPath = "OperatorConsole/CreateNotes"
		url = URLPath + apiPath	
		writeData = {
		  "isActive": True,
		  "createdBy": userID,
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
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: POC :: Add Shop Notes :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		
		
def GetOPRInfo1():

    #apiPath="ProductionSummary/GetOperatorRoleUsers/"+str(enterpriseID)+"/"+str(plantID)+"/"+str(WorkOrderId)+"/"+str(ShiftId)
    #apiPath = "OperatorInfo/GetOperatorInfo/"+str(enterpriseID)
    #url ="http://elephant040001/JEMESWebAPIZAC/api/Authorization/GetRoles" #URLPath + apiPath
    apiPath = "Authorization/GetRoles"
    url = URLPath + apiPath
    print url
    try:
		#system.perspective.print("API URL is: "+str(url))
		#system.perspective.print("API Method is: Get ")

		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		return resultData
    except Exception as e:
        return e
		