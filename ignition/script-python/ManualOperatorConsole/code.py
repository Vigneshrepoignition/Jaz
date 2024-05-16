import re
import json
import urllib2, urllib
import datetime
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
#URLPath = system.tag.read("[default]JMES_InternalTags/urlSITAPI").value

def getHourlyProductionManualDetails(lineId,WorkOrderId,machineId,shiftId,shiftTime):
	apiPath = "ManualProduction/GetDetailsofHourlyProduction"
	url = URLPath + apiPath
	params = {
	  "lineId": lineId,
	  "workOrderId": WorkOrderId,
	  "machineId": machineId,
	  "shiftId": shiftId,
	  "shiftStartDate": shiftTime 
	}
	jsonParams = system.util.jsonEncode(params)        
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)    
	except:        
		result = 0 		      
   	resultData= system.util.jsonDecode(postReturn)
   	#resultData = [{"isNew":1,"ShiftHours":8,"HourlyTarget":160}]
	dataList = []
   	for i in resultData:
   		isNew = i.get("isNew")	
   		if isNew==1 or isNew==True:
   			shiftHours = i.get("ShiftHours")
   			Target = i.get("HourlyTarget")
   			break	
   		Target = i.get("Objective")						
   		Hours = i.get("HourSequence")		
   		Production = i.get("ProductionQty")        
   		Scrap = i.get("ScrapOty")
   		try:
			difference = int(Target) - int(Production)
			completionPercent = (float(Production)/float(Target)) * float(100)
		except:
			difference = 0
			completionPercent = 0
   		Comment = i.get("Comments")
   		reservedField = 0
   		myList = [Hours,Target,Production,Scrap,difference,completionPercent,Comment,reservedField] 
   		print myList         
   		dataList.append(myList)
   		  
   	if isNew==1 or isNew==True:
   		for row in range(shiftHours):
   			Hours = row+1
   			Production = 0         
   			Scrap = 0
   			try:
				difference = int(Target) - int(Production)
				completionPercent = (float(Production)/float(Target)) * float(100)
			except:
				difference = 0
				completionPercent = 0
   			Comment = ""
   			reservedField = 0
   			myList = [Hours,Target,Production,Scrap,difference,completionPercent,Comment,reservedField]         
   			print myList 
   			dataList.append(myList)		
   	else:
   		pass	
   	
   	headers = ["Hour","Target","Production","Scrap","Difference","Status","Comment","reservedField"] 
   	resultDetails = system.dataset.toDataSet(headers,dataList)
   	return resultDetails

def postHourlyProductionManualDetails(hourlyDetails):   		
	apiPath = "ManualProduction/AddDataInHourlyProduction"
	url = URLPath + apiPath		
	jsonParams = system.util.jsonEncode(hourlyDetails)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		system.perspective.print("PostReturn",postReturn)
	except:		
		result = 0
		pass
	return result
	
def postDowntimeManualDetails(productionDetails):   		
	apiPath = "ManualProduction/AddDataInManualProductionDowntime"
	url = URLPath + apiPath		
	jsonParams = system.util.jsonEncode(productionDetails)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		#print("PostReturn",postReturn)
	except:		
		result = 0
		pass
	return postReturn
	
def getShiftDetails(inputShiftId):
	apiPath = "Shifts/GetShift/1"
	url = URLPath + apiPath

	request = urllib2.Request(url)
	response=urllib2.urlopen(request)
	data = system.net.httpGet(url)
	
	resultData= system.util.jsonDecode(data)
	dataList = []
	currentDate  =system.date.now()
	for i in resultData:	
		shiftId = i.get("Id")		
		if inputShiftId == shiftId:		
			shiftName = i.get("name")
			startDate = i.get("startDate")
			startDate = startDate.replace("T", " " )
			endDate = i.get("endDate")
			endDate = endDate.replace("T", " " )
			shiftStartDate = system.date.parse(startDate)
			shiftEndDate = system.date.parse(endDate)
			ShiftHours = system.date.hoursBetween(shiftStartDate,shiftEndDate)	
			CompletedHours = system.date.hoursBetween(shiftStartDate,currentDate)		
		else:
			continue
	return shiftId,shiftName,shiftStartDate,shiftEndDate,CompletedHours	
