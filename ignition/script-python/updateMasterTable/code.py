import re
import json
import urllib2, urllib
import system
import sys
import traceback
import decimal
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
#defaultPath=system.tag.read("[default]JMES_InternalTags/DafaultTagPath").value
try:
	defaultPath=system.tag.read("[default]JMES_InternalTags/DafaultTagPath").value		
except:
	logger = system.util.getLogger("MES Application")
	logger.error("Unable to read default tag path.")
#----------------------------------------- Function to update parameter master table -------------------------------------
def callParameterTableUpdate():	
	userID = 1
	isAuto = 0
	try:
		#activeMachinesList = updateMasterTable.getActiveMachineList()	  # ------ get active machines list -------------------		
		#Result = PackingAndLabelling.getactiveWoList()	
		Result = PackingAndLabelling.getActiveWorkOrderMachineList()
		activeMachinesList = []		
		for row in Result:
			mchId = row.get("MachineId")		
			machineName = row.get("MachineName")
			lineName = row.get("LineName")
			areaName = row.get("AreaName")
			tempList = [mchId,machineName,lineName,areaName]	
			activeMachinesList.append(tempList)		
	except:
		logger = system.util.getLogger("MES Application")
		logger.error("Unable to get active machines list for datalogging.")
		
	for machineDetails in activeMachinesList:
		machineId = machineDetails[0]
		machineName = machineDetails[1]
		lineName = machineDetails[2]
		areaName = machineDetails[3]		
		tagPath = str(defaultPath)+str(machineName)				
		try:		
			machineParametersList = updateMasterTable.getParameterList(machineId)	  # ------ get active machines list -------------------				
		except:
			logger = system.util.getLogger("MES Application")
			logger.error("Unable to execute API to get parameter List for "+str(machineName))
			pass
		print("Machine Name: "+str(machineName))		
		for parameterName in machineParametersList:		
			parameterName = str(parameterName).strip()	
			#-------------Check machine belongs to CNS or Assembly ----------------
			# If machine Belongs to CNS then Good quantity should be calculated based on Mold and pcs produced from mold.					
#			if parameterName == "GoodQty" and areaName == "CNS":
#				paramCurrentValuePath = str(tagPath) + "/machineGoodQty"						
#				paramPreviousValuePath = str(tagPath) + "/prevmachineGoodQty"	
#			else:	
#				pass			
			paramCurrentValuePath = str(tagPath) + "/" + str(parameterName)								
			paramPreviousValuePath = str(tagPath) + "/prev" + str(parameterName)			
			#------------------------------------------------------------------------									
			try:
				paramCurrentValue  = system.tag.read(paramCurrentValuePath).value
				paramPreviousValue = system.tag.read(paramPreviousValuePath).value				
			except:				
				logger = system.util.getLogger("MES Application")
				strdata = "Faild to read Tag Values for machine :"+str(machineName)+"; Parameter:"+str(parameterName)
				logger.error(strdata)
				pass											
			print("Parameter Name:- "+str(parameterName))
#			if (str(parameterName).strip()=="Repair") or (str(parameterName).strip() == "GoodQty"):
			print("Checkpoint 01")
			try:
				resultDetails = updateMasterTable.getWODetailsForAutoOperation(machineId)
				#print("Checkpoint 80")					
				for WoDetails in resultDetails:
					#print("Checkpoint 81")
					WorkflowOperationsId = WoDetails.get("WorkflowOperationsId")
					WoNumber = WoDetails.get("WorkOrderNo")				
					WorkflowId = WoDetails.get("WorkflowId")
					workOrderQty = WoDetails.get("QTY")					
					Status = WoDetails.get("StatusName")
					lineID = WoDetails.get("LineId")	
					isAuto = WoDetails.get("IsAutoOperation")
					currentOperation = WoDetails.get("OperationName")
			except:
				#print("Checkpoint 82")	
				resultDetails = []
				logger = system.util.getLogger("MES Application")
				logger.error("Unable to execute getWODetailsForAutoOperation function for "+str(machineId))		
				pass		
#			else:
#				pass
#---------------- Auto Downtime-Hold and Alert Creation function  -----------------------------------				
#			print("Checkpoint 09-"+str(isAuto)+" parametername:"+str(parameterName))
			moldCheckDisabled = 1
			if (paramCurrentValue != paramPreviousValue):
				#print("Checkpoint 03")
				print(str(parameterName) +": New Value - " + str(paramCurrentValue)+str("  ; Old Value - ")+str(paramPreviousValue))
				try:
#----------------------------------  If machine Belongs to CNS and Mold is assigned to machine then Good QTY needs to be calculated.-----------------------------				
					if parameterName == "GoodQty" and areaName=="CNS" and moldCheckDisabled==0:
						#print("Checkpoint 83")
						try:
							moldDetails = WorkOrderDetailsAPI.getMoldAssignmentDetails(WoNumber,machineId)
							for moldData in moldDetails:
								cavity = moldData[2]
								productPiece = moldData[3]
								isMoldAssigned = moldData[4]								
						except Exception as e:
							scriptName = "Operator Console: CNS Mold part qty"
							errorMessage=scriptName  +' Exception - '+  str(e)
							Authentication.exceptionLogger(errorMessage)
													
						goodQtyTagPath = str(tagPath) + "/GoodQty"							
						if isMoldAssigned == True:	
							#print("Checkpoint 84")	
							calculatedGoodQty = (paramCurrentValue * cavity)/productPiece							
							system.tag.writeAsync(goodQtyTagPath,calculatedGoodQty)	
							system.tag.writeAsync(paramPreviousValuePath,paramCurrentValue)	
							paramCurrentValue = calculatedGoodQty
						else:
							system.tag.writeAsync(goodQtyTagPath,paramCurrentValue)	
					else: 
						system.tag.writeAsync(paramPreviousValuePath,paramCurrentValue)	
				except:
					logger = system.util.getLogger("MES Application")
					logger.error("Upating current parameter value in prev parameter value or in Database failed for "+str(machineId))
				#print("Checkpoint 04")		
				machineAreaLineId = updateMasterTable.getMachinesDatails(machineId)
				areaId = machineAreaLineId[0]
				lineId = machineAreaLineId[1]
				parameterId = updateMasterTable.getParameterId(machineId,parameterName)
				try:	
					updateMasterTable.updateParameterDetailsInSQLDB(areaId,lineId,machineId,parameterId,paramCurrentValue,WoNumber)
					print("Parameter updated...")
					#print("Checkpoint 05")	
				except:
					logger = system.util.getLogger("MES Application")
					logger.error("Unable to update changed parameter value in Database.")
				#print("Checkpoint 06")	
# ---------------------------------------------------- Creating Downtime Hold Event ---------------------------------------------------------------------------				
				if (parameterName=="Repair") and (int(paramCurrentValue)==2) and (Status!="Downtime-Hold" or Status!="Downtime Hold") :										
					print("Scenario 1 : Generate DowntimeHold and Alert...!!!")											
					scanBadgeText = "Machine"
					downtimeReasonId = 13
					commentText = "Machine Generated  Downtime"						
					try:
						#print("Checkpoint 07")
						saveResult = WorkOrderDetailsAPI.updateDowntimes(WorkflowOperationsId,WoNumber,scanBadgeText,downtimeReasonId,commentText,lineID,machineId,userID)				
						AddDowntime= WorkOrderDetailsAPI.AddDowntime(WorkflowOperationsId,WoNumber,WorkflowId,userID,machineId)						
						#print("Checkpoint 08")
					except:
						logger = system.util.getLogger("MES Application")
						logger.error("Error while executing Auto Downtime-Hold Operation.")
						pass
#-------------------------------------------------------End ----------------------------------------------------------------------------------------------------																			
				elif (str(parameterName).strip() == "GoodQty") and (isAuto==True or isAuto==1 or isAuto=='true'):	
					#print("Checkpoint 2")
					#---------------- Auto Workorder Operation Complete -----------------------------------												
					scanBadgeText = 'Machine'
					goodQty = paramCurrentValue	
					#print("Checkpoint 11")					
					paramCurrentValuePath = str(tagPath) + "/" + "NGQty"
					badQty  = system.tag.read(paramCurrentValuePath).value									
					isPartialFlag = False
					isFullFlag = True
					commentText = "Auto Complete"
					userID = 0						
				else:
					print("Scenario Normal")
					pass					
			else:
				pass				
#-------------- Creating infinite loop to update master table ---------------			
	stopUpdateFlagPath = defaultPath + str("stopUpdateFlag")
	triggerCounterPath = defaultPath + str("testingTrigger")		
	stopUpdateFlag = int(system.tag.read(stopUpdateFlagPath).value)
	triggerCounter = int(system.tag.read(triggerCounterPath).value)	
	if triggerCounter >= 998 and stopUpdateFlag == 0:		
		triggerCounter=0
		system.tag.writeAsync(triggerCounterPath,triggerCounter)		
	elif stopUpdateFlag == 0:
		triggerCounter = triggerCounter + 1
		system.tag.writeAsync(triggerCounterPath,triggerCounter)

 #----------------------End --------------------------------------------------------------------------------------------------	
def completeOperation(WorkflowOperationsId,WoNumber,WorkflowId,scanBadgeText,goodQty,badQty,isPartialFlag,isFullFlag,commentText,userID):
  	apiPath = "OperatorConsole/CompleteOps" 
  	url = URLPath + apiPath
  	writeData = {
  	  "isActive": True,
  	  "createdBy": userID,
  	  "createdOn": "2022-07-14T07:56:52.652Z",
  	  "modifiedBy": userID,
  	  "modifiedOn": "2022-07-14T07:56:52.652Z",
  	  "workOrderNo": WoNumber,	
  	  "workflowOperationsId": WorkflowOperationsId,	
  	  "completeOpsScanBadge": scanBadgeText,	
  	  "completeOpsComments": commentText,
  	  "qualityGood": goodQty,
  	  "qualityBad": badQty,
  	  "isPartial": isPartialFlag,
  	  "isFull": isFullFlag,	
  	  "actualCompletionDate": "2022-07-14T07:56:52.652Z",	
  	  "workflowId": WorkflowId,	
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

def getMachinesDatails(machineId):	
	apiPath = "OperatorConsole/GetMachineDetailOperatorConsole?MachineId="+str(machineId) 
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)	
	resultData= system.util.jsonDecode(data)
	machineDetails = []	
	for i in resultData:			
		lineId = i.get("LineId")
		areaId = i.get("AreaId")									
		machineDetails = [areaId,lineId]
	return machineDetails 	
		
def getCompleteWODetailsForUser(userID):	
	apiPath = "OperatorConsole/GetOperatorConsoleWorkOrdersdefault?UserId="+str(userID)  
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)	
	resultData= system.util.jsonDecode(data)
	dataList = []
	j=1
	for i in resultData:			
		ID = j
		machineId = i.get("machineId")
		machineName = i.get("machineName")
		lineId = i.get("Operations")
		lineName = i.get("WorkflowName")		
		areaId = i.get("Process")
		areaName = i.get("Qty")
		plantId = i.get("Status")		
		plantName = i.get("Completion")
		enterpriseId = i.get("PlannedStartDate")
		enterpriseName = i.get("ActualStartDate")		
		SubInventoryCode = i.get("SubInventoryCode")				
		myList = [ID,machineId,machineName,lineId,lineName,areaId,areaName,plantId,plantName]
		dataList.append(myList)	
		j = j+1		
	headers = ["ID","machineId","machineName","lineId","lineName","areaId","areaName","plantId","plantName"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails		
		
def getParameterList(machineId):	
	apiPath = "OperatorConsole/GetParametersforMachineOperatorConsole?MachineId="+str(machineId) 
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)	
	resultData= system.util.jsonDecode(data)
	parameterList = []	
	for i in resultData:		
		parameterName = i.get("Name")					
		parameterList.append(parameterName)	
	return parameterList 		

def getParameterId(machineId,paramName):	
	apiPath = "OperatorConsole/GetParametersforMachineOperatorConsole?MachineId="+str(machineId) 
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)	
	resultData= system.util.jsonDecode(data)
	paramName = str(paramName).strip()	
	parameterId = 0
	for i in resultData:		
		parameterNameFromList = i.get("Name")
		if str(parameterNameFromList).strip() == paramName:
			parameterId = i.get("Id")	
		else:
			pass			
	return parameterId	
		
def getActiveMachineList():	
	apiPath = "PlantHierarchyMachine/GetMachines" 
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)	
	resultData= system.util.jsonDecode(data)	
	machineList = []	
	for i in resultData:		
		machineName = i.get("machineName")		
		machineId = i.get("machineId")
		lineName = i.get("lineName")
		areaName = i.get("areaName")
		tempList = [machineId,machineName,lineName,areaName]			
		machineList.append(tempList)	
	return machineList 	

def getWODetailsForAutoOperation(machineId):	
	apiPath = "OperatorConsole/GetOperatorConsoleDetailsForAutoOperations?MachineId="+str(machineId)
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)
	resultData= system.util.jsonDecode(data)	
	return resultData
		
def updateParameterDetailsInSQLDB(areaId,lineId,machineId,parameterId,parameterValue,WorkOrderNo):
	apiPath = "OperatorConsole/CreateOperatorConsoleDataAcquisition" 
	url = URLPath + apiPath
	writeData = {
	  "createdBy": 36,
	  "areaId": areaId,
	  "lineId": lineId,
	  "machineId": machineId,	  
	  "parameterId": parameterId,
	  "parameterValue": str(parameterValue),
	  "isReadByMES": False,
	  "workOrderNo":WorkOrderNo	,
	  "ShiftId":1  
	}		
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1	
	try: 
		postReturn = system.net.httpPost(url,'application/json',jsonParams)		
	except:		
		result = 0
		pass
	return result 
	
	
def getHistory(tags, startDate, endDate, returnSize, returnFormat, sampleSize, aggregationMode):
	try:	
		if aggregationMode == None or aggregationMode == '' :
			if startDate != '' and startDate != None:
					dtSet = system.tag.queryTagHistory(paths=tags,startDate=startDate, endDate=endDate, returnSize=returnSize, returnFormat=returnFormat, sampleSize=sampleSize)
			else:
				dtSet = system.tag.queryTagHistory(paths=tags,endDate=endDate, returnSize=returnSize, returnFormat=returnFormat, sampleSize=sampleSize)
		else:		
			if startDate != '' and startDate != None:
				dtSet = system.tag.queryTagHistory(paths=tags,startDate=startDate, endDate=endDate, returnSize=returnSize, aggregationMode = aggregationMode,returnFormat=returnFormat, sampleSize=sampleSize)
			else:	
				dtSet = system.tag.queryTagHistory(paths=tags,endDate=endDate, returnSize=returnSize,aggregationMode = aggregationMode, returnFormat=returnFormat, sampleSize=sampleSize)
		dtpySet = system.dataset.toPyDataSet(dtSet)	
		return dtpySet
	except:
		pass