import re
import json
import urllib2, urllib 
import datetime
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value


def GetWarehouseByUserId(userId):  
	try: 
		url= URLPath + "SparePart/GetAllSupermarketToRequestSparePart/"+str(userId)
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
			dataList = []
			headers = ["SupermarketID","Supermarket"]
			dataList=[]
			for i in resultData:		
				mId = i.get("id")
				name = i.get("name")
				myList = [mId,name] 		
				dataList.append(myList)	
			resultDetails = system.dataset.toDataSet(headers,dataList)
			resultDetails=system.dataset.toPyDataSet(resultDetails)
			return resultDetails
		else:
			return None
	except :
		return None

def GetSpareParts(warehouseId):  	
	try: 

		url= URLPath + "SparePart/GetSpareParts/0/"+str(warehouseId)
		print  url
#		url="http://172.28.3.206/FactoryMagixWebAPI/api/SparePart/GetSpareParts/0/1"
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
			dataList = []
			headers = ["id","sparePartName","sparePartNumber","maxQty","canRequest","minQty","SparepartImagepath"]
			dataList=[]
			for i in resultData:		
				mId = i.get("id")
				sparePartName = i.get("sparePartName")
				sparePartNumber = i.get("sparePartNumber")
				maxQty = i.get("maxQty")
				canRequest = i.get("canRequest")
				minQty = i.get("minQty"),
				SparepartImagepath = i.get("SparePartImagePath")
				
				myList = [mId,sparePartName,sparePartNumber,maxQty,canRequest,minQty,SparepartImagepath] 		
				dataList.append(myList)	
			resultDetails = system.dataset.toDataSet(headers,dataList)
			resultDetails=system.dataset.toPyDataSet(resultDetails)
			return resultDetails
		else:
			return None
	except exception as e:
		print "error "+str(e)
		return None

def GetSparePartsName(warehouseId):  	
	try: 

		url= URLPath + "SparePart/GetSpareParts/0/"+str(warehouseId)
		print  url
#		url="http://172.28.3.206/FactoryMagixWebAPI/api/SparePart/GetSpareParts/0/1"
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
			dataList = []
			headers = ["id","sparePartNumber"]
			dataList=[]
			for i in resultData:		
				mId = i.get("id")
				sparePartNumber = i.get("sparePartNumber")
				
				myList = [mId,sparePartNumber] 		
				dataList.append(myList)	
			resultDetails = system.dataset.toDataSet(headers,dataList)
			resultDetails=system.dataset.toPyDataSet(resultDetails)
			return resultDetails
		else:
			return None
	except exception as e:
		print "error "+str(e)
		return None			
def GetSlotsForSpareParts(sparePartId):  
	try: 

		url= URLPath + "SparePart/GetSlotsForSpareParts/"+str(sparePartId)
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
			dataList = []
			headers = ["SlotId","SlotName"]
			dataList=[]
			for i in resultData:		
				mId = i.get("SlotId")
				name = i.get("SlotName")
				myList = [mId,name] 		
				dataList.append(myList)	
			resultDetails = system.dataset.toDataSet(headers,dataList)
			resultDetails=system.dataset.toPyDataSet(resultDetails)
			return resultDetails
		else:
			return None
	except :
		return None				

def AddRecieveSparePartsReceived(poNumber,sparePartNumber,receivedQty,slot,userID,warehouseId,Comments):
	try: 
		scriptName="Spare PArt Add In PDA : Start AddRecieveSparePartsForOperatorConsole"
		apiPath = "sparepart/AddRecieveSparePartsForOperatorConsole"
		url = URLPath + apiPath		
		system.perspective.print("url" + str(url))
		writeData = {
			"PoNumber": str(poNumber),
			"SparePartNumber": str(sparePartNumber),
			"ReceivedQty": int(receivedQty),
			"Slot": str(slot),
			"WarehouseId": int(warehouseId),
			"ReceivedBy": str(userID),
			"Id":0,
			"IsActive":True,
			"CreatedBy":int(userID),
			"ModifiedBy":0,
			"IsArchive":False,
			"Comments": Comments
		}
		system.perspective.print("writeData" + str(writeData))
		jsonParams = system.util.jsonEncode(writeData)		
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
			print("PostReturn",postReturn)
		except:	
			import sys, os
			errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
			Authentication.exceptionLogger(errorMessage)
			system.perspective.print("errorMessage "+ errorMessage)	
			result = 0
		system.perspective.print( "Result" +str(result))
		return result
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print("errorMessage "+  errorMessage)
		return 0		
		
def GetWorkOrdersForSparePartDelivery(warehouseId,actionTypeId):  
	try: 
		scriptName='GetWorkOrdersForSparePartDelivery'
		url= URLPath + "SparePart/GetWorkOrdersForSparePartDelivery/"+str(warehouseId)+"/"+str(actionTypeId)
		system.perspective.print("url "+  str(url))
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
			dataList = []
			headers = ["workOrder","requestId","requestNumber"]
			dataList=[]
			for i in resultData:		
				workOrder = i.get("workOrder")
				requestId = i.get("requestId")
				requestNumber = i.get("requestNumber")
				myList = [workOrder,requestId,requestNumber] 		
				dataList.append(myList)	
			resultDetails = system.dataset.toDataSet(headers,dataList)
			resultDetails=system.dataset.toPyDataSet(resultDetails)
			return resultDetails
		else:
			return None
	except :
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print("errorMessage "+  errorMessage)
		return None		
		
def GetSparePartRequestsByWorkOrder(woNumber,warehouseId,actionTypeid): 
	try: 
	 	scriptName='GetSparePartRequestsByWorkOrder'
		url= URLPath + "SparePart/GetSparePartRequestsByWorkOrder/"+str(woNumber)+"/"+str(warehouseId)+"/"+str(actionTypeid)
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
			dataList = []
			headers = ["id","requestNumber","woNumber"]
			dataList=[]
			for i in resultData:		
				id = i.get("id")
				requestNumber = i.get("requestNumber")
				woNumber = i.get("woNumber")
				myList = [id,requestNumber,woNumber] 		
				dataList.append(myList)	
			resultDetails = system.dataset.toDataSet(headers,dataList)
			resultDetails=system.dataset.toPyDataSet(resultDetails)
			return resultDetails
		else:
			return None
	except :
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print("errorMessage "+  errorMessage)
		return None			


def GetSparePartsByRequest(requestId): 
	try: 
		system.perspective.print("requestId =" + str(requestId))
		scriptName='GetSparePartsByRequest'
		
#		parameters = {"requestId":requestId}
#		PDASparePart/GetSparePartsByRequest
#		resultData=system.db.runNamedQuery('PDASparePart/GetSparePartsByRequest', parameters)
#		resultData=system.dataset.toPyDataSet(resultData)
		url= URLPath + "SparePart/GetSparePartsByRequest/"+str(requestId)
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		if len(resultData) > 0:
			dataList = []
			headers = ["id","requestedQty","canConsumedQty","sparePartNumber","onHandQty","MachineName","LineName","SlotName","SparePartImagePath","SparePartName","Slot"]
			dataList=[]
			for i in resultData:		
				id = i.get("id")
				requestedQty= i.get("requestedQty")
				canConsumedQty =i.get("canConsumedQty")
				sparePartNumber = i.get("sparePartNumber")
				onHandQty = i.get("onHandQty")
				MachineName = i.get("MachineName")
				LineName = i.get("LineName")
				SlotName = i.get("SlotName")
				SparePartImagePath = i.get("SparePartImagePath")
				
				SparePartName = i.get("SparePartName")
				Slot = i.get("Slot")
				
#				id = i["id"]
#				requestedQty= i["requestedQty"]
#				canConsumedQty =i["canConsumedQty"]
#				sparePartNumber = i["sparePartNumber"]
#				onHandQty = i["onHandQty"]
#				MachineName = i["MachineName"]
#				LineName = i["LineName"]
#				SlotName = i["SlotName"]
#				SlotName = i["Slot"]	
#				SparePartImagePath = i["SparePartImagePath"]
#				SparePartName = i["SparePartName"]
#				Slot = i["Slot"]
				
				system.perspective.print("requestedQty "+str(requestedQty))
				system.perspective.print("canConsumedQty "+str(canConsumedQty))
				system.perspective.print("onHandQty "+str(onHandQty))
				myList = [id,requestedQty,canConsumedQty,sparePartNumber,onHandQty,MachineName,LineName,SlotName,SparePartImagePath,SparePartName,Slot] 		
				dataList.append(myList)	
			resultDetails = system.dataset.toDataSet(headers,dataList)
			resultDetails=system.dataset.toPyDataSet(resultDetails)
			print("resultDetails =" + str(resultDetails))
			return resultDetails
			
		else:
			return None
	except :
	
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		print("errorMessage "+  errorMessage)
		return None	
		

def SetSparePartAllocateQty(SPId,receivedQty,requestId,warehouseId,receivedBy,UserId):
	try: 
		scriptName="Spare PArt Add In PDA : Start SetSparePartAllocateQty"
#		parameters = {"id":SPId,"value":receivedQty,"requestId":requestId, "warehouseId":warehouseId,"receivedBy":receivedBy, "UserId":UserId}
#		system.db.runNamedQuery('PDASparePart/SetSparePartAllocateQty', parameters)
#		result = 1
		apiPath = "SparePart/SetSparePartAllocateQty"
		url = URLPath + apiPath		
		system.perspective.print("url" + str(url))
		writeData = {
			"id": int(SPId),
			"value": int(receivedQty),
			"requestId": int(requestId),
			"warehouseId": int(warehouseId),
			"receivedBy": str(receivedBy),
			"createdBy": int(UserId)
		}
		system.perspective.print("writeData" + str(writeData))
		jsonParams = system.util.jsonEncode(writeData)		
		
		
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		system.perspective.print("PostReturn = "+ str(postReturn))
		import json
		postReturn = json.loads(postReturn)
		result=0
		for i in postReturn:
			result= i.get("Valid")
		system.perspective.print("result spare part = "+ str(result))
		
		result=1
#		except:	
#			import sys, os
#			errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
#			Authentication.exceptionLogger(errorMessage)
#			system.perspective.print("errorMessage "+ errorMessage)	
#			result = 0
#		system.perspective.print( "Result" +str(result))
		return result
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print("errorMessage "+  errorMessage)
		return 0	

def GetSlotsForWarehouse(WarehouseId,sparePartId):  
	try: 
		scriptName='GetSlotsForWarehouseZ'

#		parameters = {"supermarketId":WarehouseId, "partNo":sparePartId}
#		resultData=system.db.runNamedQuery('PDASparePart/GetSlotsForSupermarket', parameters)
#		resultData=system.dataset.toPyDataSet(resultData)
		url= URLPath + "SparePart/GetSlotsForWarehouse/"+str(WarehouseId)+"/"+str(sparePartId)
		system.perspective.print("url "+  url)		
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
		if resultData!='None':

			dataList = []
			headers = ["SlotId","SlotName"]
			dataList=[]
			for i in resultData:		
				mId = i["SlotId"]
#				name = i.get("SlotName")
				name = i["Slot"]
				myList = [mId,name] 		
				dataList.append(myList)	
			resultDetails = system.dataset.toDataSet(headers,dataList)
			resultDetails=system.dataset.toPyDataSet(resultDetails)
			return resultDetails
		else:
			return None
	except :
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print("errorMessage "+  errorMessage)
		return None	
		

def AddReturnFromSPRequest(workOrderNumber,requestNumberId,sparePartNumberId,returningQty,slotId,userId,returnBy):
	try: 
		system.perspective.print("workOrderNumber "+  str(workOrderNumber))
		system.perspective.print("requestNumberId "+  str(requestNumberId))
		system.perspective.print("sparePartNumberId "+  str(sparePartNumberId))
		system.perspective.print("returningQty "+  str(returningQty))
		system.perspective.print("slotId "+  str(slotId))
		system.perspective.print("userId "+  str(userId))
		system.perspective.print("returnBy "+  str(returnBy))
		
		scriptName="Spare PArt Add In PDA : Start AddReturnFromSPRequest"
#		parameters = {"workOrderNumber":workOrderNumber, "requestNumberId":requestNumberId,"sparePartNumberId":sparePartNumberId, "returningQty":returningQty,"slotId":slotId, "userId":userId, "returnBy":returnBy}
#		system.db.runNamedQuery('PDASparePart/AddReturnFromSparePartRequest', parameters)
		
		apiPath = "SparePart/AddReturnFromSPRequest"
		url = URLPath + apiPath		
		system.perspective.print("url" + str(url))
		writeData = {
			"workOrderNumber": str(workOrderNumber),
			"requestNumberId": int(requestNumberId),
			"sparePartNumberId": int(sparePartNumberId),
			"returningQty": int(returningQty),
			"slotId": int(slotId),
			"createdBy": str(userId),
			"returnBy":  returnBy
		}
		system.perspective.print("writeData" + str(writeData))
		jsonParams = system.util.jsonEncode(writeData)		
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
			print("PostReturn",postReturn)
		except:	
			import sys, os
			errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
			Authentication.exceptionLogger(errorMessage)
			system.perspective.print("errorMessage "+ errorMessage)	
			result = 0
		system.perspective.print( "Result" +str(result))
		return result
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print("errorMessage "+  errorMessage)
		return 0			
		
def GetSparePartTemplate(SparePartNumber,SlotId):  
	try: 

		url= URLPath + "SparePart/GetSparePartTemplate/"+str(SparePartNumber)+"/"+str(SlotId)
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)		
		print resultData
		templateData=''
		if resultData!=None and resultData!='' and str(resultData)!='None':
			templateData=str(resultData[u'templateData'])
		return templateData
	except :
		return None
		

def AddUpdateSparePartReceptionPrintHistory(SparePartNumberId,SlotId,NoOfPrint,printedBy):	
	try: 
		scriptName="API:AddUpdateSparePartReceptionPrintHistory No Of Print Spare part and Slot wise"
		apiPath = "SparePart/AddUpdateSparePartReceptionPrintHistory"
		print 'call'
		url = URLPath + apiPath		
		print("url "+ str(url))
		writeData = {
			"sparePartId": int(SparePartNumberId),
			"slotId" : int(SlotId),
			"printedBy": printedBy,
			"numberOfPrints": NoOfPrint		
			}
		print 'call 1'
		jsonParams = system.util.jsonEncode(writeData)		
#		system.perspective.print ("jsonParams "+str(jsonParams))
#		system.perspective.print ("Save print History jsonParams "+str(jsonParams))
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
			print("PostReturn",postReturn)
#			system.perspective.print("PostReturn",postReturn)
		except:		
			import sys, os
			result=0
			errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
			Authentication.exceptionLogger(errorMessage)
			print  errorMessage
			result=0
		return result
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		print errorMessage
		return None		
		
def GetPrinterDetails(PrinterTypeId):  
	try: 
		scriptName="API: GetPrinterDetails"

		url= URLPath + "SparePart/GetPrinterDetails?PrinterTypeId="+str(PrinterTypeId)
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
			resultData=data.json
			dataList = []
			dataListddl = []
			headers = ["PrinterId","PrinterName","PrinterIP","Port"]
			headersddl = ["PrinterId","PrinterName"]
			for i in resultData:		
				PrinterId = i.get("PrinterId")
				PrinterName = i.get("PrinterName")
				PrinterIP = i.get("PrinterIP")
				Port = i.get("Port")
				
				myList = [PrinterId,PrinterName,PrinterIP,Port] 		
				dataList.append(myList)	
				
				PrinterName=PrinterName+' - '+PrinterIP
				myListddl = [PrinterId,PrinterName] 		
				dataListddl.append(myListddl)	
				
				
			resultDetails = system.dataset.toDataSet(headers,dataList)
			resultDetails=system.dataset.toPyDataSet(resultDetails)
			
			resultddlDetails = system.dataset.toDataSet(headersddl,dataListddl)
			resultddlDetails=system.dataset.toPyDataSet(resultddlDetails)
			
			return resultDetails ,resultddlDetails

	except :
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		print errorMessage
		return None								