import re
import json
import urllib2, urllib 
import re
import json
import urllib2, urllib
import datetime
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value

#URLPath = URLTag.value

def GetOperatorConsoleMaterialRequest(workOrderNo,selectedLineId):   
	url= URLPath + "OperatorConsole/GetOperatorConsoleMaterialRequest?WorkOrderId="+str(workOrderNo)+"&LineId="+str(selectedLineId)
	
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)
	resultData= system.util.jsonDecode(data)
	print 'resultData',resultData
	headers = ["bomdetailsId","ItemId","Material"]
	dataList=[]
	for i in resultData:
		bomdetailsId = i.get('BomDetailsId')
		ItemId = i.get('ItemId')
		Material = i.get("Material")
		myList = [bomdetailsId,ItemId,Material]		
		system.perspective.print('List :' + str(myList))
		dataList.append(myList)	
	resultDetails = system.dataset.toDataSet(headers,dataList)
	resultDetails=system.dataset.toPyDataSet(resultDetails)
	return resultDetails

def isNotBlank (myString):
	try:
		myString=str(myString).strip()
		if myString=='' or str(myString).lower()==str('None').lower() or str(myString)==None or str(myString).lower()==str('null').lower():
			myString=''	
		return myString
	except:
		return myString
    
def GetMaterialComponent(materialNo,types):   
#	url= URLPath + "MaterialMovement/GetMaterialTransfer/0?batchId="+str(materialNo)
	url= URLPath + "MaterialMovement/GetMaterialTransfer/"+str(materialNo)+"/"+str(types)
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)
	resultData= system.util.jsonDecode(data)
	headers = ["Component","QTY","LOT","TRANSFERID","BatchId","isSelect","IO","WorkOrderNo","UOM","VendorLot","VendorName","ExpiryDate","LocatorType","ToLocatorName","ToSubInventoryName","FromLocatorName","FromLocator","Ledger","OU","SubInventoryCode","RequestTransferDate","SourceCode","FromSubInventoryName","WorkOrderType","IsExpired","MfgLine"]
	dataList=[]
	for i in resultData:	
		Component = i.get("Component")
		QTY = i.get("QTY")
		LOT = i.get("LOT")
		TRANSFERID = i.get("TRANSFERID")
		BatchId = i.get("BatchId")
		isSelect=0
		IO=i.get("IO")
		WorkOrderNo=i.get("WorkOrderNo")
		UOM=i.get("UOM")
		VendorLot=i.get("VendorLot")
		VendorName=i.get("VendorName")
		ExpiryDate=i.get("ExpiryDate")
		LocatorType=i.get("LocatorType")
		ToLocatorName=i.get("ToLocatorName")
		ToSubInventoryName=i.get("ToSubInventoryName")
		FromLocatorName=i.get("FromLocatorName")
		FromLocator=i.get("FromLocator")
		Ledger=i.get("Ledger")
		OU=i.get("OU")
		SubInventoryCode=i.get("SubInventoryCode")
		RequestTransferDate=i.get("RequestTransferDate")
		SourceCode=i.get("SourceCode")
		FromSubInventoryName=i.get("FromSubInventoryName")
		WorkOrderType = i.get("WorkOrderType")
		MfgLine = i.get("MfgLine")
		
		today = system.date.now()
		TodayDate= system.date.format(today, "dd/MM/yyyy,HH:mm:ss")
		
		print 'ERPExpirationDate',ExpiryDate
		if ExpiryDate >= TodayDate or ExpiryDate == None or str(ExpiryDate).strip().lower() == str("None").strip().lower():
			IsExpired = 0
			print "Not Expired--->"
		else:
			IsExpired = 1
			print "Expired-------> "
		
		myList = [Component,QTY,LOT,TRANSFERID,BatchId,isSelect,IO,WorkOrderNo,UOM,VendorLot,VendorName,ExpiryDate,LocatorType,ToLocatorName,ToSubInventoryName,FromLocatorName,FromLocator,Ledger,OU,SubInventoryCode,RequestTransferDate,SourceCode,FromSubInventoryName,WorkOrderType,IsExpired,MfgLine] 		
		dataList.append(myList)		
	resultDetails = system.dataset.toDataSet(headers,dataList)
	resultDetails=system.dataset.toPyDataSet(resultDetails)
	return resultDetails	
	

def getSlotDetailsbyLineId(lineId,ItemId):
	try:
		url= URLPath + "MaterialMovement/GetPOUDetailsByItemID/"+str(1022)+"/"+str(538525)
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		print 'resultData',resultData
		
		dataList=[]
		for i in resultData:
			SlotId = i.get("SlotId")
			ItemId= i.get("PartNo")
			MAXQuantity = i.get("MAXQuantity")
			InHandQty = i.get("InHandQty")
			SlotName = i.get("SlotName")
		
			myList = [SlotId,ItemId,MAXQuantity,InHandQty,SlotName]
			system.perspective.print('List :' + str(myList))
			dataList.append(myList)	
		headers = ["SlotId","ItemId","MAXQuantity","InHandQty","SlotName"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		resultDetails=system.dataset.toPyDataSet(resultDetails)
		print 'resultDetails',resultDetails
		return resultDetails
	except:
		pass
		
def getSlotDetailsbyLineId(lineId,ItemId):
	try:
		url= URLPath + "MaterialMovement/GetPOUDetailsByItemID/"+str(lineId)+"/"+str(ItemId)
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		print 'resultData',resultData
		
		dataList=[]
		for i in resultData:
			ItemId= i.get("PartNo")
			MAXQuantity = i.get("MAXQuantity")
			InHandQty = i.get("InHandQty")
			SlotId = i.get("SlotId")
			SlotName = i.get("SlotName")
		
			myList = [ItemId,MAXQuantity,InHandQty,SlotId,SlotName]
			dataList.append(myList)	
		headers = ["ItemId","MAXQuantity","InHandQty","SlotId","SlotName"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		print 'resultDetails',resultDetails
		return resultDetails
	except:
		pass
		
def getslotQtyDetails(slotId,lineId,ItemId):
	try:
		url= URLPath + "MaterialMovement/GetPOUDetailsByItemID/"+str(lineId)+"/"+str(ItemId)
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		print 'resultData',resultData
		
		dataList=[]
		for i in resultData:
			SlotId = i.get("SlotId")
			if int(slotId)==int(SlotId):
				MAXQuantity = i.get("MAXQuantity")
				InHandQty = i.get("InHandQty")
				if str(InHandQty).lower() == str('Null').lower() or str(InHandQty).lower() == str('None').lower() or str(InHandQty).lower() == str(None).lower():
					 InHandQty = 0
				else:
					InHandQty = InHandQty
				myList = [MAXQuantity,InHandQty]
				print 'Mylist', myList
				dataList.append(myList)	
		headers = ["MAXQuantity","InHandQty"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		print 'resultDetails',resultDetails
		return resultDetails
	except:
		pass

def GetBomdetailsIdbyItemID(selectedItemId,workOrderNo,selectedLineId):   
#	url= URLPath + "OperatorConsole/GetOperatorConsoleMaterialRequest?WorkOrderNo="+str(workOrderNo)
	url= URLPath + "OperatorConsole/GetOperatorConsoleMaterialRequest?WorkOrderId="+str(workOrderNo)+"&LineId="+str(selectedLineId)
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)
	resultData= system.util.jsonDecode(data)
	headers = ["bomdetailsId","ItemId","Material"]
	dataList=[]
	for i in resultData:
		ItemId = i.get('ItemId')
		if selectedItemId ==ItemId:
			bomdetailsId = i.get('BomDetailsId')
			Material = i.get("Material")
			myList = [bomdetailsId,ItemId,Material] 		
			dataList.append(myList)	
	resultDetails = system.dataset.toDataSet(headers,dataList)
	resultDetails=system.dataset.toPyDataSet(resultDetails)
	return resultDetails
	
	
def AddSlotDetails(selectedWorkorderId,selectedLineId,selectedItemId,slotID,bomDetailsId,receivedLotNumber,receivedQuantity,userId):
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
							    "createdBy":userId
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