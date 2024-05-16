import re
import json
import urllib2, urllib
import datetime
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
#URLPath = system.tag.read("[default]JMES_InternalTags/urlSITAPI").value

def getshiftId():
	apiPath ="OperatorConsole/GetCurrentShiftId"
	url = URLPath + apiPath
#	try:
#		system.perspective.print("API URL is: "+str(url))
#		system.perspective.print("API Method is: Get ")
#	except:
#		pass
#	system.perspective.print('API Url is :' + str(url))
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
 	Data = resultData[0]
 	ShiftId = Data.get('ShiftId')
 	print ShiftId
	return ShiftId
	

def isNotBlank(myString):
	try:
		myString=str(myString).strip()
		if myString=='' or str(myString).lower()==str('None').lower() or str(myString)==None or str(myString).lower()==str('null').lower():
			myString=''	
		return myString
	except:
		return myString

def getWorkOrderQty(WorkOrderId,FGCount):
	try:
		scriptName = "getOprConsoleMaterialRequestDetails"
		apiPath = "OperatorConsole/MaterialRequestFromOperatorConsole?WorkOrderId="+str(WorkOrderId)+"&FGQty="+str(FGCount)
		url = URLPath + apiPath
		try:
			system.perspective.print("API URL is: "+str(url))
			system.perspective.print("API Method is: Get ")
		except:
			pass
		system.perspective.print('API Url is :' + str(url))
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		return resultData
	except:
		return ''
		pass

def getExpiredComponentsDetails(workOrderId,FGCount):
	try:
		scriptName = "Get Expired Components Details"
		apiPath = "OperatorConsole/MaterialRequestFromOperatorConsole?WorkOrderId="+str(workOrderId)+"&FGQty="+str(FGCount)
		url = URLPath + apiPath
		try:
			system.perspective.print("API URL is: "+str(url))
			system.perspective.print("API Method is: Get ")
		except:
			pass
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		dataList = []
		j=1
		for i in resultData:
			ComponentExpiryDate = i.get("ComponentExpiryDate")
			print 'ComponentExpiryDate',ComponentExpiryDate
			today = system.date.now()
			TodayDate= system.date.format(today, "dd/MM/yyyy,HH:mm:ss")
			
			ComponentExpiryDateDefault = "01/01/1900,00:00:00"
			if ComponentExpiryDate >= TodayDate or ComponentExpiryDate == None or ComponentExpiryDate == ComponentExpiryDateDefault:
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
				if ComponentExpiryDate == ComponentExpiryDateDefault:
					ComponentExpiryDate = 'Not Expired'
				else:
					pass
					
				
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
		try:
			system.perspective.print("API URL is: "+str(url))
			system.perspective.print("API Method is: Get ")
		except:
			pass
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
			
		dataList = []
		j=1
		for i in resultData:	
			srNo = j  # START --> TO Display On MaterialRequestScreen
			workOrderNumber = i.get("WorkOrderNumber")
			componentName = MaterialRequestAPI.isNotBlank(i.get("PartNumber"))
			componentDescription = MaterialRequestAPI.isNotBlank(i.get("Description"))
			uom = i.get("UOM")
			bomQty = i.get("BOMQTY")
			system.perspective.print('componentDescription :' + str(componentDescription) + ' bomQty :' + str(bomQty))
			totalPendingRequestCount = i.get("TotalPendingReqCount")
			totalPendingReqestedQty = i.get("TotalPendingReqestedQty")
			totalRequiredQty = i.get("TotalRequiredQty")
			spqSize = i.get("SPQ")
			spqRequired = i.get("SPQRequired")
			IsSelected = 1   # END --> TO Display On MaterialRequestScreen
			partNumberId = i.get("PartNumberId")  #START
#---------------This are used to Post in Payload-----------------------------------------
			IO = MaterialRequestAPI.isNotBlank(i.get("FactoryName"))       # START --> Used to Post in Payload
			woPartNumber = MaterialRequestAPI.isNotBlank(i.get("WoPartNumber"))
			partRevision = MaterialRequestAPI.isNotBlank(i.get("PartRevision"))
			datetime = ""
			woqty = MaterialRequestAPI.isNotBlank(i.get("TotalRequiredQty"))
			requestComponentCode = MaterialRequestAPI.isNotBlank(i.get("RequestComponentCode"))
			componentRevison = MaterialRequestAPI.isNotBlank(i.get("ComponentRevison"))
			mfgLine =  MaterialRequestAPI.isNotBlank(i.get("MFGLINE"))
			locatorName = MaterialRequestAPI.isNotBlank(i.get("LocatorName"))
			transferOrganization = i.get("TransferOrganization")
			subInventoryCode = MaterialRequestAPI.isNotBlank(i.get("SubInventoryCode"))
			requestedDateTime = MaterialRequestAPI.isNotBlank(i.get('PlannedCompletionDate'))
			employeeNumber = MaterialRequestAPI.isNotBlank(i.get("EmployeeNumber"))
			reason = MaterialRequestAPI.isNotBlank(i.get("Reason"))
			requestStatus = MaterialRequestAPI.isNotBlank(i.get("RequestStatus"))
			requestCloseddate = MaterialRequestAPI.isNotBlank(i.get("RequestCloseddate"))
			ledger = MaterialRequestAPI.isNotBlank(i.get("Ledger"))
			ou = MaterialRequestAPI.isNotBlank(i.get("OU"))
			workOrderType = MaterialRequestAPI.isNotBlank(i.get("WorkOrderType"))
			IsSubAssembly=MaterialRequestAPI.isNotBlank(i.get("IsSumbAssembly"))
			
			system.perspective.print('requestedDateTime : ' + str(requestedDateTime))

			if str(workOrderType) == str(1) and (str(IsSubAssembly).lower() == str("false").lower() or str(IsSubAssembly) == str(0)):
				workOrderType = 'Flow Schedule'
			elif str(workOrderType) == str(2):
				if str(locatorName).lower() == str("None").lower() or str(locatorName).lower() == str("Null").lower() or str(locatorName) == str(""):
					locatorName = ""
					subInventoryCode = ""
				else:
					pass
				workOrderType = 'Discrete Job'
				mfgLine =''
			elif str(workOrderType) == str(1) and (str(IsSubAssembly).lower() != str("false").lower() or str(IsSubAssembly) != str(0)):
				workOrderType = 'SubAssembly'
			else:
				pass

#			if str(workOrderType) == str(1) and (str(IsSubAssembly).lower() == str("false").lower() or str(IsSubAssembly) == str(0)):
#				 workOrderType = 'Flow Schedule'
#			elif str(workOrderType) == str(2):
#				 workOrderType = 'Discrete Job'
#			elif str(workOrderType) == str(1) and (str(IsSubAssembly).lower() != str("false").lower() or str(IsSubAssembly) != str(0)):
#				 workOrderType = 'SubAssembly'
#			else:
#				pass

			sourceCode  = "MES"
			SPQCount = i.get("SPQCount")
			IsSPQSizeAvailableFlag = i.get("isSPQNull")
			ComponentExpiryDate = i.get("ComponentExpiryDate")
			WorkOrderQty = i.get('WorkOrderQty')
			InHandQty = i.get("InHandQty")
			if str(InHandQty).lower() == str('Null').lower() or str(InHandQty).lower() == str('None').lower() or str(InHandQty).lower() == str(None).lower():
				 InHandQty = 0
			else:
				pass
			
			today = system.date.now()
			TodayDate= system.date.format(today, "dd/MM/yyyy,HH:mm:ss")
			
			ComponentExpiryDateDefault = "01/01/1900,00:00:00"
			if ComponentExpiryDate >= TodayDate or ComponentExpiryDate == None or ComponentExpiryDate == ComponentExpiryDateDefault:
				IsExpired = 0
				print 'IsExpired : ', IsExpired
			else:
				IsExpired = 1
			
			if IsSPQSizeAvailableFlag == int(1):
				IsSelected = 0
			else:
				IsSelected = 1

			myList = [srNo,workOrderNumber,componentName,componentDescription,uom,bomQty,totalPendingRequestCount,totalPendingReqestedQty,totalRequiredQty,spqSize,spqRequired,IsSelected,partNumberId,IO,woPartNumber,requestComponentCode,componentRevison,mfgLine,locatorName,transferOrganization,subInventoryCode,requestedDateTime,employeeNumber,reason,requestStatus,requestCloseddate,ledger,ou,workOrderType,sourceCode,SPQCount,IsSPQSizeAvailableFlag,IsExpired,partRevision,WorkOrderQty,InHandQty]
			print 'myList',myList
			dataList.append(myList)	
			j = j+1
		
		headers = ["SrNo","WorkOrderName","ComponentName","ComponentDescription","UOM","BOMQty","TPCount","TPQty","TRQty","PackingSize","SPQRequired","Action","PartID","IO","WoPartNumber","RequestComponentCode","ComponentRevison","MFGLine","LocatorName","TransferOrganization","SubInventoryCode","RequestedDateTime","EmployeeNumber","Reason","RequestStatus","RequestCloseddate","Ledger","OU","WorkOrderType","SourceCode","SPQCount","Flag","IsExpired","PartRevision","WorkOrderQty","InHandQty"]
		resultDetails = system.dataset.toDataSet(headers,dataList) 
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		

def saveRequestMaterial(resultData,workOrderId,userID,requestedDate,ShiftId):
	try:
		system.perspective.print('INSIE ShiftId is: '+ str(ShiftId))
		scriptName ="saveRequestMaterial"
		system.perspective.print('API resultData :' + str(resultData))
		resultDetails = system.util.jsonDecode(resultData)
		arrayJson = []
		
		for part in resultDetails:
			PackingSize = int(part[9])
			system.perspective.print('INSIE PackingSize is: '+ str(PackingSize))
			PartID = int(part[12])  
			SPQNumber =int(part[10])   
			IsSelected = int(part[11])
			IsExpired = part[32]
			
			SPQCount = SPQNumber* PackingSize
			system.perspective.print('INSIE SPQCount is: '+ str(SPQCount))
				
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
			    "lineId": ShiftId
				}
				
			arrayJson.append(jsonformat)
		
		system.perspective.print('arrayJson is: '+ str(arrayJson))

		params = {
				"operatorConsoleRequestMateriallist": arrayJson
				 }
			
		apiPath = "OperatorConsole/AddMaterialFromOperatorConsole"
		
		url = URLPath + apiPath	

		jsonParams = system.util.jsonEncode(params)

		result = 1
		try:
			system.perspective.print("API URL is: "+str(url))
			system.perspective.print("API InputData is: "+str(jsonParams))
			system.perspective.print("API Method is: Post")
		except:
			pass
		try:
			postReturn1 = system.net.httpPost(url,'application/json',jsonParams)
		except:		
			result = 0		
			pass
		return result
	except:
		system.perspective.print('Exception :: Save Material Request')
		exc_type, exc_obj,tb = sys.exc_info()
		errorMessage = "Error:"+ str(exc_obj)
		system.perspective.print(errorMessage)
		lineno = tb.tb_lineno
		system.perspective.print('LineNo is :' + str(lineno))

def submitRequestMaterial(resultData,workOrderId,userID,requestedDate,LineId):
	try:
		scriptName = "submitRequestMaterial"
		resultDetails = system.util.jsonDecode(resultData)
		arrayJson = []
		
		for part in resultDetails:	
			PackingSize = float(part[9])
			PartID = int(part[12])  
			SPQNumber =float(part[10])
			IsSelected = int(part[11])
			IsExpired = part[32]	
#			SPQCount = SPQNumber* PackingSize
			SPQCount = float(SPQNumber)* float(PackingSize)
			unitUsage =  float(part[5])
			system.perspective.print('INSIE Submitting unitUsage is: '+ str(unitUsage))
			if IsExpired ==int(1):
				IsExpired = True
			else:
				IsExpired = False
			
			if IsSelected != int(1) or IsSelected != True:
				IsSelected = False
			else:
				IsSelected = True
				
#				system.perspective.print('INSIE Submitting workOrderId is: '+ str(workOrderId))
#				system.perspective.print('INSIE Submitting PartID is: '+ str(PartID))
#				system.perspective.print('INSIE Submitting IsSelected is: '+ str(IsSelected))
#				system.perspective.print('INSIE Submitting requestedDate is: '+ str(requestedDate))
#				system.perspective.print('INSIE Submitting userID is: '+ str(userID))
#				system.perspective.print('INSIE Submitting IsExpired is: '+ str(IsExpired))
#				system.perspective.print('INSIE Submitting LineID  is: '+ str(LineId))
				jsonformat =  {
					"workOrderId": int(workOrderId),
					"partId": PartID, 
					"spqCount": SPQCount,
					"isSubmit": True,
					"isSelected": IsSelected,
					"requestDate": str(requestedDate),
					"createdBy": int(userID),
				    "isExpired": IsExpired,
				    "lineId": LineId,
				    "unitUsage": unitUsage
					}
					
				arrayJson.append(jsonformat)
		
		params = {
			"operatorConsoleRequestMateriallist": arrayJson
			 }
			 
		system.perspective.print('INSIE Submitting params is: '+ str(params))
		apiPath = "OperatorConsole/AddMaterialFromOperatorConsole"
		
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
def postOprConsoleMaterialRequestDetailsToERP(resultData,selectedWorkorderId,userID):
	try:
		resultDetails = system.util.jsonDecode(resultData)
		arrayJson = []
		
		componentDataList = []
		for i in resultDetails:		
			componentSelected = str(i[11])
			Flag = str(i[31])
			if (str(componentSelected) == str('1') and str(Flag)==str('0')):  
				IO = i[13]
				WorkOrderNumber = i[1]
				WoPartNumber = i[14]
				PartRevision = i[33]
				datetime = ""
				workorderQty =  i[34]
				requestComponentCode = i[15]
				componentRevison = i[16]
				SPQPackingSize = float(i[9])
				SPQNumber = float(i[10])
				SPQQuantity = SPQNumber* SPQPackingSize
				UOM = i[4]
				MFGLINE = i[17]
				locatorName = i[18]
				transferOrganization =i[19]
				subInventoryCode = i[20]
				requestedDateTime = i[21]
				employeeNumber = i[22]
				reason = i[23]
				requestStatus = i[24]
				requestCloseddate = i[25]
				ledger = i[26]
				OU = i[27]
				WorkOrderType = i[28]
				
				system.perspective.print('requestedDateTime : ' + str(requestedDateTime))
#				system.perspective.print('IO :' + str(IO))
#				system.perspective.print('WorkOrderNumber :' + str(WorkOrderNumber))
#				system.perspective.print('WoPartNumber :' + str(WoPartNumber))
#				system.perspective.print('PartRevision :' + str(PartRevision))
#				system.perspective.print('datetime :' + str(datetime))
#				system.perspective.print('workorderQty :' + str(workorderQty))
#				system.perspective.print('requestComponentCode :' + str(requestComponentCode))
#				system.perspective.print('componentRevison :' + str(componentRevison))
#				system.perspective.print('SPQPackingSize :' + str(SPQPackingSize))
#				system.perspective.print('SPQNumber :' + str(SPQNumber))
#				system.perspective.print('SPQQuantity :' + str(SPQQuantity))
#				system.perspective.print('UOM :' + str(UOM))
#				system.perspective.print('MFGLINE :' + str(MFGLINE))
#				system.perspective.print('locatorName :' + str(locatorName))
#				system.perspective.print('TransferOrganization :' + str(transferOrganization))
#				system.perspective.print('subInventoryCode :' +str (subInventoryCode))
#				system.perspective.print('requestedDateTime :' +str(requestedDateTime))
#				system.perspective.print('employeeNumber :'+str(employeeNumber))
#				system.perspective.print('reason :'+str(reason))
#				system.perspective.print('requestStatus :' +str(requestStatus))
#				system.perspective.print('requestCloseddate :'+str(requestCloseddate))
#				system.perspective.print('ledger :'+str(ledger))
#				system.perspective.print('OU :'+str(OU))
#				system.perspective.print('WorkOrderType :'+ str(WorkOrderType))

			
				payloadRequest = {
									"io": str(IO),
									"workOrderNumber": str(WorkOrderNumber),
									"partNumber": str(WoPartNumber),
									"revision": str(PartRevision),
									"datetime": "",
									"woqty": str(workorderQty),
									"requestComponentCode": str(requestComponentCode),
									"componentRevison": str(componentRevison),
									"qty": str(SPQQuantity),
									"uom": str(UOM),
									"mfgLine": str(MFGLINE),
									"locatorName": str(locatorName),
									"transferOrganization": str(transferOrganization),
									"subInventoryCode": str(subInventoryCode),
									"requestedDateTime": str(requestedDateTime), 
									"employeeNumber":str(employeeNumber), 		#for Future Reference
									"reason":str(reason), 						# for Future Reference
									"requestStatus":str(requestStatus), 		#for Future Reference
									"requestCloseddate": str(requestCloseddate),
									"ledger": str(ledger), 						# for Future Reference
									"ou": str(OU), 
									"workOrderType":str(WorkOrderType),
									"sourceCode": "MES",
								    "workOrderId": selectedWorkorderId,
								    "createdBy": userID
									
									}
									
				componentDataList.append(payloadRequest)
						
#		system.perspective.print('componentDataList :'+ str(componentDataList))
		apiPath = "MaterialRequest/AddMaterialRequest"
		url = URLPath + apiPath	
#		system.perspective.print('API Url is :' + str(url))
#		system.perspective.print('API componentDataList :' + str(componentDataList))
#		system.perspective.print('url :' + str(url))
		jsonParams = system.util.jsonEncode(componentDataList)
		try:
			system.perspective.print("API URL is: "+str(url))
			system.perspective.print("API InputData is: "+str(jsonParams))
			system.perspective.print("API Method is: Post ")
		except:
			pass
		submitresult = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
#			pass
		except:
			submitresult = 0
	   		import sys, os
	   		errorMessage=str(' Exception : '+  str(sys.exc_info()[1]))
	   		system.perspective.print('errorMessage :' + str(errorMessage))
	   		Authentication.exceptionLogger(errorMessage)
			pass
		return submitresult
	except:
   		import sys, os
   		errorMessage=str(' Exception : '+  str(sys.exc_info()[1]))
   		system.perspective.print('errorMessage :' + str(errorMessage))
   		Authentication.exceptionLogger(errorMessage)

def GetPrevioussubmittedRequest(selectedLineId,userId):
	try:
		scriptName = "API: Get Previous Requested Material Workorder List"
#		apiPath = "OperatorConsole/GetWorkordersForViewRequestsForOperatorConsole?LineId="+str(selectedLineId).strip()
		apiPath = "OperatorConsole/GetWorkordersForViewRequestsForOperatorConsole?LineId="+str(selectedLineId)+"&UserId="+str(userId)
		url = URLPath + apiPath
		try:
			system.perspective.print("API URL is: "+str(url))
#			system.perspective.print("API InputData is: "+str(jsonParams))
			system.perspective.print("API Method is: Get ")
		except:
			pass
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		print "resultData",resultData
		system.perspective.print('resultData :' + str(resultData))
		dataList = []
		j = 1
		for i in resultData:	
			SrNo = i.get("BatchId")
			LineName = i.get("LineName")
			WorkorderNo = i.get("WorkorderNo")
			BatchId = i.get("BatchId")
			ProductName = i.get("ProductName")
			RequestedDate = i.get("RequestedDate")
			system.perspective.print('RequestedDate :' + str(RequestedDate))
			WorkOrderId = i.get("WorkOrderId")
			RequestStatus = i.get("RMStatus")


			ViewDetails = ""
			BatchId = i.get("BatchId")
			j= j+1
			myList = [SrNo,LineName,WorkorderNo,ProductName,RequestedDate,WorkOrderId,RequestStatus,ViewDetails,BatchId]
			dataList.append(myList)
		
		headers = ["SrNo","LineName","WorkorderNo","ProductName","RequestedDate","WorkOrderId","RequestStatus","ViewDetails","BatchId"]
		resultDetails1 = system.dataset.toDataSet(headers,dataList)	
		resultDetails = system.dataset.sort(resultDetails1, 'RequestedDate', False)
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)

def GetsubmitedRequest(selectedBatchId):
	try:
		scriptName = "API: Get Previous Requested Material Workorder List"
		apiPath = "OperatorConsole/GetWorkordersMaterialRequestsForOperatorConsole?RequestBatchId="+str(selectedBatchId)
		url = URLPath + apiPath
		try:
			system.perspective.print("API URL is: "+str(url))
#			system.perspective.print("API InputData is: "+str(jsonParams))
			system.perspective.print("API Method is: Get ")
		except:
			pass
#		system.perspective.print('API Url is :' + str(url))
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		print "resultData",resultData
		dataList = []
		j = 1
		for i in resultData:	
			SrNo = j
			RequestedBatchID = str(i.get("RequestedBatchID"))
			ComponentName = str(i.get("PartNo"))
			Description = str(i.get("Description"))
			UOMName = str(i.get("UOMName"))
			BOMQTY = str(i.get("BOMQTY"))
			SPQ = str(i.get("SPQ"))
			SPQCount = str(i.get("SPQCount"))
			PartId = str(i.get("PartId"))
			DispatchStatus = str(i.get("DispatchStatus"))
			TotalTransferredQty= str(i.get("TRANSFERQTY"))
			
#			system.perspective.print('TotalTransferredQty :' + str(TotalTransferredQty))
#			
			if float(TotalTransferredQty) == float(0.00):
				DispatchStatus = 'Not Dispatched'
			elif float(SPQCount) == float(TotalTransferredQty) or  float(SPQCount) <= float(TotalTransferredQty):
				DispatchStatus = 'Dispatched'
			elif float(SPQCount) > float(TotalTransferredQty) and float(TotalTransferredQty) != float(0.00):
				DispatchStatus = 'Partially Dispatched'
			else:
				pass

			j= j+1
			myList = [SrNo,RequestedBatchID,ComponentName,Description,UOMName,BOMQTY,SPQ,SPQCount,PartId,DispatchStatus,TotalTransferredQty] 
			print myList
			dataList.append(myList)
		
		headers = ["SrNo","RequestedBatchID","ComponentName","Description","UOMName","BOMQTY","SPQ","SPQCount","PartId","DispatchStatus","TotalTransferredQty"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception :: component :: View Previosu Request :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
#		system.perspective.print(errorMessage+' || Line No :' + str(lineno))
		print(errorMessage+' || Line No :' + str(lineno))
		Authentication.exceptionLogger(errorMessage)
		resultData = []
		
#----------------------------------PDA Related Functions --------------------------------------------------
def getLinesByUserID(userID):
	apiPath = "OperatorConsole/GetOperatorConsoleLinesPDA?UserId="+str(userID)  
	url = URLPath + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
#			system.perspective.print("API InputData is: "+str(jsonParams))
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
		IsApplicableforPOU = i.get("ValidateLineSidePOU")	
		lineId = i.get("LineId")
		lineName = i.get("LineName")
		myList = [IsApplicableforPOU,lineId,lineName]
		dataList.append(myList)	
			
	headers = ["IsApplicableforPOU","LineId","LineName"]
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
	
	dataList=[]
	for i in resultData:
		workorderTypeId = i.get("WorkorderType")
		workOrderId = i.get("ID")
		woNumber = i.get("WorkOrderNo")
		myList = [workorderTypeId,workOrderId,woNumber] 		
		dataList.append(myList)
	headers = ["WorkorderType","WorkOrderId","WoNumber"]
	resultDetails = system.dataset.toDataSet(headers,dataList)
	return resultDetails
	
def getCNSClubbedWorkorderDetailsbyworkorderId(selectedWorkorderId):
	try:
		scriptName = "API: Get Clubbed WorkOrder List"
		apiPath = "ProductionOperatorConsole/GetClubbedWorkOrdersbyWoNumber/WorkOrderId:int?WorkOrderId="+str(selectedWorkorderId)
		url = URLPath + apiPath

		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData=data.json

		dataList = []
		for i in resultData:	
			workorderId = i.get('WorkorderId')
			workOrderNo = i.get('WorkOrderNo')
			primaryWorkOrderId = i.get('PrimaryWorkOrderId')
			IsWorkOrderClubbed = i.get('IsWorkOrderClubbed')
			primaryWorkorderNo = i.get('PrimaryWorkOrderNumber')

			myList = [workorderId,workOrderNo,primaryWorkOrderId,IsWorkOrderClubbed,primaryWorkorderNo] 
			dataList.append(myList)	

		headers = ['WorkorderId','WorkOrderNo','PrimaryWorkOrderId','IsWorkOrderClubbed','PrimaryWorkorderNo']
		resultDetails = system.dataset.toDataSet(headers,dataList)
		print	'resultDetails'	,resultDetails
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)

def GetPaginationPreMaterialRequestDetails(Start,length,Search,LineId,userId):
	apiPath = "OperatorConsole/GetWorkordersForViewRequestsForOperatorConsole"
	url = URLPath + apiPath

	writeData=	{
				  "userId": userId,
				  "lineId": LineId,
				  "start": Start,
				  "draw": 0,
				  "length": length,
				  "search": {
				    "regex": True,
				    "value": Search
				  	}
				}
	jsonParams = system.util.jsonEncode(writeData)	
	system.perspective.print("jsonParams: "+str(jsonParams))
	createdeffect = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		print postReturn
		postReturn = system.util.jsonDecode(postReturn)
		dataList=[]
		j = 1
		for i in(postReturn):
			SrNo = i.get("BatchId")
			LineName = i.get("LineName")
			WorkorderNo = i.get("WorkorderNo")
			BatchId = i.get("BatchId")
			ProductName = i.get("ProductName")
			RequestedDate = i.get("RequestedDate")
			print('RequestedDate :' + str(RequestedDate))
			WorkOrderId = i.get("WorkOrderId")
			RequestStatus = i.get("RMStatus")
			ViewDetails = ""
			BatchId = i.get("BatchId")
			
			recordsTotal=0
			recordsFiltered=0
			RecordsTotal=i.get('RecordsTotal')
			if RecordsTotal>0:
				RecordsFiltered=i.get('RecordsFiltered')
				if str(recordsTotal)!=(RecordsFiltered):
					RecordsTotal=i.get('RecordsFiltered')
			j= j+1
			myList = [SrNo,LineName,WorkorderNo,ProductName,RequestedDate,WorkOrderId,RequestStatus,ViewDetails,BatchId,RecordsTotal,RecordsFiltered]
			dataList.append(myList)
		headers = ["SrNo","LineName","WorkorderNo","ProductName","RequestedDate","WorkOrderId","RequestStatus","ViewDetails","BatchId","RecordsTotal","RecordsFiltered"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
#		resultDetails = system.dataset.toPyDataSet(resultDetails)
		return resultDetails

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
			pass
	return postReturn