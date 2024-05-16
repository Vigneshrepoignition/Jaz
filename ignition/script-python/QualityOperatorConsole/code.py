import smtplib	
import system
import re
import json
import urllib2, urllib

URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
#URLPath = system.tag.read("[default]JMES_InternalTags/urlSITAPI").value



def getQualityOperatorConsole(enterpriseID,plantID,areaID,lineID,inspectionId,userId):	
	try:	
		print("userId" + str(userId)) 
		workOrderId=0
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
		apiPath = "InspectionProcessManager/GetInspectionProcessManagersByMachineId/"+str(inspectionId)+"/"+str(userId)+"/"+str(lineID)+"/"+str(areaID)+"/"+str(plantID)+"/"+str(enterpriseID)+"/"+str(workOrderId)
		workOrderId='0'
		url = URLPath + apiPath
		print("Qlty URL: "+str(url))
		system.perspective.print(url)
		resultData=None
		client = system.net.httpClient() 
		data = client.get(url)
		if data.good:
			resultData=data.json
		dataList = []
		j=1
		for i in resultData:			
			ID = j
			Status = i.get("Status")
			if str(Status).strip().lower()=="completed" or str(Status).strip() == "Completed":
				pass
			else:				
				InspectionProcessName = i.get("InspectionProcessName")
				ItemId = i.get("ItemId")
				
				Type = i.get("InspectionType")
				WorkOrderNo = i.get("WorkOrderNo")
				PartNumber = i.get("PartNumber")
				StartDate = i.get("StartDate")
				CompletionDate = i.get("CompletionDate")

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
				LineId =  i.get("LineId")
				IsFQC = i.get("IsFQC")
#				print("QUALITY url Operations " +  str(Operations))
				WorkOrderId =  i.get("WorkOrderId")
				
				EnterpriseId = i.get("EnterpriseId")
				PlantId = i.get("PlantId")
				AreaId = i.get("AreaId")

				if str(StartDate).strip()==None or str(StartDate).strip()=='None' or  str(StartDate).strip()=='' or str(StartDate).lower().strip()=='null':
					StartDate=''		

				if str(LastModifiedOn).strip()==None or str(LastModifiedOn).strip()=='None' or  str(LastModifiedOn).strip()=='' or str(LastModifiedOn).lower().strip()=='null':
					LastModifiedOn=''		
				if str(LastModifiedBy).strip()==None or  str(LastModifiedBy).strip()=='None' or str(LastModifiedBy).strip()=='' or str(LastModifiedBy).lower().strip()=='null':
					LastModifiedBy=''	


#				myList = [ID,InspectionProcessName,Type,WorkOrderNo,PartNumber,StartDate,CompletionDate,Status,LastModifiedOn,LastModifiedBy,View,enterpriseName,plantName,areaName,lineName,machineName,InspectionId,MachineId,Operations,ItemId,WorkOrderId,LineId,IsFQC] 		
				myList = [ID,InspectionProcessName,Type,WorkOrderNo,PartNumber,StartDate,CompletionDate,Status,LastModifiedOn,LastModifiedBy,View,enterpriseName,plantName,areaName,lineName,machineName,InspectionId,MachineId,Operations,ItemId,WorkOrderId,LineId,IsFQC,EnterpriseId,PlantId,AreaId] 
				dataList.append(myList)	
				j = j+1			
				print"lineName",lineName
#		headers = ["SRNO","InspectionProcessName","Type","WorkOrderNo","PartNumber","StartDate","CompletionDate","Status","LastModifiedOn","LastModifiedBy","View_Details","EnterpriseName","PlantName","AreaName","LineName","MachineName","InspectionId","MachineId","Operations","ItemId","WorkOrderId","LineId","IsFQC"]
		headers = ["SRNO","InspectionProcessName","Type","WorkOrderNo","PartNumber","StartDate","CompletionDate","Status","LastModifiedOn","LastModifiedBy","View_Details","EnterpriseName","PlantName","AreaName","LineName","MachineName","InspectionId","MachineId","Operations","ItemId","WorkOrderId","LineId","IsFQC","EnterpriseId","PlantId","AreaId"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		print"resultDetails",resultDetails
		return resultDetails 
	except:		
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: Quality Landing Page :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)
		return None

def GetCharacteristicsForInspectionProcessManager(operationId,InspectionTypeId,WoNumber,itemId,CharacteristicId,CharacteristicType,session):
	try:	
		machineId=0
		moldId=0
		lotNumber=-1

		scriptName='Quality Operator Console: - GetCharacteristicsForInspectionProcessManager'
		apiPath = "InspectionProcessManager/GetCharacteristicsForInspectionProcessManager/"+str(operationId)+"/"+str(InspectionTypeId)+"/"+str(WoNumber)+"/"+str(itemId)+"/"+str(CharacteristicId)+"/"+str(CharacteristicType)+"/"+str(machineId)+"/"+str(moldId)+"/"+str(lotNumber)

		url= URLPath + apiPath
		system.perspective.print("GetCharacteristicsForInspectionProcessManager url "+str(url))

		resultData=None
		client = system.net.httpClient()
		data = client.get(url)

		if data.good:    
			resultData=data.json
			print("resultData Quality "+str(resultData))

		dataList = []
		j=1
		for i in resultData:
			ID = j
			CharacteristicId = i.get("CharacteristicId")
			CharacteristicName = i.get("CharacteristicName")
			MinimumLimit = i.get("MinimumLimit")
			NominalValue = i.get("NominalValue")
			MaximumLimit = i.get("MaximumLimit")
			UOM = i.get("UOM")
			ActualValue = i.get("ActualValue")
			InstrumentSerialNumber = i.get("InstrumentSerialNumber")
			Operation = i.get("Operation")
			FrequencyType = i.get("FrequencyType")
			SampleSize = i.get("SampleSize")
			MachineName = i.get("MachineName")
			PlannedStartDate = i.get("PlannedStartDate")
			PlannedDueDate = i.get("PlannedDueDate")
			InstrumentName = i.get("InstrumentNames")
			SelectedInstrument = i.get("SelectedInstrument")
			Id = i.get("Id")
			Status = i.get("Status")
			InspectionProcessManagerId= i.get("InspectionProcessManagerId")
			Spec= i.get("Spec")
			CanComplete=i.get("CanComplete")
			InstrumentType= i.get("InstrumentType")
			characteristicType= i.get("characteristicType")
#			MachineList= i.get("MachineList")
			LotNumbers = i.get("LotNumbers")
			LotNumber = i.get("LotNumber")
			MachineName = i.get("MachineName1")
			MoldName = i.get("MoldName")
			workOrderType = i.get("workOrderType")
			IsCavity = i.get("IsCavity")
			CavityNumber = i.get("CavityNumber")
			ErrorMessage = i.get('errorMessage')
#			LotNumber='23242342342lot'
			
			
			AddAlert=''
			if str(SelectedInstrument).strip()=='' or str(SelectedInstrument).strip()=='None' or str(SelectedInstrument).strip()==None:
				SelectedInstrument=0


			if SampleSize==None or str(SampleSize)==None or str(SampleSize).strip()=='':
				SampleSize=0
			if str(CharacteristicId).strip()==None or  str(CharacteristicId).strip()=='' or  str(CharacteristicId).strip()=='None':
				CharacteristicId=""
			if str(CharacteristicName).strip()==None or  str(CharacteristicName).strip()=='' or  str(CharacteristicName).strip()=='None':
				CharacteristicName=""
			if str(MinimumLimit).strip()==None or  str(MinimumLimit).strip()=='' or  str(MinimumLimit).strip()=='None':
				MinimumLimit=0.000
			if str(NominalValue).strip()==None or  str(NominalValue).strip()=='' or  str(NominalValue).strip()=='None':
				NominalValue=0.000
			if str(MaximumLimit).strip()==None or  str(MaximumLimit).strip()=='' or  str(MaximumLimit).strip()=='None':
				MaximumLimit=0.000
			if str(UOM).strip()==None or  str(UOM).strip()=='' or  str(UOM).strip()=='None':
				UOM=''
			if str(ActualValue).strip()==None or  str(ActualValue).strip()=='' or  str(ActualValue).strip()=='None':
				ActualValue=0.0
			if str(InstrumentSerialNumber).strip()==None or  str(InstrumentSerialNumber).strip()=='' or  str(InstrumentSerialNumber).strip()=='None':
				InstrumentSerialNumber=''
			if str(Operation).strip()==None or  str(Operation).strip()=='' or  str(Operation).strip()=='None':
				Operation=''
			if str(FrequencyType).strip()==None or  str(FrequencyType).strip()=='' or  str(FrequencyType).strip()=='None':
				FrequencyType=''
			if str(SampleSize).strip()==None or  str(SampleSize).strip()=='' or  str(SampleSize).strip()=='None':
				SampleSize=''
			if str(MachineName).strip()==None or  str(MachineName).strip()=='' or  str(MachineName).strip()=='None':
				MachineName=''
			if str(PlannedStartDate).strip()==None or  str(PlannedStartDate).strip()=='' or  str(PlannedStartDate).strip()=='None':
				PlannedStartDate=''	
			if str(PlannedDueDate).strip()==None or  str(PlannedDueDate).strip()=='' or  str(PlannedDueDate).strip()=='None':
				PlannedDueDate=''
			if str(InstrumentName).strip()==None or  str(InstrumentName).strip()=='' or  str(InstrumentName).strip()=='None':
				InstrumentName=''				

			NominalValue=float(NominalValue)
			MaximumLimit=float(MaximumLimit)
			MinimumLimit=float(MinimumLimit)

			myList = [ID,CharacteristicId,CharacteristicName,MinimumLimit,NominalValue,MaximumLimit,UOM,ActualValue,InstrumentSerialNumber,Operation,FrequencyType,SampleSize,MachineName,InspectionProcessManagerId,PlannedStartDate,PlannedDueDate,InstrumentName,SelectedInstrument,Id,Status,operationId,InspectionTypeId,itemId,Spec,InstrumentType,CanComplete,AddAlert,characteristicType,LotNumbers,LotNumber,MachineName,MoldName,workOrderType,IsCavity,CavityNumber,ErrorMessage]
			dataList.append(myList)	
			j = j+1

		headers = ["SRNO","CharacteristicId","CharacteristicName","MinimumLimit","NominalValue","MaximumLimit","UOM","ActualValue","InstrumentSerialNumber","Operation","FrequencyType","SampleSize","MachineName","InspectionProcessManagerId","PlannedStartDate","PlannedDueDate","InstrumentName","SelectedInstrument","Id","Status","operationId","InspectionTypeId","itemId","Spec","InstrumentType","CanComplete","AddAlert","characteristicType","LotNumbers","LotNumber","MachineName","MoldName","workOrderType","IsCavity","CavityNumber","ErrorMessage"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		print errorMessage
		system.perspective.print(errorMessage)
		Authentication.exceptionLogger(errorMessage)	
		return None

def GetCharacteristicsForInspectionProcessManagerParent(operationId,InspectionTypeId,WoNumber,itemId,CharacteristicId,CharacteristicType,session):	

	try:
		machineId=0
		moldId=0
		lotNumber=-1

		scriptName='Quality Operator Console: - GetCharacteristicsForInspectionProcessManager'
		apiPath = "InspectionProcessManager/GetCharacteristicsForInspectionProcessManager/"+str(operationId)+"/"+str(InspectionTypeId)+"/"+str(WoNumber)+"/"+str(itemId)+"/"+str(CharacteristicId)+"/"+str(CharacteristicType)+"/"+str(machineId)+"/"+str(moldId)+"/"+str(lotNumber)
		url = URLPath + apiPath

		system.perspective.print("GetCharacteristicsForInspectionProcessManager url "+str(url))
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData=data.json

		dataList = []
		j=1
		for i in resultData:
			ID = j
			CharacteristicId = i.get("CharacteristicId")
			CharacteristicName = i.get("CharacteristicName")
			MinimumLimit = i.get("MinimumLimit")
			NominalValue = i.get("NominalValue")
			MaximumLimit = i.get("MaximumLimit")
			UOM = i.get("UOM")
			ActualValue = i.get("ActualValue")
			InstrumentSerialNumber = i.get("InstrumentSerialNumber")
			Operation = i.get("Operation")
			FrequencyType = i.get("FrequencyType")
			SampleSize = i.get("SampleSize")
			MachineName = i.get("MachineName")
			PlannedStartDate = i.get("PlannedStartDate")
			PlannedDueDate = i.get("PlannedDueDate")
			InstrumentName = i.get("InstrumentNames")
			SelectedInstrument = i.get("SelectedInstrument")
			Id = i.get("Id")
			Status = i.get("Status")
			InspectionProcessManagerId= i.get("InspectionProcessManagerId")
			Spec= i.get("Spec")
			CanComplete=i.get("CanComplete")
			InstrumentType= i.get("InstrumentType")
			characteristicType= i.get("characteristicType")
			LotNumbers = i.get("LotNumbers")
			LotNumber = i.get("LotNumber")
			MachineName = i.get("MachineName1")
			MoldName = i.get("MoldName")
			workOrderType = i.get("workOrderType")
			IsCavity = i.get("IsCavity")		
			CavityNumber = i.get("CavityNumber")
			ErrorMessage = i.get('errorMessage')
#			LotNumbers='23242342342'

			system.perspective.print('MinimumLimit  is: ' + str(MinimumLimit))
			system.perspective.print('MaximumLimit is: ' + str(MaximumLimit))
			system.perspective.print('ActualValue is: ' + str(ActualValue))

			AddAlert=''
			if str(SelectedInstrument).strip()=='' or str(SelectedInstrument).strip()=='None' or str(SelectedInstrument).strip()==None:
				SelectedInstrument=0

#			InspectionProcessManagerId = i.get("InspectionProcessManagerId")
			if str(CharacteristicId).strip()==None or  str(CharacteristicId).strip()=='' or  str(CharacteristicId).strip()=='None':
				CharacteristicId=""
			if str(CharacteristicName).strip()==None or  str(CharacteristicName).strip()=='' or  str(CharacteristicName).strip()=='None':
				CharacteristicName=""
			if str(MinimumLimit).strip()==None or  str(MinimumLimit).strip()=='' or  str(MinimumLimit).strip()=='None':
				MinimumLimit=0.000
			if str(NominalValue).strip()==None or  str(NominalValue).strip()=='' or  str(NominalValue).strip()=='None':
				NominalValue=0.000
			if str(MaximumLimit).strip()==None or  str(MaximumLimit).strip()=='' or  str(MaximumLimit).strip()=='None':
				MaximumLimit=0.000
			if str(UOM).strip()==None or  str(UOM).strip()=='' or  str(UOM).strip()=='None':
				UOM=''
			if str(ActualValue).strip()==None or  str(ActualValue).strip()=='' or  str(ActualValue).strip()=='None':
				ActualValue=0.0
			if str(InstrumentSerialNumber).strip()==None or  str(InstrumentSerialNumber).strip()=='' or  str(InstrumentSerialNumber).strip()=='None':
				InstrumentSerialNumber=''
			if str(Operation).strip()==None or  str(Operation).strip()=='' or  str(Operation).strip()=='None':
				Operation=''
			if str(FrequencyType).strip()==None or  str(FrequencyType).strip()=='' or  str(FrequencyType).strip()=='None':
				FrequencyType=''
			if str(SampleSize).strip()==None or  str(SampleSize).strip()=='' or  str(SampleSize).strip()=='None':
				SampleSize=''
			if str(MachineName).strip()==None or  str(MachineName).strip()=='' or  str(MachineName).strip()=='None':
				MachineName=''
			if str(PlannedStartDate).strip()==None or  str(PlannedStartDate).strip()=='' or  str(PlannedStartDate).strip()=='None':
				PlannedStartDate=''	
			if str(PlannedDueDate).strip()==None or  str(PlannedDueDate).strip()=='' or  str(PlannedDueDate).strip()=='None':
				PlannedDueDate=''
			if str(InstrumentName).strip()==None or  str(InstrumentName).strip()=='' or  str(InstrumentName).strip()=='None':
				InstrumentName=''				

			NominalValue=''
			MaximumLimit=''
			MinimumLimit=''
			ActualValue=''
			CavityNumber=''
			UOM=''
			Spec=''
			InstrumentType=''
			
			myList = [ID,CharacteristicId,CharacteristicName,MinimumLimit,NominalValue,MaximumLimit,UOM,ActualValue,InstrumentSerialNumber,Operation,FrequencyType,SampleSize,MachineName,InspectionProcessManagerId,PlannedStartDate,PlannedDueDate,InstrumentName,SelectedInstrument,Id,Status,operationId,InspectionTypeId,itemId,Spec,InstrumentType,CanComplete,AddAlert,characteristicType,LotNumbers,LotNumber,MachineName,MoldName,workOrderType,IsCavity,CavityNumber,ErrorMessage] 		
#			myList["style"] = {"fontWeight": "bold"}
			dataList.append(myList)	
			j = j+1

		headers = ["SRNO","CharacteristicId","CharacteristicName","MinimumLimit","NominalValue","MaximumLimit","UOM","ActualValue","InstrumentSerialNumber","Operation","FrequencyType","SampleSize","MachineName","InspectionProcessManagerId","PlannedStartDate","PlannedDueDate","InstrumentName","SelectedInstrument","Id","Status","operationId","InspectionTypeId","itemId","Spec","InstrumentType","CanComplete","AddAlert","characteristicType",",LotNumbers","LotNumber","MachineName","MoldName","workOrderType","IsCavity","CavityNumber","ErrorMessage"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		print"resultDetails",resultDetails
		return resultDetails 
	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		print errorMessage
		system.perspective.print(errorMessage)
		Authentication.exceptionLogger(errorMessage)	
		return None				
		
										
def startQuality(InspectionProcessId,WoNumber,userID,ItemId):
	try: 
		scriptName="Quality Operator Console : Start Quality Operation"
		apiPath = "InspectionProcessManager/AddUpdateInspectionForOperator"
		url = URLPath + apiPath		
		
		writeData = {
		  "workOrderNo": str(WoNumber),
		  "scanBadge": "",
		  "inspectionProcessId": 0,
		  "statusId": 1,
		  "updatedBy": int(userID),
		   "ItemId":ItemId 
		}
		
		jsonParams = system.util.jsonEncode(writeData)		
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
			print("PostReturn",postReturn)
		except:		
			result = 0
			pass
		print "Result",result
		return result
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)


def completeQuality(InspectionProcessId,WoNumber,userID,ItemId):
	try: 
		scriptName="Quality Operator Console : Start Quality Operation"
		apiPath = "InspectionProcessManager/AddUpdateInspectionForOperator"
		url = URLPath + apiPath		
		
		writeData = {
		  "workOrderNo": str(WoNumber),
		  "scanBadge": "",
		  "inspectionProcessId": 0,
		  "statusId": 3,
		  "updatedBy": int(userID),
		  "ItemId":ItemId 
		}

		jsonParams = system.util.jsonEncode(writeData)		
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
			print("PostReturn",postReturn)
		except:		
			result = 0
			pass
		print "Result",result
		return result
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		
def UpdateRecordCharacteristicValuesFromOperator(WoNumber,characteristicId,inspectionProcessId,actualValue,instrumentId,instrumentSerialNumber,id,userID,LotNumber,machineId,MoldId,operationId,cavity):
	try: 
		scriptName="Quality Operator Console : Start RecordCharacteristicValuesFromOperator"
		apiPath = "InspectionProcessManager/RecordCharacteristicValuesFromOperator"
		url = URLPath + apiPath		
		instrumentId=int(instrumentId)
		system.perspective.print("url" +str(url))
		writeData = {
			"workOrderNo": WoNumber,
			"characteristicId": characteristicId,
			"inspectionProcessId": inspectionProcessId,
			"actualValue": actualValue,
			"instrumentId": instrumentId,
			"instrumentSerialNumber": instrumentSerialNumber,
			"id": id,
			"updatedBy": userID,
			"lotNumber": LotNumber,
			"machineId": machineId,
			"moldId": MoldId,
			"operationId": operationId,
			"cavityNumber":cavity
		}
		system.perspective.print("writeData = " +str(writeData))
		jsonParams = system.util.jsonEncode(writeData)		
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
			print("PostReturn",postReturn)
		except:		
			result = 0
			pass
		print "Result",result
		return result
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		print errorMessage
		return 0

def AddInspectionDetailRecord(WoNumber,inspectionProcessId,userID,machineId,moldId):
	try: 
		scriptName="Quality Operator Console : Start AddInspectionDetailRecord"
		apiPath = "InspectionProcessManager/AddInspectionDetailRecord"
		url = URLPath + apiPath		
		system.perspective.print("url" +str(url))
		writeData = {
			"inspectionProcessId": inspectionProcessId,
			"workOrderNumber": str(WoNumber),
			"userId": userID,
			"machineId": machineId,
			"moldId": moldId
		}
		system.perspective.print("writeData" +str(writeData))
		jsonParams = system.util.jsonEncode(writeData)		
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
			print("PostReturn",postReturn)
		except:		
			result = 0
			pass
		print "Result",result
		return result
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		print errorMessage
		return 0
		
def AddQualityAlert(trnId,userID):
	try: 
		scriptName="Quality Operator Console : Start AddQualityAlert"
		apiPath = "InspectionProcessManager/AddQualityAlert"
		url = URLPath + apiPath		
		system.perspective.print("url" +str(url))
		writeData = {
			"trnId": trnId,
			"raisedBy": userID
		}
		system.perspective.print("writeData" +str(writeData))
		jsonParams = system.util.jsonEncode(writeData)		
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
			print("PostReturn",postReturn)
		except:		
			result = 0
			pass
		print "Result",result
		return result
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		print errorMessage
		return 0	
		
			

def getQualityOperatorConsole1(enterpriseID,plantID,areaID,lineID,inspectionId,userId):	
	try:	
		print("userId" + str(userId)) 
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
		print url
#		system.perspective.print("url " + str(url )) 
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		
		resultData= system.util.jsonDecode(data)
		dataList = []
		j=1
		for i in resultData:			
			ID = j
			Status = i.get("Status")
	
			InspectionProcessName = i.get("InspectionProcessName")
			ItemId = i.get("ItemId")
			
			Type = i.get("InspectionType")
			WorkOrderNo = i.get("WorkOrderNo")
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
			WorkOrderId =  i.get("WorkOrderId")
			LineId =  i.get("LineId")
			
			print"LastModifiedOn =",LastModifiedOn
			print"LastModifiedBy =",LastModifiedBy
			if str(LastModifiedOn).strip()==None or str(LastModifiedOn).strip()=='None' or  str(LastModifiedOn).strip()=='' or str(LastModifiedOn).lower().strip()=='null':
				LastModifiedOn=''		
			if str(LastModifiedBy).strip()==None or  str(LastModifiedBy).strip()=='None' or str(LastModifiedBy).strip()=='' or str(LastModifiedBy).lower().strip()=='null':
				LastModifiedBy=''	
#			LastModifiedBy=''
#			LastModifiedOn=''
			myList = [ID,InspectionProcessName,Type,WorkOrderNo,PartNumber,StartDate,CompletionDate,Status,LastModifiedOn,LastModifiedBy,View,enterpriseName,plantName,areaName,lineName,machineName,InspectionId,MachineId,Operations,ItemId,WorkOrderId,LineId] 		
			dataList.append(myList)	
			j = j+1
			
		headers = ["SRNO","InspectionProcessName","Type","WorkOrderNo","PartNumber","StartDate","CompletionDate","Status","LastModifiedOn","LastModifiedBy","View_Details","EnterpriseName","PlantName","AreaName","LineName","MachineName","InspectionId","MachineId","Operations","ItemId","WorkOrderId","LineId"]
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
		
def GetMoldDataByMachine(machineId,woNumber):
	try:
		scriptName='GetMoldDataByMachine Quality'
		apiPath = "InspectionProcessManager/GetMoldDataByMachine/"+str(machineId)+"/"+str(woNumber)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		dataListSam = []
		dataList = []
		print resultData
		for i in resultData:	
			ToolId = i.get("ToolId")
			ToolName = i.get("ToolName")
			SampleSize = i.get("SampleSize")
			myList = [ToolId,ToolName]
			myListSam = [ToolId,ToolName,SampleSize]
			
			dataList.append(myList)			
			dataListSam.append(myListSam)	
			
		headers = ["ToolId","ToolName"]
		headersSam = ["ToolId","ToolName","SampleSize"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		resultDetailsSam = system.dataset.toDataSet(headersSam,dataListSam)
		return resultDetails,resultDetailsSam
	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print("errorMessage" + str(errorMessage))
		print"errorMessage",errorMessage	
		return None			

def GetMachinesByOperationForQuality(operationId ,woNumber):
	try:
		scriptName='GetMachinesByOperationForQuality Quality'
		apiPath = "InspectionProcessManager/GetMachinesByOperationForQuality/"+str(operationId )+"/"+str(woNumber)

		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		dataList = []
		dataListLot = []
		print resultData
		for i in resultData:	
			machineId = i.get("machineId")
			machineName = i.get("machineName")
			lotNumbers = i.get("lotNumbers")
			
			myList = [machineId,machineName]
			dataList.append(myList)	
			
			myListLot = [machineId,machineName,lotNumbers]
			dataListLot.append(myListLot)	
			
		headers = ["machineId","machineName"]
		headersLot = ["machineId","machineName","lotNumbers"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		resultDetailslot = system.dataset.toDataSet(headersLot,dataListLot)
		return resultDetails,resultDetailslot
	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print("errorMessage" + str(errorMessage))
		print"errorMessage",errorMessage	
		return None		
		
def getProductionQualityOperatorConsole(enterpriseID,plantID,areaID,lineID,inspectionId,userId,workOrderId):	
	try:
		import json
		resultDetails=None
		scriptName='Quality Operator Console: - getQualityOperatorConsole'

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

		system.perspective.print("EnterpriseID  :" + str(enterpriseID))
		system.perspective.print("plantID  :" + str(plantID))
		system.perspective.print("areaID  :" + str(areaID))
		system.perspective.print("lineID  :" + str(lineID))
		system.perspective.print("inspectionId  :" + str(inspectionId))
		system.perspective.print("workOrderId  :" + str(workOrderId))

		apiPath = "InspectionProcessManager/GetInspectionProcessManagersByMachineId/"+str(inspectionId)+"/"+str(userId)+"/"+str(lineID)+"/"+str(areaID)+"/"+str(plantID)+"/"+str(enterpriseID)+"/"+str(workOrderId)
		url = URLPath + apiPath
		system.perspective.print(" || url  :" + str(url))
		resultData=None
		client = system.net.httpClient() 
		data = client.get(url)
		if data.good:
			resultData=data.json
		dataList = []
		j=1
		for i in resultData:			
			ID = j
			Status = i.get("Status")
			if str(Status).strip().lower()=="completed" or str(Status).strip() == "Completed":
				pass
			else:				
				InspectionProcessName = i.get("InspectionProcessName")
				ItemId = i.get("ItemId")
				
				Type = i.get("InspectionType")
				WorkOrderNo = i.get("WorkOrderNo")
				PartNumber = i.get("PartNumber")
				StartDate = i.get("StartDate")
				CompletionDate = i.get("CompletionDate")

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
				LineId =  i.get("LineId")
				IsFQC = i.get("IsFQC")

				WorkOrderId =  i.get("WorkOrderId")
				
				EnterpriseId = i.get("EnterpriseId")
				PlantId = i.get("PlantId")
				AreaId = i.get("AreaId")
				
				if str(LastModifiedOn).strip()==None or str(LastModifiedOn).strip()=='None' or  str(LastModifiedOn).strip()=='' or str(LastModifiedOn).lower().strip()=='null':
					LastModifiedOn=''		
				if str(LastModifiedBy).strip()==None or  str(LastModifiedBy).strip()=='None' or str(LastModifiedBy).strip()=='' or str(LastModifiedBy).lower().strip()=='null':
					LastModifiedBy=''	
#				myList = [ID,InspectionProcessName,Type,WorkOrderNo,PartNumber,StartDate,CompletionDate,Status,LastModifiedOn,LastModifiedBy,View,enterpriseName,plantName,areaName,lineName,machineName,InspectionId,MachineId,Operations,ItemId,WorkOrderId,LineId,IsFQC,EnterpriseId,PlantId,AreaId] 
#				dataList.append(myList)	
				j = j+1			
		
				resultDetails = {
								"SRNO":ID,
								"InspectionProcessName":InspectionProcessName,
								"Type":Type,
								"WorkOrderNo":WorkOrderNo,
								"PartNumber":PartNumber,
								"StartDate":StartDate,
								"CompletionDate":CompletionDate,
								"Status":Status,
								"LastModifiedOn":LastModifiedOn,
								"LastModifiedBy":LastModifiedBy,
								"View_Details":View,
								"EnterpriseName":enterpriseName,
								"PlantName":plantName,
								"AreaName":areaName,
								"LineName":lineName,
								"MachineName":machineName,
								"InspectionId":InspectionId,
								"MachineId":MachineId,
								"Operations":Operations,
								"ItemId":ItemId,
								"WorkOrderId":WorkOrderId,
								"LineId":LineId,
								"IsFQC":IsFQC,
								"EnterpriseId":EnterpriseId,
								"PlantId":PlantId,
								"AreaId":AreaId
								}		
				break
#		headers = ["SRNO","InspectionProcessName","Type","WorkOrderNo","PartNumber","StartDate","CompletionDate","Status","LastModifiedOn","LastModifiedBy","View_Details","EnterpriseName","PlantName","AreaName","LineName","MachineName","InspectionId","MachineId","Operations","ItemId","WorkOrderId","LineId","IsFQC","EnterpriseId","PlantId","AreaId"]
#		resultDetails = system.dataset.toDataSet(headers,dataList)
#		resultDetails=str(resultDetails)
#		print"resultDetails",resultDetails
		return resultDetails 

	except:		
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: Quality Production Landing Page :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)
		return None

def GetCollectedSampleSizeForCharacteristicsByMoldId(woNumber,moldId,characteristicId):
	try:
		scriptName='GetCollectedSampleSizeForCharacteristicsByMoldId Quality'
		apiPath = "InspectionProcessManager/GetCollectedSampleSizeForCharacteristicsByMoldId/"+str(woNumber)+"/"+str(moldId)+"/"+str(characteristicId)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		dataListSam = []
		dataList = []
		print resultData
		for i in resultData:	
			collectedSample = i.get("collectedSample")
			cavityNumbers = i.get("cavityNumbers")
			myList = [collectedSample,cavityNumbers]
			dataList.append(myList)			
		headers = ["collectedSample","cavityNumbers"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:		
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		print("errorMessage" + str(errorMessage))
		print"errorMessage",errorMessage	
		return None																																										
															