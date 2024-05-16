import re
import json
import urllib2, urllib
import datetime
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
defaultPath=system.tag.read("[default]JMES_InternalTags/DafaultTagPath").value

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Application use: Get The List of running workorder to show in workorder start
	# Developer Name: Hari Mhasalekar
	# Created On: 08/05/2023
	# Updated By : 
	# Updated On :	
def GetListofrunnigWo(LineId):
	try:
		apiPath = "ProductionOperatorConsole/GetWorkOrderByLineId/LineId:int?LineId="+str(LineId)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)	
		ListOfrunningWo=[]
		if data.good:    
			resultData=data.json
			print 'ResultData'+str(resultData)
			Id=0		
			for i in (resultData):
				Id=Id+1
				workorderName = i.get('MfgOrderName')
				workorderStatusId = i.get('WorkOrderStatusId')
				if workorderStatusId==1:
					workorderStatus='In-Progress'
				elif workorderStatusId==0:
					workorderStatus='Not-Started'
				elif workorderStatusId==2:
					workorderStatus='On-Hold'
				templist=(Id,workorderName,workorderStatus)
				ListOfrunningWo.append(templist)	
		header = ["Id","Workorder", "Status" ]
		resultDetails = system.dataset.toDataSet(header,ListOfrunningWo)	
		return resultDetails
	except:
		print 'Exception'
		exc_type, exc_obj,tb = sys.exc_info()
		errorMessage = "Error:"+ str(exc_obj)			
		lineno = tb.tb_lineno
		print("Script Exception: Workorder Validation")
		print(errorMessage)
		print(lineno)
		resultDetails=[]
		
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Application use: Get The List of Material loaded on Machine
	# Developer Name: Hari Mhasalekar
	# Created On: 10/05/2023
	# Updated By : 
	# Updated On :			
def CurrentLoadedMaterialOnMachine(UserId,workOrderId ,woNumber,machineName):
	try:
		apiPath ="OperatorConsole/GetAttachedWorkFlowProcessComponentsWithSubstituteForOperatorConsole_WorkOrderIdWise/"+str(UserId)+"/"+str(workOrderId)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient() 
		data = client.get(url)
		if data.good:
			resultData=data.json
		dataList = []
		k=1
		dataList = []
#		system.perspective.print('resultData' + str(resultData))
		for i in resultData:
			SrNo = k
			MachineName = i.get("MachineName")
			MachineName1 = MachineName.split('|')
			MachineName=MachineName1[0]
			print("MachineName in Function:"+str(MachineName))
			if str(MachineName)==str(machineName):
				WorkOrderNo=i.get("WorkOrderName")
				PartNowithRevision = i.get("PartNumber")
				LotNo = i.get("TransferComponentLot")
				if str(LotNo) == str("") or str(LotNo).lower() == str("None").lower() or str(LotNo) == str("null").lower():
					LotNo = ''
				else:
					LotNo = LotNo
				consumeQty = i.get("LoadQuantity")
				if str(consumeQty) == str("") or str(consumeQty).lower() == str("None").lower() or str(consumeQty) == str("null").lower():
					consumeQty = 0
				else:
					consumeQty =consumeQty
				bomdetailsId = i.get("BomDetailsId")
				ItemId=i.get("ItemId")
				ERPExpirationDate = ''
				today = system.date.now()
				TodayDate= system.date.format(today, "dd/MM/yyyy,HH:mm:ss")
	
				if ERPExpirationDate >= TodayDate or ERPExpirationDate == None or str(ERPExpirationDate).strip().lower() == str("None").strip().lower():
					IsExpired = 0
				else:
					IsExpired = 1
					
				IsExpired = 0
							
				Operation = i.get("Operations")
				myList = [SrNo,WorkOrderNo,PartNowithRevision,LotNo,consumeQty,MachineName,Operation]
				dataList.append(myList)
				k = k+1
			else:
				pass
				
		headers = ["SrNo","WorkOrderNo","PartNowithRevision","LotNo","consumeQty","MachineName","Operation"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		print 'resultDetails',resultDetails
		return resultDetails
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: PDA :: GetAttachedWorkFlowProcessComponentsWithSubstituteForOperatorConsole_WorkOrderIdWise :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
#		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)	
		print 	errorMessage
		return None

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Application use: Get The List of Material loaded on Machine
	# Developer Name: Hari Mhasalekar
	# Created On: 10/05/2023
	# Updated By : 
	# Updated On :			
def PreviousLoadedMaterialOnMachine(workOrderId ,MachineId):
	try:
		apiPath ="ProductionOperatorConsole/GetPreviousWorkorderMaterialDetails/"+str(workOrderId)+"/"+str(MachineId)
		url = URLPath + apiPath
		print('url: '+str(url))
		resultData=None
		client = system.net.httpClient() 
		data = client.get(url)
		if data.good:
			resultData=data.json
		dataList = []
		k=1
		dataList = []
#		system.perspective.print('resultData' + str(resultData))
		for i in resultData:
			SrNo = k
			MachineName = i.get("EquipmentCode")
			print("MachineName in Function:"+str(MachineName))
			WorkOrderNo=i.get("WorkOrderName")
			PartNo = i.get("PartNo")
			Revision = i.get("Revision")
			PartNowithRevision = PartNo+'_'+Revision
			LotNo = i.get("TransferComponentLot")
			if str(LotNo) == str("") or str(LotNo).lower() == str("None").lower() or str(LotNo) == str("null").lower():
				LotNo = ''
			else:
				LotNo = LotNo
			consumeQty = i.get("FeedLotQuantity")
			if str(consumeQty) == str("") or str(consumeQty).lower() == str("None").lower() or str(consumeQty) == str("null").lower():
				consumeQty = 0
			else:
				consumeQty =consumeQty
			bomdetailsId = i.get("BomDetailsId")
					
			Operation =''
			myList = [SrNo,WorkOrderNo,PartNowithRevision,LotNo,consumeQty,MachineName,Operation]
			dataList.append(myList)
			k = k+1
#			else:
#				pass
				
		headers = ["SrNo","WorkOrderNo","PartNowithRevision","LotNo","consumeQty","MachineName","Operation"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		print 'resultDetails',resultDetails
		return resultDetails
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: PDA :: GetAttachedWorkFlowProcessComponentsWithSubstituteForOperatorConsole_WorkOrderIdWise :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
#		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)	
		print 	errorMessage
		return None		
						
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
		# Application use: Get The List of Previous Completed Workorder
		# Developer Name: Hari Mhasalekar
		# Created On: 11/05/2023
		# Updated By : 
		# Updated On :	
def GetListofPreviousCompletedWorkorders(LineId,machineId,userId,workflowId,CurrentWorderId):
	try:
#		apiPath ="ProductionOperatorConsole/GetPreviousCompletedWorkOrder/6/29/64/241"
		apiPath ="ProductionOperatorConsole/GetPreviousCompletedWorkOrder/"+str(LineId)+"/"+str(machineId)+"/"+str(userId)+"/"+str(workflowId)+"/"+str(CurrentWorderId)+"?CurrentWorkOrderId="+str(CurrentWorderId)
		
		
		url = URLPath + apiPath
		system.perspective.print('url'+str(url))
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		ListOfPrevworkorders=[]
		if data.good:    
			resultData=data.json
		else:	
			resultData=None
		return resultData
	except:
			print 'Exception'
			exc_type, exc_obj,tb = sys.exc_info()
			errorMessage = "Error:"+ str(exc_obj)			
			lineno = tb.tb_lineno
			print("Script Exception: Workorder Validation")
			print(errorMessage)
			print(lineno)
			resultDetails=[]
			return None

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
		# Application use: Get The current workorderInformation
		# Developer Name: Hari Mhasalekar
		# Created On: 11/05/2023
		# Updated By : 
		# Updated On :	
def GetCurrentWorkorderInfo(WorkorderId):
	try:
		apiPath = "ProductionOperatorConsole/GetOperatorConsoleCurrentWorkOrdersInfo/WorkOrderId:int?WorkOrderId="+str(WorkorderId)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)	
		ListOfPrevworkorders=[]
		if data.good:    
			resultData=data.json
			return resultData
		else:
			return []
	except:
			print 'Exception'
			exc_type, exc_obj,tb = sys.exc_info()
			errorMessage = "Error:"+ str(exc_obj)			
			lineno = tb.tb_lineno
			print("Script Exception: Workorder Validation")
			print(errorMessage)
			print(lineno)
			resultDetails=[]
			
#-----------------------------------------------------New Mold Details Against WO No and Machine ID---------------------------------
	# Application use: Production Operator Console --> Display Mold information widget
	# Developer Name: Hari Mhasalekar
	# Created On: 
	# Updated By : 
	# Updated On :	
def CurrentPossibleLoadedMoldOnMachine(WorkorderId,machineID):
	dataList = []	
	if str(WorkorderId).strip() != '' and str(WorkorderId).strip()!= None and str(WorkorderId).strip() != 'None' and str(WorkorderId).lower().strip() != 'value':	
		apiPath='OperatorConsole/OperatorconsoleMoldAssignmentCheck?WorkOrderId='+str(WorkorderId)+'&MachineId='+str(machineID)
		url = URLPath + apiPath
		resultData = None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData = data.json
		  SrNo=0
		for i in resultData:
			SrNo=SrNo+1			
			MachineName = i.get("MachineName")		
			MoldCode = i.get("MoldCode")
			MachineId = i.get("MachineId")
			cavity = i.get("Cavity")
			productPiece = i.get("ProductPiece")		
			MaxLife = i.get("MaxLife")
			MachineShots = i.get("Shots")
			isLoaded = (i.get("isLoaded"))
			ActualLife = i.get("ActualLife")
			print MachineName
			
			if MachineName!= None :
				myList = (SrNo,MachineName,MoldCode,isLoaded)
				dataList.append(myList)	
#			else:
#				dataList = []
		print dataList						
		headers = ["SrNo","MachineName","MoldCode","isLoaded"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails
	
		
#-----------------------------------------------------New Mold Details Against WO No and Machine ID---------------------------------
		# Application use: Production Operator Console --> Display Mold information widget
		# Developer Name: Hari Mhasalekar
		# Created On: 
		# Updated By : 
		# Updated On :	
def PreviousLoadedMoldOnMachine(WorkorderId,machineID):
	dataList = []	
	if str(WorkorderId).strip() != '' and str(WorkorderId).strip()!= None and str(WorkorderId).strip() != 'None' and str(WorkorderId).lower().strip() != 'value':	
		apiPath='OperatorConsole/OperatorconsoleMoldAssignmentCheck?WorkOrderId='+str(WorkorderId)+'&MachineId='+str(machineID)
		url = URLPath + apiPath
		resultData = None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData = data.json
		  SrNo=0
		for i in resultData:
			SrNo=SrNo+1	
			isLoaded = (i.get("isLoaded"))
			if isLoaded==1 or isLoaded==True or isLoaded=='true':		
				MachineName = i.get("MachineName")		
				MoldCode = i.get("MoldCode")
				MachineId = i.get("MachineId")
				cavity = i.get("Cavity")
				productPiece = i.get("ProductPiece")		
				MaxLife = i.get("MaxLife")
				MachineShots = i.get("Shots")
				
				ActualLife = i.get("ActualLife")
				myList = (SrNo,MachineName,MoldCode,isLoaded)
				dataList.append(myList)	
			else:
				pass						
		headers = ["SrNo","MachineName","MoldCode","isLoaded"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails	
	
def getClubbedWorkorders(WorkorderId):
	try:
		scriptName = "API: Get Clubbed WorkOrder List"
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
		
		
#--------------------------------------------------------------------------------------
		# Application use: Production Operator Console --> DIsplay Workinstruction details
		# Developer Name: Hari Mhasalekar
		# Created On: 
		# Updated By : 
		# Updated On :	
def GetListofWorkinstruction(PartNo,Rev,Factory):
	dataList = []	
	
	apiPath='ProductionOperatorConsole/GetWorkinstructionForMSR/'+str(PartNo)+'/'+str(Rev)+'/'+str(Factory)
	url = URLPath + apiPath
	resultData = None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData = data.json
	  SrNo=0
	for i in resultData:
		SrNo=SrNo+1	
		Workinstruction = i.get("Workinstruction")		
		Comment = i.get("Comment")
		myList = (SrNo,Workinstruction,Comment)
		dataList.append(myList)	
							
	headers = ["SrNo","Workinstruction","Comment"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails	