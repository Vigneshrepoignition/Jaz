import re
import json
import urllib2, urllib
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
defaultPath=system.tag.read("[default]JMES_InternalTags/DafaultTagPath").value

def updatePackingAndLebelling():
	try:	
		activeWOList = PackingAndLabelling.getactiveWoList()
	except:
		logger = system.util.getLogger("MES Application")
		logger.error("Error while fetching active WorkOrder List for packing script")
	print(activeWOList)	
	for row in activeWOList:
		lineName = row.get("LineName")
		WoNumber = row.get("WorkOrderNo")
		machineName = row.get("MachineName")
		machineId = row.get("MachineId")
		areaName = row.get("AreaName")		
		print(machineName)
		print("--------------"+str(WoNumber)+"--------------")
		try:
			TagPathCompletedLots = str(defaultPath)+str(machineName)+"/CompletedLots"
			TagPathCompletedCarton = str(defaultPath)+str(machineName)+"/CompletedCarton"
			TagPathCompletedPallet = str(defaultPath)+str(machineName)+"/CompletedPallet"
			TagPathGoodQty = str(defaultPath) +str(machineName)+"/GoodQty"
			print("Machine Tags Identified.. ")
		except:			
			logger = system.util.getLogger("MES Application")
			logger.error("Error while reading machine tags in packing script")
		CompletedLots = system.tag.read(TagPathCompletedLots).value
		CompletedCarton = system.tag.read(TagPathCompletedCarton).value
		CompletedPallet = system.tag.read(TagPathCompletedPallet).value
		if areaName=="CNS":
			paramCurrentValue = system.tag.read(TagPathGoodQty).value
			goodQty = PackingAndLabelling.getGoodQtyForCNSMoldingMachines(WoNumber,machineId,machineName,paramCurrentValue)
		else:
			goodQty = system.tag.read(TagPathGoodQty).value
			
		print("GoodQty:"+str(goodQty))
	#------------------------Inputs from Packing API  ------------------------				
		try:
			configDetails = getPackingConfigDetails(WoNumber)	# API Call		
		except:
			logger = system.util.getLogger("MES Application")
			logger.error("Error while executing getPackingConfigDetails function in packing script")			
		printConfig = configDetails.get("PrintLabel")		
		backflushConfig = configDetails.get("BFLabel")
		packingConfig = configDetails.get("PackingLabel")
		print("printConfig:"+str(printConfig))
		print("backflushConfig:"+str(backflushConfig))
		print("packingConfig:"+str(packingConfig))
		
		CanSkipLot = configDetails.get("CanSkipLot")
		lotPerCarton = configDetails.get("ContainerCount")
		cartonPerPallet = configDetails.get("PalleteCount")							
		if CanSkipLot== 'true' or CanSkipLot==1:
			skipLot = True
			qtyPerCarton = lotPerCarton
		else:
			skipLot = False		
			qtyPerLot = configDetails.get("LotCount")
			print("qtyPerLot:"+str(qtyPerLot))
			qtyPerCarton = (lotPerCarton*qtyPerLot)					
			runningLotQty    = goodQty - (qtyPerLot*CompletedLots)		
		qtyPerPallet = (qtyPerCarton*cartonPerPallet)		
		print("qtyPerCarton:"+str(qtyPerCarton))
		print("qtyPerPallet:"+str(qtyPerPallet))
		print("CanSkipLot:"+str(CanSkipLot))	
		runningCartonQty = goodQty - (qtyPerCarton*CompletedCarton)
		runningPalletQty = goodQty - (qtyPerPallet*CompletedPallet)
	
	#--------------- Call Functions --------------------------------------------------
		if skipLot==True or skipLot==1:			
			pass	
		else:
			updateLotFlush(WoNumber,lineName,machineId,goodQty,runningLotQty,skipLot,qtyPerLot,printConfig,backflushConfig,packingConfig,CompletedLots,TagPathCompletedLots)			
		updateCartonFlush(WoNumber,lineName,machineId,goodQty,runningCartonQty,qtyPerCarton,printConfig,backflushConfig,packingConfig,CompletedCarton,TagPathCompletedCarton)	
		updatePalletFlush(WoNumber,lineName,machineId,goodQty,runningPalletQty,qtyPerPallet,printConfig,backflushConfig,packingConfig,CompletedPallet,TagPathCompletedPallet)	
		print("----------------------------------------------------")
		
def updateLotFlush(WoNumber,lineName,machineId,goodQty,runningLotQty,skipLot,qtyPerLot,printConfig,backflushConfig,packingConfig,CompletedLots,TagPathCompletedLots):
	if skipLot==False and runningLotQty >= qtyPerLot and qtyPerLot != 0:
		try:
			CompletedLots = goodQty/qtyPerLot
		except:				
			logger = system.util.getLogger("MES Application")
			logger.error("There is an Error while calculating Completed Lots.")
			
		print("CompletedLots: "+str(CompletedLots))
		try:
			system.tag.writeAsync(TagPathCompletedLots,CompletedLots)
		except:
			logger = system.util.getLogger("MES Application")
			logger.error("Unable to update completed lots tag in "+str(WoNumber))			
#------------------------------- Printing -------------------------------------------------------------	
		if printConfig in [4,5,6,7]:
			print("Lot Label Printed..")
			labelTypeId = 1
			try:
				PackingAndLabelling.updatePrintHistory(WoNumber,labelTypeId)
			except:
				logger = system.util.getLogger("MES Application")
				logger.error("There is an error print lable for workorder- "+str(WoNumber))	
				pass
		else:
			pass
#------------------------------- Backflush  ------------------------------------------------------------
		if backflushConfig in [4]:
			print("Backflush Trigger at Lot Level Started..")
			try:
				resultData = PackingAndLabelling.getProductionDetailsforERP(WoNumber,lineName,machineId)
				for prodDetails in resultData:
					woLotNumber = prodDetails.get("LotNumber")
					workflowId = int(prodDetails.get("WorkflowId"))					
					workOrderType = prodDetails.get("WorkorderType")
					partNumber = prodDetails.get("PRODUCTNAME")
					revision = prodDetails.get("PRODUCTREVISION")
					UOM = prodDetails.get("UOM")
					IO = prodDetails.get("IO")
					OU = prodDetails.get("OU")
					subInventoryCode = prodDetails.get("SubInventoryCode")					
					ledger = prodDetails.get("Ledger")
					locatorName =  prodDetails.get("LocatorName")	
					containerNo =  prodDetails.get("CurrentContainerNumber")
					lineName = prodDetails.get("ERPLineName")				
			except:
				logger = system.util.getLogger("MES Application")
				logger.error("Unable to read WorkOrder related Details in Production Data Flush for WorkOrder- "+str(WoNumber))				
			try:
				WorkOrderDetailsAPI.postCompleteDetailsToERP(WoNumber,woLotNumber,workflowId,workOrderType,lineName,partNumber,revision,goodQty,UOM,IO,OU,subInventoryCode,ledger,locatorName,containerNo)
			except:
				logger = system.util.getLogger("MES Application")
				logger.error("There is an Error in Production data flush for WorkOrder "+str(WoNumber))
			
			pass
	elif skipLot==True:
		print("Lot is Skipped")	
	else:
		print("Lot In Progress")	
#----------------------------------End Lot Flush Function --------------------------------------------
	
def updateCartonFlush(WoNumber,lineName,machineId,goodQty,runningCartonQty,qtyPerCarton,printConfig,backflushConfig,packingConfig,CompletedCarton,TagPathCompletedCarton):
	if runningCartonQty >= qtyPerCarton and qtyPerCarton != 0:
		try:
			CompletedCarton = goodQty/qtyPerCarton	
			system.tag.writeAsync(TagPathCompletedCarton,CompletedCarton)
		except:							
			logger = system.util.getLogger("MES Application")
			logger.error("There is an Error while calculating Completed Carton.")
#------------------------------- Printing -------------------------------------------------------------		
		if printConfig in [2,3,6,7]:
			print("Carton Label Printed..")	
			labelTypeId = 2
			try:
				PackingAndLabelling.updatePrintHistory(WoNumber,labelTypeId)
			except:
				logger = system.util.getLogger("MES Application")
				logger.error("There is an error print lable for workorder- "+str(WoNumber))			
		else:
			pass	
#------------------------------- Backflush  ------------------------------------------------------------
		if backflushConfig in [2]:
			print("Backflush Trigger at Carton Level..")	
			try:
				resultData = PackingAndLabelling.getProductionDetailsforERP(WoNumber,lineName,machineId)
				for prodDetails in resultData:
					woLotNumber = prodDetails.get("LotNumber")
					workflowId = int(prodDetails.get("WorkflowId"))					
					workOrderType = prodDetails.get("WorkorderType")
					partNumber = prodDetails.get("PRODUCTNAME")
					revision = prodDetails.get("PRODUCTREVISION")
					UOM = prodDetails.get("UOM")
					IO = prodDetails.get("IO")
					OU = prodDetails.get("OU")
					subInventoryCode = prodDetails.get("SubInventoryCode")					
					ledger = prodDetails.get("Ledger")
					locatorName =  prodDetails.get("LocatorName")				
					containerNo =  prodDetails.get("CurrentContainerNumber")
					lineName = prodDetails.get("ERPLineName")
			except:
				logger = system.util.getLogger("MES Application")
				logger.error("Unable to read WorkOrder related Details in Production Data Flush for WorkOrder- "+str(WoNumber))			
			try:
				WorkOrderDetailsAPI.postCompleteDetailsToERP(WoNumber,woLotNumber,workflowId,workOrderType,lineName,partNumber,revision,goodQty,UOM,IO,OU,subInventoryCode,ledger,locatorName,containerNo)
			except:
				logger = system.util.getLogger("MES Application")
				logger.error("There is an Error in Production data flush for WorkOrder "+str(WoNumber))
			pass				
		else:
			pass
#------------------------------- Packing -------------------------------------------------------------	
		if packingConfig in [2]:
			containerType = "CARTON"			
			print("Packing Trigger at Carton Level..")
			try:
				resultData = PackingAndLabelling.getLotNumberDetails(WoNumber,lineName,machineId)
				collectResult = WorkOrderDetailsAPI.postPackingDetailsToERP(resultData,WoNumber,lineName,containerType,qtyPerCarton,str(goodQty))
			except:
				logger = system.util.getLogger("MES Application")
				logger.error("There is an Error in Packing data flush for WorkOrder "+str(WoNumber))
		else:
			pass		
	else:
		print("Carton In Progress")
#----------------------------------End Carton Flush Function -----------------------------------------
		
def updatePalletFlush(WoNumber,lineName,machineId,goodQty,runningPalletQty,qtyPerPallet,printConfig,backflushConfig,packingConfig,CompletedPallet,TagPathCompletedPallet):
	if runningPalletQty >= qtyPerPallet and qtyPerPallet != 0:
		try:
			CompletedPallet = goodQty/qtyPerPallet	
		except:				
			logger = system.util.getLogger("MES Application")
			logger.error("There is an Error while calculating Completed Pallet in "+str(WoNumber))		
		try:
			system.tag.writeAsync(TagPathCompletedPallet,CompletedPallet)
		except:
			logger = system.util.getLogger("MES Application")
			logger.error("There is an Error updating completed pallet quantity in "+str(WoNumber))
#------------------------------- Printing -------------------------------------------------------------			
		if printConfig in [1,3,5,7]:
			print("Pallet Label Printed..")
			labelTypeId = 3
			try:
				PackingAndLabelling.updatePrintHistory(WoNumber,labelTypeId)
			except:
				logger = system.util.getLogger("MES Application")
				logger.error("There is an error print lable for workorder- "+str(WoNumber))	
		else:
			pass		
#------------------------------- Backflush  ------------------------------------------------------------	
		if backflushConfig in [1]:
			print("Backflush Trigger at Pallet Level..")
			try:
				resultData = PackingAndLabelling.getProductionDetailsforERP(WoNumber,lineName,machineId)
				for prodDetails in resultData:
					woLotNumber = prodDetails.get("LotNumber")
					workflowId = int(prodDetails.get("WorkflowId"))					
					workOrderType = prodDetails.get("WorkorderType")
					partNumber = prodDetails.get("PRODUCTNAME")
					revision = prodDetails.get("PRODUCTREVISION")
					UOM = prodDetails.get("UOM")
					IO = prodDetails.get("IO")
					OU = prodDetails.get("OU")
					subInventoryCode = prodDetails.get("SubInventoryCode")					
					ledger = prodDetails.get("Ledger")
					locatorName =  prodDetails.get("LocatorName")
					containerNo =  prodDetails.get("CurrentContainerNumber")
					lineName = prodDetails.get("ERPLineName")
			except:
				logger = system.util.getLogger("MES Application")
				logger.error("Unable to read WorkOrder related Details in Production Data Flush for WorkOrder- "+str(WoNumber))
			try:					
				WorkOrderDetailsAPI.postCompleteDetailsToERP(WoNumber,woLotNumber,workflowId,workOrderType,lineName,partNumber,revision,goodQty,UOM,IO,OU,subInventoryCode,ledger,locatorName,containerNo)
			except:
				logger = system.util.getLogger("MES Application")
				logger.error("There is an Error in Production data flush for WorkOrder "+str(WoNumber))
			pass
		else:
			pass
#------------------------------- Packing -------------------------------------------------------------	
		if packingConfig in [1]:		
			containerType = "PALLET"
			containerNo = "99"
			print("Packing Trigger at Pallet Level..")
			try:
				resultData = PackingAndLabelling.getLotNumberDetails(WoNumber,lineName,machineId)		
				collectResult = WorkOrderDetailsAPI.postPackingDetailsToERP(resultData,WoNumber,lineName,containerType,qtyPerPallet,str(goodQty))			
			except:
				logger = system.util.getLogger("MES Application")
				logger.error("There is an Error in Packing data flush for WorkOrder "+str(WoNumber))
		else:
			pass
	else:
		print("Pallet In Progress")		
#----------------------------------End Pallet Flush Function -----------------------------------------

def getPackingConfigDetails(WoNumber):
	apiPath = "PackingPrintingConfiguration/GetWorkOrderPackingConfiguration/"+str(WoNumber)
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)	
	resultData= system.util.jsonDecode(data)
	return resultData
	
def getactiveWoList():
	apiPath = "OperatorConsole/GetOperatorConsoleRunningOperationsMachines"			                 
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)	
	resultData= system.util.jsonDecode(data)
	return resultData
	
def getActiveWorkOrderMachineList():
	apiPath = "OperatorConsole/GetOperatorConsoleALLRunningOperationsMachines" 		                 
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)	
	resultData= system.util.jsonDecode(data)
	return resultData
	
def getLotNumberDetails(WoNumber,lineName,machineId):		
	apiPath = "PackingProductionOperatorConsole/GetLotNumberforPackingProduction"
	url = URLPath + apiPath
	params = {
	  "workOrderNumber": WoNumber,  
	  "lineName": lineName,  
	  "shift": "1",
	  "machineId": machineId 
	}		
	jsonParams = system.util.jsonEncode(params)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except:
		logger = system.util.getLogger("MES Application")
		logger.error("unable to execute lot number genration script in "+str(WoNumber))		
		result = 0
		postReturn = ''
		pass	
	resultData= system.util.jsonDecode(postReturn)	
	return resultData

def getProductionDetailsforERP(WoNumber,lineName,machineId):
	apiPath = "PackingProductionOperatorConsole/GetProductionReporting"
	url = URLPath + apiPath
	params = {
	  "workOrderNumber": WoNumber,  
	  "lineName": lineName,  
	  "shift": "1",
	  "machineId": machineId 
	}		
	jsonParams = system.util.jsonEncode(params)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except:	
		logger = system.util.getLogger("MES Application")
		logger.error("Unable to get production details while executing ERP backflush in "+str(WoNumber))	
		result = 0
		postReturn = ''
		pass	
	resultData= system.util.jsonDecode(postReturn)
	
	return resultData

def getComponentDetailsRelatedToWO(WoNumber):	
	apiPath = "PackingProductionOperatorConsole/GetComponentDetailsForERPBackflush?WorkOrderNumber="+str(WoNumber)	
	url = URLPath + apiPath
	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)	
	resultData= system.util.jsonDecode(data)
	return resultData
	
def updatePrintHistory(WoNumber,labelTypeId):		
	apiPath = "SparePart/UpdateWorkOrderPrintStatus"
	url = URLPath + apiPath
	params = {
	  "workOrderNumber": WoNumber,
	  "labelNumber": int(labelTypeId)
	}		
	jsonParams = system.util.jsonEncode(params)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except:
		logger = system.util.getLogger("MES Application")
		logger.error("unable to update Print History "+str(WoNumber))		
		result = 0
		postReturn = ''
		pass	
	resultData= system.util.jsonDecode(postReturn)
	return resultData
	
#Packing Configuration
def getWorkOrderNo(machineID):		
	try:
		scriptName="API:getWorkOrderNo PAcking"
		apiPath = "PlantHierarchyMachine/GetPlantHierarchyMachinesWo_OnMachineChange/"+str(machineID)
		url = URLPath + apiPath
		print url
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)		
		dataList = []
		for i in resultData:	
			ID = i.get("woId")
			Name = i.get("woName")
#			myList = [ID,Name]
			myList = [ID,Name]			
			dataList.append(myList)				
		headers = ["ID","Name"]
		resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		print errorMessage
		Authentication.exceptionLogger(errorMessage)
		return None
			
def GetWorkOrderPackageConfigurations(WorkorderId):		
	try:
		scriptName="API:GetWorkOrderPackageConfigurations Packing"
#		apiPath = "PlantHierarchyMachine/GetWorkOrderPackageConfigurations/"+str(WorkorderId)+"/0"
		apiPath='PackingPrintingConfiguration/GetWorkOrderPackingConfigurationsDetails/'+str(WorkorderId)
		
		url = URLPath + apiPath
		system.perspective.print("API URL is: "+str(url))
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)		
#		resultDetails = system.dataset.toPyDataSet(resultData)
		return resultData
	except:
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		system.perspective.print(errorMessage)
		Authentication.exceptionLogger(errorMessage)
		return None



def GetWorkOrderPackageConfigurationsDetails(Start,length,Search,WorkOrderId):
	apiPath = "PrinterConfiguration/GetContainerPallet"
	url = URLPath + apiPath
	
	writeData={
				  "workorderId":WorkOrderId,
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
		for i in(postReturn):
			SrNo=i.get('SrNo')
			Pallet=i.get('PalletNo')
			Lot=i.get('LotNo')
			Container=i.get('ContainerId')
			Qty=i.get('Qty')
			WorkOrderNo=i.get('WorkOrderNo')
			WorkOrderId=i.get('WorkOrderId')
			IsPalletCompleted=i.get('IsPalletCompleted')
			recordsTotal=0
			recordsFiltered=0
			RecordsTotal=i.get('RecordsTotal')
			if RecordsTotal>0:
				RecordsFiltered=i.get('RecordsFiltered')
				if str(recordsTotal)!=(RecordsFiltered):
					RecordsTotal=i.get('RecordsFiltered')
				Template=""
				NoOFPrints=1		
				ContainerPrintHistory=""
				PalletPrintHistory=""			
				myList=[SrNo,Pallet,Lot,Container,Template,NoOFPrints,ContainerPrintHistory,PalletPrintHistory,RecordsTotal,RecordsFiltered,IsPalletCompleted]		
				dataList.append(myList)	
		headers = ["SrNo","Pallet","Lot","Container","Template","NoOFPrints","ContainerPrintHistory","PalletPrintHistory","RecordsTotal","RecordsFiltered","IsPalletCompleted"]
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
	
	
	


def GetWorkOrderPrintPackingConfigurationsDetails(workOrderName):		
	try:
		scriptName="API:GetWorkOrderPrintPackingConfigurationsDetails Packing"
		apiPath = "PackingPrintingConfiguration/GetWorkOrderPrintPackingConfigurationsDetails/"+str(workOrderName)+"/0"
		url = URLPath + apiPath
		print url
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		SrNo=0
		dataList = []
		for i in resultData:
			template= i['template']
			label = i['label']
			firstPrint = i['firstPrint']
			if firstPrint==None:
				firstPrint=''
			number = i['number']
			SrNo=SrNo+1	
			NoOfPrint=''
			PrintHistory=''
			myList = [SrNo,number,label,template,firstPrint,NoOfPrint,PrintHistory]		
			dataList.append(myList)	
		headers = ["SrNo","Number","Type","Template","FirstPrint","NoOfPrint","PrintHistory"]		
		resultDetails = system.dataset.toDataSet(headers,dataList)
		resultDetails = system.dataset.toPyDataSet(resultDetails)	
		return resultDetails
	except:		
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		print errorMessage
		Authentication.exceptionLogger(errorMessage)
		return None


def PrintNumberPacking(Number,labelTypeId,printedBy,NoOfPrint,WorkorderId):	
	try: 
		scriptName="API:PrintPacking No Of Print Lot No wise"
		apiPath = "PackingPrintingConfiguration/UpdateWorkOrderPrintStatus"
		print 'call'
		url = URLPath + apiPath		
#		system.perspective.print("url "+ str(url))
		print("url "+ str(url))
		writeData = {
			"itemNumber": str(Number),
			"labelTypeId" : int(labelTypeId),
			"printedBy": printedBy,
			"numberOfPrints": NoOfPrint,
			"workorder":'',
			"workorderId": WorkorderId,			
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



def GetPrintHistory(Number,type,WorkorderId,UserID):
	try:
		system.perspective.print('Number : ' + str(Number))
		system.perspective.print('type : ' + str(type))
		system.perspective.print('WorkorderId : ' + str(WorkorderId))
		system.perspective.print('UserID : ' + str(UserID))

		import sys, os
		scriptName="API:GetPrintHistory Packing"
		Number=Number.replace("/","%2F")
		Number=Number.replace("\\","%2F")
		apiPath = "PackingPrintingConfiguration/GetPrintHistory/"+str(Number)+"/"+str(type)+"/"+str(WorkorderId)+"/"+str(UserID)
		url = URLPath + apiPath
		print url

		system.perspective.print(url)
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		SrNo=0
		dataList = []
		for i in resultData:
		
			LabelName= i['LabelName']
			WorkOrderNumber= i['WorkOrderNumber']	
			NoOfPrint= i['NoOfPrints']
			PrintedOn = i['PrintDate']
			PrintedBy = i['PrintedBy']
			ItemNumber = i['ItemNumber']
			
			SrNo=SrNo+1	
			myList = [SrNo,LabelName,WorkOrderNumber,NoOfPrint,PrintedOn,PrintedBy,ItemNumber]		
			dataList.append(myList)	
		headers = ["SrNo","LabelName","WorkOrderNumber","NoOfPrint","PrintedOn","PrintedBy","ItemNumber"]
		resultDetails = system.dataset.toDataSet(headers,dataList)	
		resultDetails = system.dataset.toPyDataSet(resultDetails)	
		return resultDetails
	except:		
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		print errorMessage
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print(errorMessage)
		return None

def Getfilecontents(templatePath,fileName):
	try:
		scriptName="API:Getfilecontents Packing"
		fileNameTemplate=fileName
#		system.perspective.print("templatePath "+str(templatePath))
#		system.perspective.print("fileName "+str(fileName))
#		system.perspective.print("templatePath "+templatePath)
#		system.perspective.print("fileName "+fileName)
		templatePath = str(templatePath.replace("\v9", "\V9" ))
		templatePath = templatePath.replace(":", "%3A" )
		
		templatePath = templatePath.replace(" ", "%20" )
		templatePath = templatePath.replace('\\', "%5C" )
		fileName = fileName.replace(":", "%3A" )
		fileName = fileName.replace("\\", "%5C" )
		fileName = fileName.replace(" ", "%20" )
#		          "PackingPrintingConfiguration/Getfilecontents/"E%3A%5CWeb%20Deployments%5CWeb%20API%5Cv9.0.0.3%5CTemplates%5CPalletLabel_sizeadjusted%20-%20Copy09092022161115Pallete.prn/PalletLabel_sizeadjusted%20-%20Copy09092022161115Pallete.prn
		apiPath = "PackingPrintingConfiguration/Getfilecontents/"+str(templatePath)+"/"+str(fileName)
		
		url = URLPath + apiPath
		system.perspective.print (url)
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)		
		fileContain='1'
#		file = open("E://SharedPat//PrnFiles//"+str(fileNameTemplate))
		fileContain = system.file.readFileAsString("E://SharedPath\\PrnFiles\\"+str(fileNameTemplate))
		system.perspective.print("file :- "+str(fileContain))
#		system.perspective.print("file :- "+type(fileContain))
#		fileContain=file.read()
#		system.perspective.print ("fileContain "+ str(fileContain))
		return str(fileContain)
	except Exception as e:
#		scriptName = "Operator Console: CNS Mold part qty"
		errorMessage=scriptName  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print (errorMessage)	
		return None

def GetWorkOrderPackingConfigurationTemplate(WorkorderId,number,type):

	try:
		scriptName="API:GetWorkOrderPackingConfigurationTemplate Packing"
		
		
		number=number.replace("/","%2F")
		number=number.replace("\\","%2F")
		print number

#		apiPath = "PackingPrintingConfiguration/GetWorkOrderPackingConfigurationTemplate/"+str(workOrderNumber)+"/"+str(number)+"/"+str(type)
		apiPath= "PackingPrintingConfiguration/GetWorkOrderPackingConfigurationTemplate/"+str(WorkorderId)+"/"+str(number)+"/"+str(type)
		url = URLPath + apiPath
#		system.perspective.print (url)
#		url = "http://172.19.16.91/FactoryMagixWebAPIQA/api/PackingPrintingConfiguration/GetWorkOrderPackingConfigurationTemplate/CL13881572/30931%2FK1BA%2F0011/2"

#		system.perspective.print("url--->"+str(url))
		print ("sagar twstt")	
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)		
		print resultData
		templateData=''
		if resultData!=None and resultData!='' and str(resultData)!='None':
			templateData=str(resultData[u'templateData'])

		return templateData
	except Exception as e:
		errorMessage=scriptName  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)
		print errorMessage
#		system.perspective.print(errorMessage)
		return None			
						
def getGoodQtyForCNSMoldingMachines(WoNumber,machineId,machineName,paramCurrentValue):	
	goodQtyTagPath = str(defaultPath)+str(machineName)+"/GoodQty"	
	try:
		moldDetails = WorkOrderDetailsAPI.getMoldAssignmentDetails(WoNumber,machineId)												
	except Exception as e:
		scriptName = "Operator Console: CNS Mold part qty"
		errorMessage = scriptName  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)								
	else:
		if not moldDetails :	
			print("Mold Details Not Found...!!")			
			return paramCurrentValue			
		else:
			for moldData in moldDetails:
				cavity = moldData[2]
				productPiece = moldData[3]
				isMoldAssigned = moldData[4]															
			if (isMoldAssigned == True or isMoldAssigned == 1) and productPiece!=0:		
				calculatedGoodQty = (paramCurrentValue * cavity)/productPiece
				return int(calculatedGoodQty)
			elif isMoldAssigned == True and productPiece==0:
				return int(0) 
			else:			
				return paramCurrentValue
				

#----------------------------------------------------------------------Get  List Of continers for which Printing is not Done--------------------
def getnotPrintedContainer():

 	apiPath ="PackingPrintingConfiguration/GetNotPrintedContainers"
	url = URLPath + apiPath
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	return resultData
#------------------------------------------------Update container printing status------------------------------------	
def updatecontainerprintingstatus(workOrderNumber,containerName):		
	apiPath = "PackingPrintingConfiguration/UpdateContainerPrintStatus"
	url = URLPath + apiPath
	params = {
			  "containerName": containerName,
			  "workOrderNo": workOrderNumber
			}
	jsonParams = system.util.jsonEncode(params)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)	
	except:
		logger = system.util.getLogger("MES Application")
		logger.error("unable to update Print History "+str(WoNumber))		
		result = 0
		postReturn = ''
		pass	
	resultData= system.util.jsonDecode(postReturn)
	return resultData
				

