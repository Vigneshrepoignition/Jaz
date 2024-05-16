import re
import json
import urllib2, urllib
from datetime import datetime
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value

#--------Used in Both Line Side Storage and Machine Feeding Screens: Movement TypeId = 2 (POU) , 3 (MachineFeeding)
def getValidationStatus(selectedItemId,scannedLotNumber,selectedLineId,scannedLotQty,movementTypeId,selectedWorkorderId,machineLocator,labelType,scannedVendorLot):
	
	try:
		apiPath = "ProductionOperatorConsole/MaterialFeedingValidation"
		url = URLPath + apiPath
		params = {
		 		  "operatorMaterialReturn": {
		   							     "workorderID": selectedWorkorderId,
		   							     "materialMovementTypeId" : movementTypeId,
		   							     "lineID": selectedLineId,
		   							     "itemId": selectedItemId,
		   							     "TransferComponentLot": str(scannedLotNumber),
		   							     "machineLocator": str(machineLocator),  #---- Will be used for the CNS Only----------
#		   							     "returnQuantity": str(scannedLotQty),
									     "labelType": labelType,
									     "vendorLot": str(scannedVendorLot)
		   							   }
		   							 }

		jsonParams = system.util.jsonEncode(params)			 
		result = 1
		system.perspective.print(' jsonParams For Material Feeding Validation is ::' + str(jsonParams))
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)	
		except:
			import sys, os
			exc_type, exc_obj,tb = sys.exc_info()
			lineno = tb.tb_lineno
			errorMessage = "'Exception :: PDA :: Post Return :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
			system.perspective.print(errorMessage+' || Line No :' + str(lineno))
			Authentication.exceptionLogger(errorMessage)
			result =0
			pass
				
		try:
			resultData= system.util.jsonDecode(postReturn)
		except:
			import sys, os
			exc_type, exc_obj,tb = sys.exc_info()
			lineno = tb.tb_lineno
			errorMessage = "'Exception :: PDA :: getValidationStatus :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
			system.perspective.print(errorMessage+' || Line No :' + str(lineno))
			Authentication.exceptionLogger(errorMessage)
			resultData = []

		dataList = []

		for i in resultData:
			ReceivedQuantity = PDAComponentScanning.isNotBlank(i.get("ReceivedQuantity"))
			DispatchedQuantity = PDAComponentScanning.isNotBlank(i.get("DispatchedQuantity"))
			ERPExpirationDate = PDAComponentScanning.isNotBlank(i.get("ExpiryDate"))
			
			system.perspective.print('ReceivedQuantity  is :' + str(ReceivedQuantity))
			system.perspective.print('DispatchedQuantity  is :' + str(DispatchedQuantity))
			system.perspective.print('ERPExpirationDate  is :' + str(ERPExpirationDate))
			
			if (str(ReceivedQuantity).lower().strip() == str('none').strip().lower() and str(DispatchedQuantity).lower().strip() == str('none').strip().lower() and str(ERPExpirationDate).lower().strip() == str('none').strip()) or (str(ReceivedQuantity).lower().strip() == str('0').strip().lower() and str(DispatchedQuantity).lower().strip() == str('0').strip().lower() and str(ERPExpirationDate).lower().strip() == str('0').strip()):
				AvailableLot = 0
			else:
				AvailableLot = 1

			if int(AvailableLot) == int(1):
				totalReceivedLotQuantity = PDAComponentScanning.isNotBlank(i.get("DispatchedQuantity"))

				if int(movementTypeId) == int(2):
					TotalInlinePOUQty = float(PDAComponentScanning.isNotBlank(i.get("ReceivedQuantity")))
				elif int(movementTypeId) == int(3):
					TotalInlinePOUQty = float(PDAComponentScanning.isNotBlank(i.get("LoadedQuantity")))
				else:
					pass

				AvailableQTY = float(totalReceivedLotQuantity) - float(TotalInlinePOUQty)
				ERPExpirationDate =  i.get("ExpiryDate")

				if str(ERPExpirationDate).strip().lower() != str('none').strip().lower() or ERPExpirationDate != None or str(ERPExpirationDate).strip().lower() != str("None").strip().lower():
					from datetime import datetime
					input_format = "%Y-%m-%dT%H:%M:%S.%f"
					output_format = "%d/%m/%Y,%H:%M:%S"
					input_datetime = datetime.strptime(ERPExpirationDate, input_format)
					ERPExpirationDate = input_datetime.strftime(output_format)
					today = system.date.now()
					TodayDate= system.date.format(today, "dd/MM/yyyy,HH:mm:ss")
					
					system.perspective.print('ERPExpirationDate : ' + str(ERPExpirationDate))
					system.perspective.print('TodayDate : ' + str(TodayDate))
	
	#				if ERPExpirationDate >= TodayDate or str(ERPExpirationDate) >= str(TodayDate) or ERPExpirationDate == None or str(ERPExpirationDate).strip().lower() == str("None").strip().lower():
	#					IsExpired = 0
	#				else:
	#					IsExpired = 1
	
					erp_expiration_date = datetime.strptime(ERPExpirationDate, "%d/%m/%Y,%H:%M:%S")
					today_date = datetime.strptime(TodayDate, "%d/%m/%Y,%H:%M:%S")
	
					if erp_expiration_date >= today_date:
					    IsExpired = 0
					else:
					   IsExpired = 1
				else:
					IsExpired = 0

				system.perspective.print('ERPExpirationDate : ' + str(ERPExpirationDate))
				system.perspective.print('IsExpired : ' + str(IsExpired))
			else:
				AvailableQTY= 0
				IsExpired = 0

#			IsExpired = 0
			myList = [AvailableLot,AvailableQTY,IsExpired] 		
			dataList.append(myList)
		headers = ["AvailableLot","AvailableQTY","IsExpired"] 	
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: PDA :: getValidationStatus :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)

#------------PDA------ Line Side Storage POU------------------------------------------------------>
def GetRequestedComponentsDetails(selectedWorkorderId,selectedLineId):
	system.perspective.print("selectedWorkorderId :" + str(selectedWorkorderId))
	system.perspective.print("selectedLineId :" + str(selectedLineId))
	try:
		url= URLPath + "OperatorConsole/GetOperatorConsoleMaterialRequest?WorkOrderId="+str(selectedWorkorderId)+"&LineId="+str(selectedLineId)
		
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		print 'data',data
		if data.good:    
			resultData=data.json

		try:
			headers = ["SrNo","ComponentName","Uom","DeltaQty","ItemId","SubInventoryName"]	
			dataList=[]
			k = 1
			for i in resultData:
				SrNo = k
				ComponentName = i.get("Material")
				Uom = i.get('UOMName')
				DeltaQty =i.get('DeltaQty')
				ItemId = i.get('ItemId')
				SubInventoryName = i.get('SubInventory')
				k = k+1
				myList = [SrNo,ComponentName,Uom,DeltaQty,ItemId,SubInventoryName]	
				dataList.append(myList)	
			resultDetails = system.dataset.toDataSet(headers,dataList)
			return 	resultDetails
		except:
			pass
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: PDA :: Line Side Storage : Get Requested Componnets"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		system.perspective.print("errorMessage :" + str(errorMessage))
		Authentication.exceptionLogger(errorMessage)


def getComponentSlotDetails(selectedLineId,selectedItemId):
	try:
		url= URLPath + "MaterialMovement/GetPOUDetailsByItemID/"+str(selectedLineId)+"/"+str(selectedItemId)
		
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		print 'data',data
		if data.good:    
			resultData=data.json
			
#		request = urllib2.Request(url)
#		response=urllib2.urlopen(request)
#		data = system.net.httpGet(url)
#		resultData= system.util.jsonDecode(data)

		dataList=[]
		for i in resultData:
			slotItemId= i.get("PartNo")
			slotMaximumQty = i.get("MAXQuantity")
			slotInHandQty = i.get("InHandQty")
			slotCapacity= i.get("SlotCapacity")
			slotName = i.get("SlotName")

			myList = [slotItemId,slotMaximumQty,slotInHandQty,slotCapacity,slotName]
			dataList.append(myList)	
		headers = ["SlotItemId","SlotMaximumQty","SlotInHandQty","SlotCapacity","SlotName"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:
		pass

def AddComponentsinPOU(selectedWorkorderId,selectedLineId,selectedItemId,slotID,bomDetailsId,receivedLotNumber,receivedQuantity,userId,labelType,scannedVendorLot):
	try: 
		scriptName="API:AddInhandQty"
		apiPath = "MaterialMovement/ReceiveMaterialFromOperatorConsole"
		url = URLPath + apiPath		
		writeData = {
			"receiveMaterial": {
							    "workOrderId": selectedWorkorderId,
							    "lineID": selectedLineId,
							    "itemId": selectedItemId,
							    "slotID": slotID,
							    "bomDetailsId": bomDetailsId,
							    "TransferComponentLot": str(receivedLotNumber),
							    "receivedQuantity": receivedQuantity,
							    "createdBy":userId,
						        "labelType": labelType,
						       	"vendorLot": str(scannedVendorLot)
			  					}
			}
		jsonParams = system.util.jsonEncode(writeData)		
		system.perspective.print('Post Slot Details JOSN :' + str(jsonParams))
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

#---------------PDA Component Scanning ---------------------------------
def getSubstitueComponentDetails(selectedWoNumberId,operationId,machineId,headName,machineLocator):
	
	system.perspective.print('Get Substitute Component Details ----------------START------------------------------------>  ')
	system.perspective.print('selectedWoNumberId :' + str(selectedWoNumberId))
	system.perspective.print('operationId :' + str(operationId))
	system.perspective.print('machineId :' + str(machineId))
	system.perspective.print('headName :' + str(headName))
	system.perspective.print('machineLocator :' + str(machineLocator))

	
	try:
		apiPath = "OperatorConsole/GetAttachedWorkFlowProcessComponentsWithSubstituteForOperatorConsole"
		url = URLPath + apiPath
		params = {
		  "workOrderId":selectedWoNumberId,
		  "operationId": operationId,
		  "machineId":machineId,
		  "headerName":headName,
		  "machineLocator":machineLocator
			}

		jsonParams = system.util.jsonEncode(params)			 
		result = 1
		system.perspective.print('jsonParams :' + str(jsonParams))
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)			
		except:	
			result = 0
			postReturn = ''
			pass

		system.perspective.print('postReturn :' + str(postReturn))
		
		try:
			resultData= system.util.jsonDecode(postReturn)		
		except:
			resultData = []	

		k=1
		dataList = []

		for i in resultData:
			SrNo = k
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
			UnitUsage = i.get("UnitUsage")
			BomId = i.get("BomId")
			MaterialAvailableWorkOrderID = PDAComponentScanning.isNotBlank(i.get("MaterialAvailableWorkOrderID"))
			RemainLotQuantity = PDAComponentScanning.isNotBlank(i.get("RemainLotQuantity"))
			CurrentRemainingQty = PDAComponentScanning.isNotBlank(i.get("CurrentRemainingQty"))
			MaterialAvailableWorkOrderNo = PDAComponentScanning.isNotBlank(i.get("MaterialAvailableWorkOrderNo")) 
			system.perspective.print('MaterialAvailableWorkOrderID :' + str(MaterialAvailableWorkOrderID) + str(" RemainLotQuantity : "+ str(RemainLotQuantity) ))
			
			today = system.date.now()
			TodayDate= system.date.format(today, "dd/MM/yyyy,HH:mm:ss")
			
			if ERPExpirationDate >= TodayDate or ERPExpirationDate == None or str(ERPExpirationDate).strip().lower() == str("None").strip().lower():
				IsExpired = 0
			else:
				IsExpired = 1
				
			IsExpired = 0
	
			myList = [SrNo,WorkOrderNo,PartNowithRevision,LotNo,consumeQty,bomdetailsId,ItemId,IsExpired,UnitUsage,BomId,MaterialAvailableWorkOrderID,RemainLotQuantity,CurrentRemainingQty,MaterialAvailableWorkOrderNo]
			dataList.append(myList)
			k = k+1

		headers = ["SrNo","WorkOrderNo","PartNowithRevision","LotNo","consumeQty","bomdetailsId","ItemId","IsExpired","UnitUsage","BomId","MaterialAvailableWorkOrderID","RemainLotQuantity","CurrentRemainingQty","MaterialAvailableWorkOrderNo"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		print 'resultDetails',resultDetails
		system.perspective.print('resultDetails :' + str(resultDetails))
		system.perspective.print('Get Substitute Component Details ----------------END---------------------------------->  ')
		return resultDetails
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: PDA :: getSubstitueComponentDetails :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		system.perspective.print('errorMessage :' + str(errorMessage))
		Authentication.exceptionLogger(errorMessage)

def postScannedComponentDetails(selectedWorkorderId,selectedLineId,BomDetailsId,selectedItemId,scannedLotNumber,scannedLotQty,userId,BobbinId,scannedHeadName,operationId,machineId,machineLocator,labelType,scannedVendorLot,scannedRMBomId,scannedRMUnitUsage):
	try:
		apiPath = "OperatorConsole/CreateOperatorConsoleComponent"
		url = URLPath + apiPath		

		writeData = {	
					"machineMaterialLoading": 
											{
												"workorderID": selectedWorkorderId,
												"lineID": selectedLineId,
												"bomDetailsID": BomDetailsId,
												"itemId": selectedItemId,
												"transferComponentLot": str(scannedLotNumber),
												"feedQuantity": scannedLotQty,
												"bobbinsId": BobbinId,
												"headName": scannedHeadName,
												"operationId": operationId,
												"machineId": machineId,
												"createdBy": userId,
												"machineLocator" : str(machineLocator),
												"labelType": labelType,
												"vendorLot": str(scannedVendorLot),
												"unitUsage": scannedRMUnitUsage,
												"bomId": scannedRMBomId
	    									}
					}


		jsonParams = system.util.jsonEncode(writeData)
		system.perspective.print('jsonParams in feeding material to machine is :' + str(jsonParams))	
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
		except:
			result = 0	
			import sys, os
			exc_type, exc_obj,tb = sys.exc_info()
			lineno = tb.tb_lineno
			errorMessage = "'Exception :: PDA :: postScannedComponentDetails :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
			system.perspective.print(errorMessage+' || Line No :' + str(lineno))
			Authentication.exceptionLogger(errorMessage)
		return result
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: PDA :: postScannedComponentDetails :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)
		

def isNotBlank(myString):
	try:
		myString=str(myString).strip()
		if myString=='' or str(myString).lower()==str('None').lower() or str(myString)==None or str(myString).lower()==str('null').lower() or int(myString) == "": 
			myString=0
		return myString
	except:
		return myString
		

def getHeadDetailsbyMachineId(machineId):
	try:
		apiPath= "OperatorConsole/GetMachineHead?MachineId="+str(machineId)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		print 'data',data
		if data.good:    
			resultData=data.json
		print 'resultData',resultData
		dataList = []
		k=1
		for i in resultData:
			SrNo = k
			BobbinsNo = i.get("Bobbins")
			BobbinsId = i.get("BobbinsId")
			HeadsName = i.get("HeadsName")
			
			myList = [SrNo,BobbinsNo,BobbinsId,HeadsName]
			dataList.append(myList)	
			k=k+1
		
		headers = ["SrNo","BobbinsNo","BobbinsId","HeadsName"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		print 'resultDetails',resultDetails
		return resultDetails
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: PDA Component Scanning:: Get Head Details:"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)
		
	
#-------Validation Check This is used to check the validation in production operator Console Screen---->
def getChangeoverDetails(workorderId,lineId,Acknowledgement,userId):
	try:
		url= URLPath + "OperatorConsole/GetWorkOrderChangeOver?WorkorderId="+str(workorderId)+"&LineID="+str(lineId)+"&MoveMaterialInNextWorkOrder="+str(Acknowledgement)+"&CreatedBy="+ str(userId)
		
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		print 'resultData',resultData
		
		
		headers =["SrNo","WorkorderNo","PrevPartNumber","CurrentPartNumber","MachineName","ComponentName","TransferComponentLot","AvailableToReturn","PartNumberChanged","WorkFlowChanged","Acknowledgement","ValidateMFGLine","MFGLineDifferent","PrevMFGLine","CurrentMFGLine","DataProcessing","IsScrapBackflushed"]
		dataList=[]
		if resultData == None:
			print 'Allow To start Workorder'
			return 1
		else:
			k=1
			for i in resultData:
				SrNo = k
				PrevWorkorder = i.get('PrevWorkOrderName')
				PrevPartNumber = i.get('PrevPartNumber')
				CurrentPartNumber = i.get('PartNumber')
				MachineName = i.get('MachineName')
#				ComponentName = i.get("PartNumber1")
				ComponentName = i.get("Material")
				TransferComponentLot = i.get('TransferComponentLot')
				AvailableToReturn=i.get('RemainLotQuantity')
				PartNumberChanged = i.get("PartNumberChanged")
				WorkFlowChanged = i.get("WorkFlowChanged")
				Acknowledgement=i.get('MaterialCopyConfirmation')
				ValidateMFGLine = i.get('ValidateMFGLine')
				MFGLineDifferent= i.get('MFGLineDifferent')
				PrevMFGLine = i.get('PrevMFGLine')
				CurrentMFGLine = i.get('MFGLine')
				DataProcessing = i.get('DaTaProcessing')
				IsScrapBackflushed = i.get('BackFlushQty')

				myList = [SrNo,PrevWorkorder,PrevPartNumber,CurrentPartNumber,MachineName,ComponentName,TransferComponentLot,AvailableToReturn,PartNumberChanged,WorkFlowChanged,Acknowledgement,ValidateMFGLine,MFGLineDifferent,PrevMFGLine,CurrentMFGLine,DataProcessing,IsScrapBackflushed]
				dataList.append(myList)
				k = k+1
			resultDetails = system.dataset.toDataSet(headers,dataList)
			print 'resultDetails',resultDetails
			return resultDetails
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception ::ChangeOver Details:"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)

def getMaterialAlerts(workorderId,lineId):
	try:
		apiPath = "OperatorConsole/GetMachineComponentEmptyAlert?WorkorderId="+str(workorderId)+"&LineID="+str(lineId)+"&MachineId=0&HeadName=string"
		url = URLPath + apiPath
		
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		print 'data',data
		if data.good:    
			resultData=data.json
		print 'resultData',resultData
		dataList = []
		k=1
		for i in resultData:
			SrNo = k
			MachineName = i.get("MachineName")
			HeadName = i.get("HeadName")
			MachineName = MachineName +'_'+HeadName
			ComponentName = i.get("ComponentName")
			RemainLotQuantity = i.get("RemainLotQuantity")
			if float(RemainLotQuantity) <= float(0):
				myList = [SrNo,MachineName,ComponentName,RemainLotQuantity] 		
				dataList.append(myList)	
				k=k+1
			else:
				pass
		
		headers = ["SrNo","MachineName","ComponentName","RemainLotQuantity"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		print 'resultDetails',resultDetails
		return resultDetails
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: Get Material Alerts :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)
		


#------------Used for Material Return Details ------------------------------>
def GetRequestedComponentsforMaterialReturn(selectedWorkorderId,selectedLineId):   
#	url= URLPath + "OperatorConsole/GetOperatorConsoleMaterialRequest?WorkOrderId="+str(selectedWorkorderId)+"&LineId="+str(selectedLineId)
	url= URLPath + "OperatorConsole/GetMaterialToReturn?WorkOrderId="+str(selectedWorkorderId)+"&LineId="+str(selectedLineId)
	
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)
	resultData= system.util.jsonDecode(data)
	print 'resultData',resultData
	headers = ["bomdetailsId","ItemId","ComponentName","UnitUsage"]
	dataList=[]
	for i in resultData:
		bomdetailsId = i.get('BomDetailsId')
		ItemId = i.get('itemId')
		Material = i.get("Material")
		unitUsage = 1
		
		myList = [bomdetailsId,ItemId,Material,unitUsage]		
		dataList.append(myList)	
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails
	
	
#----Used in Material Return Screen--------------------->	
def getAvailableLotToReturn(selectedWorkorderId,selectedItemId,selectedLineId,bomDetailsId,operationId,machineId,scannedHeadName,scannedLotNumber,labelType,scannedVendorLot):
	try:

		apiPath = "MaterialMovement/GetMaterialLoadedDetails"
		url = URLPath + apiPath		
		
		writeData = {	
		    	 "operatorMaterialReturn": {
						  	      "workorderID": selectedWorkorderId,
						  	      "lineID": selectedLineId,
						  	      "bomDetailsID": bomDetailsId,
						  	      "itemId": selectedItemId,
						  	      "operationId": operationId,
						  	      "machineId": machineId,
						  	      "headName": scannedHeadName,
						  	      "transferComponentLot": scannedLotNumber,
						  	      "VendorLot": scannedVendorLot,
						  	      "LabelType": labelType
										}
		}
		
		
		jsonParams = system.util.jsonEncode(writeData)	
		system.perspective.print("jsonParams view Return Lot to View :" + str(jsonParams))
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
		except:		
			result = 0
			import sys, os
			exc_type, exc_obj,tb = sys.exc_info()
			lineno = tb.tb_lineno
			errorMessage = "'Exception :: PDA :: Get PrintTemplate :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
			system.perspective.print(errorMessage+' || Line No :' + str(lineno))
			Authentication.exceptionLogger(errorMessage)
			
		resultData = system.util.jsonDecode(postReturn)
		
		system.perspective.print('Available Vendor Lot :' + str(resultData))
		dataList = []
		k=1
		for i in resultData:
			SrNo = k
			componentName = i.get("ProdItemName")
			lotNumber = i.get("TransferComponentLot")
#			TotalLoaded = i.get("loaded")
#			TotalBackflushed = PDAComponentScanning.isNotBlank(i.get("Consumed"))
#			Totalreturned = i.get("Returned")
			BomDetailsId = i.get("BomDetailsId")
			AvailableToReturn=PDAComponentScanning.isNotBlank(i.get("RemainLotQty"))
			VendorLot = PDAComponentScanning.isNotBlank(i.get("VendorLot"))

#			myList = [SrNo,componentName,lotNumber,TotalLoaded,TotalBackflushed,AvailableToReturn,Totalreturned,BomDetailsId,VendorLot]
			myList = [SrNo,componentName,lotNumber,AvailableToReturn,BomDetailsId,VendorLot]		
			dataList.append(myList)	
			k=k+1

		headers = ["SrNo","ComponentName","LotNumber","AvailableToReturn","BomDetailsId","VendorLot"]
#		headers = ["SrNo","ComponentName","LotNumber","TotalLoaded","TotalBackflushed","AvailableToReturn","Totalreturned","BomDetailsId","VendorLot"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: PDA :: GetAvailable Lot :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)
	
def postReturnMaterialToERP(selectedWorkorderId,selectedLineId,BomDetailsId,ItemId,scannedLotNumber,scannedLotQty,returnLocation,userId,operationId,machineId,scannedHeadName,labelType,scannedVendorLot,scannedMachineLocator,scannedSubInventory):
	try:
		if int(returnLocation) == int(1):
			returnLocation = 6
		else:
			returnLocation = 5

		apiPath = "OperatorConsole/OperatorConsoleReturnComponent"
		url = URLPath + apiPath		

		writeData = {	
		    	"operatorMaterialReturn": {
									        "workorderID": selectedWorkorderId,
									        "lineID": selectedLineId,
									        "bomDetailsID": BomDetailsId,
									        "itemId": ItemId,
									        "TransferComponentLot": str(scannedLotNumber),
									        "returnQuantity": scannedLotQty,
									        "createdBy": userId,
									        "MaterialMovementTypeId": int(returnLocation),
								            "operationId": operationId,
								            "machineId": machineId,
								            "headName": str(scannedHeadName),
								            "VendorLot":scannedVendorLot,
								            "LabelType":labelType,
							                "MachineLocator": scannedMachineLocator,
											"ToSubInventory": scannedSubInventory
		  	}
		}
		
		jsonParams = system.util.jsonEncode(writeData)	
		system.perspective.print('jsonParams Return Material  :' + str(jsonParams))
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
		except:		
			result = 0
			import sys, os
			exc_type, exc_obj,tb = sys.exc_info()
			lineno = tb.tb_lineno
			errorMessage = "'Exception :: PDA :: postReturnMaterialToERP :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
			system.perspective.print(errorMessage+' || Line No :' + str(lineno))
			Authentication.exceptionLogger(errorMessage)
		return result
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: PDA :: postReturnMaterialToERP :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)

def getPrintingTemplate(selectedWorkorderId,selectedLineId,BomDetailsId,ItemId,scannedLotNumber,scannedLotQty,returnLocation,returnQRCodeString,userId):
	try:
		if int(returnLocation) == int(1):
			returnLocation = 6
		else:
			returnLocation = 5
		system.perspective.print('Inside the Function calling ------>')
		apiPath = "OperatorConsole/GetMaterialReturnPrintTemplate"
		url = URLPath + apiPath		

		writeData = {	
		    	"operatorMaterialReturn": {
									  	    "workorderID": selectedWorkorderId,
									  	    "lineID": selectedLineId,
									  	    "bomDetailsID": BomDetailsId,
									  	    "itemId": ItemId,
									  	    "transferComponentLot": str(scannedLotNumber),
									  	    "returnQuantity": str(scannedLotQty),
									  	    "createdBy": userId,
									  	    "materialMovementTypeId": returnLocation,
									  	    "qR1": str(returnQRCodeString),
									  	    "printTemplate": "string"
		  	  }
		}

		jsonParams = system.util.jsonEncode(writeData)	

		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
		except:		
			result = 0
			import sys, os
			exc_type, exc_obj,tb = sys.exc_info()
			lineno = tb.tb_lineno
			errorMessage = "'Exception :: PDA :: Get PrintTemplate :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
			system.perspective.print(errorMessage+' || Line No :' + str(lineno))
			Authentication.exceptionLogger(errorMessage)
			
		resultData = system.util.jsonDecode(postReturn)

		if resultData!=None and resultData!='' and str(resultData)!='None':
			printTemplate=resultData['operatorMaterialReturn']
		
			printTemplateData =str(printTemplate[u'PrintTemplate'])
#		printTemplate =printTemplateData['PrintTemplate']
			system.perspective.print('printTemplate sagar  :' + printTemplateData)
		return printTemplateData
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: PDA :: Get PrintTemplate :"+ str(exc_obj) + " Line No: "+ str(lineno)
		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)

def postPrintingHistory(selectedWorkorderId,selectedLineId,BomDetailsId,ItemId,scannedLotNumber,scannedLotQty,returnLocation,returnQRCodeString,userId):
	try:
		if int(returnLocation) == int(1):
			returnLocation = 6
		else:
			returnLocation = 5

		apiPath = "OperatorConsole/GetMaterialReturnPrintTemplateHistory"
		url = URLPath + apiPath		

		writeData = {	
		    	"operatorMaterialReturn": {
									  	    "workorderID": selectedWorkorderId,
									  	    "lineID": selectedLineId,
									  	    "bomDetailsID": BomDetailsId,
									  	    "itemId": ItemId,
									  	    "transferComponentLot": str(scannedLotNumber),
									  	    "returnQuantity": str(scannedLotQty),
									  	    "createdBy": userId,
									  	    "materialMovementTypeId": returnLocation,
									  	    "qR1": str(returnQRCodeString),
									  	    "printTemplate": str(returnQRCodeString)
		  			  	  }
		}
		
		jsonParams = system.util.jsonEncode(writeData)	
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
		except:
			result = 0
			import sys, os
			exc_type, exc_obj,tb = sys.exc_info()
			lineno = tb.tb_lineno
			errorMessage = "'Exception :: PDA :: postReturnMaterialToERP :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
			system.perspective.print(errorMessage+' || Line No :' + str(lineno))
			Authentication.exceptionLogger(errorMessage)
		return result
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: PDA :: postReturnMaterialToERP :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)

def getAllPrintedHistory(selectedWorkorderId,selectedLineId,userId):
	try:
		apiPath = "OperatorConsole/GetMaterialReturnPrintHistory/"+str(selectedWorkorderId)+"/"+str(selectedLineId)+"/"+str("1")+"/"+str(userId)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		print 'data',data
		if data.good:    
			resultData=data.json
		print 'resultData',resultData
		dataList = []
		for i in resultData:
			id = i.get("id")
			PartNo = i.get("PartNo")
			Revision = i.get("Revision")
			WorkOrderNo = i.get("WorkOrderNo")
			ComponentName = PartNo +'_'+Revision
			LotNumber = i.get("Lot")
			PrintedOn = i.get("CreatedOn")
			CreatedBy= i.get("CreatedBy")
			Reprint = 'Reprint'
					
			myList = [id,WorkOrderNo,ComponentName,LotNumber,PrintedOn,CreatedBy,Reprint]
			dataList.append(myList)	
		
		headers = ["id","WorkOrderNo","ComponentName","LotNumber","PrintedOn","CreatedBy","Reprint"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		print 'resultDetails',resultDetails
		return resultDetails
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: PDA :: getAllPrintedHistory Lot :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)


def getReprintTemplate(PrintHistoryId,isPrint,NoOfPrint,PrinterIP,Port):
	try:
		dslist=[]
		apiPath = "OperatorConsole/GetMaterialReturnPrintHistory/"+str(PrintHistoryId)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		print 'data',data
		resultData=None
		if data.good:    
			resultData=data.json
			system.perspective.print('resultDetails :'+ (resultData))
		dslist.append(resultData)
		if isPrint ==0:
			return resultData
		else:
			resultData=str(resultData)
			printResult=Print.printingServer(resultData,NoOfPrint,PrinterIP,Port)
			return printResult
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: PDA :: Get ReprintTemplate Lot :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)

def getSubstitueComponentDetails_WorkOrderIdWise(userId,selectedWorkorderId):
	try:
		apiPath = "OperatorConsole/GetAttachedWorkFlowProcessComponentsWithSubstituteForOperatorConsole_WorkOrderIdWise/"+str(userId)+"/"+str(selectedWorkorderId)
		url = URLPath + apiPath
		resultData=None
		client = system.net.httpClient() 
		data = client.get(url)
		if data.good:
			resultData=data.json
		dataList = []
		k=1
		dataList = []

		for i in resultData:
			SrNo = k
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
			MachineName = i.get("MachineName")
			Operation = i.get("Operations")
			ScannedVendorLot = i.get("ScannedVendorLot")
			myList = [SrNo,WorkOrderNo,PartNowithRevision,LotNo,consumeQty,bomdetailsId,ItemId,IsExpired,MachineName,Operation,ScannedVendorLot]
			dataList.append(myList)
			k = k+1

		headers = ["SrNo","WorkOrderNo","PartNowithRevision","LotNo","consumeQty","bomdetailsId","ItemId","IsExpired","MachineName","Operation","ScannedVendorLot"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: PDA :: GetAttachedWorkFlowProcessComponentsWithSubstituteForOperatorConsole_WorkOrderIdWise :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		Authentication.exceptionLogger(errorMessage)	
		print 	errorMessage
		return None


def getWoNumbersByLineForReturnMaterial(userId,selectedLine):
	try:
		scriptName = 'getWoNumbersByLineForReturnMaterial'
		apiPath = "OperatorConsole/GetOperatorConsoleWorkordersForMaterialReturn?UserId="+str(userId)+"&LineId="+str(selectedLine)
		url = URLPath + apiPath
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)	
		resultData= system.util.jsonDecode(data)

		dataList=[]
		for i in resultData:
			WorkorderStatus = i.get('WorkorderStatus')
			WorkorderType = i.get('WorkorderType')
			workOrderId = i.get("ID")
			woNumber = i.get("WorkOrderNo")
			myList = [WorkorderStatus,WorkorderType,workOrderId,woNumber] 		
			dataList.append(myList)
		headers = ["WorkorderStatus","WorkorderType","WorkOrderId","WoNumber"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails	
	except:
		import sys, os
		errorMessage= scriptName  +' Exception : '+  str(sys.exc_info()[1])
		system.perspective.print("errorMessage :" + str(errorMessage))
		Authentication.exceptionLogger(errorMessage)

def getWoNumbersByLine(userId,selectedLine):
	apiPath = "OperatorConsole/GetOperatorConsoleWorkordersPDA?UserId="+str(userId)+"&LineId="+str(selectedLine)  
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)	
	resultData= system.util.jsonDecode(data)

	dataList=[]
	for i in resultData:
		WorkorderType = i.get("WorkorderType")
		workOrderId = i.get("ID")
		woNumber = i.get("WorkOrderNo")
		myList = [WorkorderType,workOrderId,woNumber] 		
		dataList.append(myList)
	headers = ["WorkorderType","WorkOrderId","WoNumber"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails


def GetCurrentRuningWorkorderDetails(selectedLineId,selectedWorkorderId):
	apiPath = "OperatorConsole/GetCurrentRunningWorkorderDetails/"+str(selectedLineId)+"/"+str(selectedWorkorderId)
	url = URLPath + apiPath

	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)	
	resultData= system.util.jsonDecode(data)

	dataList=[]
	for i in resultData:
		currentRunningWorkorder = i.get("WorkOrderName")
		currentRunningWorkOrderID = i.get("WorkOrderID")
		WorkOrderStatusId = i.get("WorkOrderStatusId")
		currentRunningWorkorderLineId = i.get("LineId")
		currentRunningworkordersItemId = i.get("ItemId")
		currentRunningworkordersRawMaterial = i.get("PartNumber")
		currentRunningworkordersOperationId = i.get("OperationId")
		currentRunningworkordersMachineId = i.get("MachineId")

		myList = [currentRunningWorkorder,currentRunningWorkOrderID,WorkOrderStatusId,currentRunningWorkorderLineId,currentRunningworkordersItemId,currentRunningworkordersRawMaterial,currentRunningworkordersOperationId,currentRunningworkordersMachineId] 		
		dataList.append(myList)
	headers = ["currentRunningWorkorder","currentRunningWorkOrderID","WorkOrderStatusId","currentRunningWorkorderLineId","currentRunningworkordersItemId","currentRunningworkordersRawMaterial","currentRunningworkordersOperationId","currentRunningworkordersMachineId"] 		
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails

def GetCurrentRuningWorkorderDetailsByMachineWise(selectedLineId,selectedWorkorderId,scannedMachineId):
	apiPath = "OperatorConsole/GetCurrentRunningWorkorderDetails/"+str(selectedLineId)+"/"+str(selectedWorkorderId)
	url = URLPath + apiPath
	
	system.perspective.print('API Url is :' + str(url))
	system.perspective.print('API Method is : Get')	
	
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)	
	resultData= system.util.jsonDecode(data)

	dataList=[]
	for i in resultData:
		currentRunningworkordersMachineId = i.get("MachineId")
		if int(scannedMachineId) == int(currentRunningworkordersMachineId):
			currentRunningWorkorder = i.get("WorkOrderName")
			currentRunningWorkOrderID = i.get("WorkOrderID")
			WorkOrderStatusId = i.get("WorkOrderStatusId")
			currentRunningWorkorderLineId = i.get("LineId")
			currentRunningworkordersItemId = i.get("ItemId")
			currentRunningworkordersRawMaterial = i.get("PartNumber")
			currentRunningworkordersOperationId = i.get("OperationId")
			currentRunningworkordersMachineId = i.get("MachineId")

			myList = [currentRunningWorkorder,currentRunningWorkOrderID,WorkOrderStatusId,currentRunningWorkorderLineId,currentRunningworkordersItemId,currentRunningworkordersRawMaterial,currentRunningworkordersOperationId,currentRunningworkordersMachineId] 		
			dataList.append(myList)

	headers = ["currentRunningWorkorder","currentRunningWorkOrderID","WorkOrderStatusId","currentRunningWorkorderLineId","currentRunningworkordersItemId","currentRunningworkordersRawMaterial","currentRunningworkordersOperationId","currentRunningworkordersMachineId"] 		
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails

#Material Return New Functions
def getMachineListForSelectedWO(userId,selectedLineId,selectedWorkorderId):
	apiPath = 'ProductionOperatorConsole/GetPDAWorkorderdetailsPDAMaterialReturn/'+str(userId)+'/'+str(selectedLineId)+'/'+str(selectedWorkorderId)+'/string'
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)	
	resultData= system.util.jsonDecode(data)
	myList=[]
	for i in resultData:
		machineName = i.get("MachineName")
		myList.append(machineName)
	return myList

def getSingleMachineDetailsforMaterialReturn(userId,selectedLineId,selectedWorkorderId,scannedMachineCode):
	apiPath = 'ProductionOperatorConsole/GetSingleOperationDetailsPDAMaterialReturn/'+str(userId)+'/'+str(selectedLineId)+'/'+str(selectedWorkorderId)+'/'+str(scannedMachineCode)+'/parameter'
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)
	resultData= system.util.jsonDecode(data)
	return resultData


def IsAllowToCompleteWorkOrder(selectedWorkorderId,selectedLineId,ActualRunningWOQty):
	try:
		ActualRunningWOQty = int(ActualRunningWOQty)
		apiPath = "OperatorConsole/ValidateTotalConsumptionAgainstProduction?WorkorderId="+str(selectedWorkorderId)+"&Lineid="+str(selectedLineId)+"+&FGQty="+str(ActualRunningWOQty)
		url = URLPath + apiPath
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)	
		resultData= system.util.jsonDecode(data)
		dataList=[]
		k=1

		for i in resultData:
			SrNo = k
			IsValid = i.get("IsValid")
			EquipmentCode =  i.get("EquipmentCode")
			HeadName =  i.get("HeadName")
			MachineName = EquipmentCode+'|'+HeadName
			ComponentName =  i.get("ComponentName")
			RequiredQtytoFeed =  i.get("RequiredQty")
			k = k+1
			
			myList = [SrNo,IsValid,MachineName,ComponentName,RequiredQtytoFeed]
			dataList.append(myList)

		headers =  ['SrNo','IsValid','MachineName','ComponentName','RequiredQtytoFeed']
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:
		pass

#Reserve Material Before Material Return

def reserveMaterialBeforeMaterialReturn(selectedLineId,selectedWorkorderId,scannedMachineId):
	try:
		apiPath = "OperatorConsole/OperatorConsoleReserveMaterialBeforeReturn"
		url = URLPath + apiPath
		params = {
		 		    "operatorMaterialReturn": {
											    "workorderID": selectedWorkorderId,
											    "lineID": selectedLineId,
											    "bomDetailsID": 0,
											    "itemId": 0,
											    "operationId": 0,
											    "machineId": scannedMachineId,
											    "bobbinsId": 0,
											    "headName": "string",
											    "transferComponentLot": "string",
											    "machineLocator": "string",
											    "returnQuantity": 0,
											    "createdBy": 0,
											    "materialMovementTypeId": 0,
											    "qR1": "string",
											    "printTemplate": "string",
											    "labelType": 0,
											    "vendorLot": "string",
											    "toSubInventory": "string",
											    "message": "string"
											  }
		   		}
		
		jsonParams = system.util.jsonEncode(params)			 
		result = 1
		system.perspective.print('jsonParams Material Reserve Before Material Return : ' + str(jsonParams))
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


		print 'postReturn ',postReturn
		resultData = system.util.jsonDecode(postReturn)
		print 'resultData ',resultData
		DataToGetDetails =resultData['operatorMaterialReturn']
		message =str(DataToGetDetails[u'message'])
		print 'message ',message
		system.perspective.print('message : ' + str(message))
		return message
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: PDA :: getValidationStatus :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)