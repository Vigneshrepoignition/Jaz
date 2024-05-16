import re
import json
import urllib2, urllib
import datetime
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
defaultPath=system.tag.read("[default]JMES_InternalTags/DafaultTagPath").value
	
#-----------------------------------------------------Get Machine Details for Take- In ---------------------------------
	# Application use: WorkOrder Machine Take-In 
	# Developer Name: Hari Mhasalekar
	# Created On: 10th April 2023
	# Updated By : Sushant Chavan
	# Updated On : 17-04-2023
	
def getMachineListForTakeIn(workorderId):	
	apiPath = "Workflow/GetListOfMachinesForTakeIn?workorderID="+str(workorderId)		
	url = URLPath + apiPath
	resultData = None
	client = system.net.httpClient()
	data = client.get(url)

	if data.good:    
		resultData = data.json

	dataList = []	
	print'moldDetails API Result'+str(resultData)	
	SrNo=0
	for i in resultData:			
		Operation = i.get("OperationName")
		OperationId = i.get("OperationId")
		EquipmentCode = i.get("MachineName")
		MachineId = i.get("MachineID")
		machineStatus=''
		IsSelect = i.get("isSelected")

		SrNo = SrNo + 1								
		myList = [SrNo,Operation,OperationId,EquipmentCode,MachineId,machineStatus,IsSelect] 		
		dataList.append(myList)								
	headers = ["Sr No","Operation","OperationId","Machine Name","MachineId","Machine Status","IsSelect"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails
	
#-----------------------------------------------------Get Machine Details for Take- Out --------------------------------
	# Application use: WorkOrder Machine Take Out
	# Developer Name: Hari Mhasalekar
	# Created On: 10th April 2023
	# Updated By : Sushant Chavan
	# Updated On : 17-04-2023
	
def getMachineListForTakeOut(workorderId):	
	apiPath = "Workflow/GetListOfMachinesForTakeOut?workorderID="+str(workorderId)		
	url = URLPath + apiPath
	resultData = None
	client = system.net.httpClient()
	data = client.get(url)

	if data.good:    
	  resultData = data.json
	dataList = []	
	print'moldDetails API Result'+str(resultData)	
	SrNo = 0
	for i in resultData:			
		Operation = i.get("OperationName")
		OperationId = i.get("OperationId")
		EquipmentCode = i.get("MachineName")
		MachineId = i.get("MachineID")
		machineStatus=''
		IsSelect = i.get("isSelected")
#		if IsSelectFlag==1:
#			IsSelect = 0
#		else:
#			IsSelect = 1
		SrNo = SrNo + 1								
		myList = [SrNo,Operation,OperationId,EquipmentCode,MachineId,machineStatus,IsSelect] 		
		dataList.append(myList)								
	headers = ["Sr No","Operation","OperationId","Machine Name","MachineId","Machine Status","IsSelect"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails
	

#------------------------------ Update Machine TakeIn - TakeOut ----------------------------------------------
	# Application use: WorkOrder Machine Take Out
	# Developer Name: Hari Mhasalekar
	# Created On: 10th April 2023
	# Updated By : Sushant Chavan
	# Updated On : 17-04-2023
def postMachineTakeIn_OutDetails(workorderId,jsonParams,isTakeInFlag,statusFlag,userId):
	try:
		apiPath = "Workflow/AddUpdateTakeInTakeOutMachine"		
		url = URLPath + apiPath	
		print url	
		writeData = {
					  "workOrderId": workorderId,
					  "isTakeInFlag": isTakeInFlag,
					  "selectedMachines": jsonParams,
					  "statusFlag": statusFlag,	
					  "userId": userId				  			  
					}							
		params = system.util.jsonEncode(writeData)	
		postResult = system.net.httpPost(url,'application/json',params)
		return 1
	except:	
		return 0


#------------------------------ Update Machine TakeIn - TakeOut ----------------------------------------------
	# Application use: 
	# Developer Name: 
	# Created On: 
	# Updated By : Sushant Chavan
	# Updated On : 
def TITOLoadedMaterialValidation(workorderId,jsonParams,userId):
	apiPath = "ProductionOperatorConsole/TITOLoadedMaterialValidation"		
	url = URLPath + apiPath	
	writeData = {
				  "workOrderId": workorderId,				  		
				  "userId": userId,
				  "machineList": jsonParams				  			  
				}
	try:									
		params = system.util.jsonEncode(writeData)	
		print (params)
		resultData = system.net.httpPost(url,'application/json',params)
		decodedData = system.util.jsonDecode(resultData)		
		machineList = []
		TITIValidationFlag = []
		MaterialLoadedFlag = 0	
		for row in decodedData:
			remainingQty =  row.get("RemainLotQuantity")
			QualityContainerValidation =  row.get("QualityContainerValidation")
			LLContainerValidation =  row.get("LLContainerValidation")
			RemainingQTYValidation =  row.get("RemainingQTYValidation")
			MachineRemainingCheck =  row.get("MachineRemainingCheck")
			TITIValidationFlag = {"QualityContainerValidation":QualityContainerValidation,"LLContainerValidation":LLContainerValidation,"RemainingQTYValidation":RemainingQTYValidation,"MachineRemainingCheck":MachineRemainingCheck}

		return TITIValidationFlag
	except  Exception as e:
		print(e)
		return 99	
		
def TITOComponentValidation(workorderId,jsonParams,userId):
	apiPath = "ProductionOperatorConsole/TITOTakeInComponentValidation"		
	url = URLPath + apiPath	
	writeData = {
				  "workOrderId": workorderId,				  		
				  "userId": userId,
				  "machineList": jsonParams				  			  
				}

	try:									
		params = system.util.jsonEncode(writeData)	
		resultData = system.net.httpPost(url,'application/json',params)
		decodedData = system.util.jsonDecode(resultData)		
		machineList = []
	
		for row in decodedData:
			IsComponentFeed = row.get("IsComponentFeed")
			IsMoldLoaded = row.get("valid")							
			ToolCode = row.get("ToolCode")
				
		return IsComponentFeed,IsMoldLoaded,ToolCode
	except:
		return 99					
#-------------------------------------------Take In Take-out Button Validation------------------------
	# Application use: To anable Disable the buttons from take-In & Take-out screen
	# Developer Name: Hari Mhasalekar
	# Created On: 18th April 2023
	# Updated By : 
	# Updated On : 
	# ActionCode : Take-In==1, Take-Out==0
	# Response	 : 1==Linke Machine Enable, 2==Take-In Complete Enable, 3==Unlink Machine Enable, 4==Takeout Complete Enable, Return==5 disable take-in take-out button from tab
def takeIntakeOutButtonValidation(workorderId,ActionCode):	
	apiPath = "Workflow/validateTakeInTakeOut?WorkOrderId="+str(workorderId) +("&isTakeIn=")+str(ActionCode)		
	url = URLPath + apiPath
	resultData = None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData = data.json
	dataList = []	
	print'Button Enable Disable API Result'+str(resultData)	
	SrNo = 0
	for i in resultData:			
		LineValidation = i.get("LineValidation")
		TITOValidation = i.get("TITOValidation")
		if LineValidation == 1:
			return	TITOValidation 	# In case if TakeIn TakeOut validation is present for the line then any number other than 99 will be sent 		
		else:
			return 99 			    # In case if TakeIn TakeOut validation is Not configured for the line then 99 will be sent 
	return resultDetails

#-------------------------------------------Take In Take-out Button Validation------------------------
	# Application use: To anable Disable the buttons from take-In & Take-out screen
	# Developer Name: Hari Mhasalekar
	# Created On: 18th April 2023
	# Updated By : 
	# Updated On : 
	# ActionCode : Take-In==1, Take-Out==0
	# Response	 : 1==Linke Machine Enable, 2==Take-In Complete Enable, 3==Unlink Machine Enable, 4==Takeout Complete Enable, Return==5 disable take-in take-out button from tab
def isTakeinTakeoutConfigForLine(workorderId):	
	ActionCode=0
	apiPath = "Workflow/validateTakeInTakeOut?WorkOrderId="+str(workorderId) +("&isTakeIn=")+str(ActionCode)		
	url = URLPath + apiPath
	resultData = None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData = data.json
	dataList = []	
#	print'Button Enable Disable API Result'+str(resultData)	
	SrNo = 0
	for i in resultData:			
		LineValidation = i.get("LineValidation")
		isMachineConfigured = i.get("AtLeastOneMachineTakeIN")	
	return LineValidation,isMachineConfigured
	
#------------------------------ Update Containers For Remaining Qty Before Machine Take-Out ----------------------------------------------
	# Application use: Update Container for remaining Qty
	# Developer Name: Hari Mhasalekar
	# Created On: 28th June 2023
	# Updated By : 
	# Updated On : 
def UpdateContainersforMachine(workorderId,userId,jsonParams):
	try:
		apiPath = "ProductionOperatorConsole/LotNumberGeneration_CNS_DeltaContainers"		
		url = URLPath + apiPath	
		print url	
		writeData = {
					  "WorkOrderId": workorderId,
					  "CreatedBy": userId,
					  "machineList":jsonParams				  			  
					}
											
		params = system.util.jsonEncode(writeData)	
		system.perspective.print('params:'+str(params))
		postResult = system.net.httpPost(url,'application/json',params)
		return 1
	except:	
		return 0