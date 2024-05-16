import re
import json
import urllib2, urllib
import datetime
import system.date

URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_fpsi-ignition01").value  

URLPath1 = system.tag.read("[default]JMES_InternalTags/urlAPI_fpsi-ignition1").value
URLPath2 = system.tag.read("[default]JMES_InternalTags/urlAPI_fpsi-ignition01_jemessetup").value

URLPath_jemesSetup = system.tag.read("[default]JMES_InternalTags/urlAPI_jemesSetup").value



################## URL path  ################## 
def Post_and_get_serailnumber(startDate,endDate,item1):
	apiPath = "production/get/completeDataList/"
 	script_name = "fpsi_ignition01.Post_and_get_serailnumber"
 	url = URLPath + apiPath	

 	writeData = {

 	    "startDate": startDate,
 	    "endDate":endDate,
 	    "lineList": [
 	      {
 	        "item1":item1,
 	        "item2": "0"
 	      }
 	    ],
 	    "serialNo": "",
 	    "typeCodes": [
 	      {
 	        "id": 0,
 	        "displayName": "",
 	        "typeDesc": "",
 	        "typeCode": 0
 	      }
 	    ]
 	  }
 	jsonParams = system.util.jsonEncode(writeData)		
 	result = 1
 	dataList = []
 	try:
 		system.perspective.print("API URL is: "+str(url))
 		system.perspective.print("API Method is: Post method ")
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		data =  system.util.jsonDecode(postReturn)
		#print("PostReturn",data)
		postReturn1 = list(data)
		#print(type(postReturn1))
		system.perspective.print(data)
		for i in data:
			
			serialNo = i.get("serialNo")
			uniqueID = i.get("uniqueID")
			idd = i.get("id")
			myList = [uniqueID,idd,serialNo]    
			dataList.append(myList)
			headers = ["uniqueID","idd","serialNo"]
			resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
 	except Exception as e:
 		result =0
 		errorMessage= script_name  +' Exception - '+  str(e)
 		Authentication.exceptionLogger(errorMessage)
 		system.perspective.print(errorMessage)
 		return result
 	
################## URL path  ##################
def GetEquipmentDataList(serialnumber):
	script_name = "fpsi_ignition01.GetEquipmentDataList"
	apiPath="equipment/get/getEquipmentDataListBySerial/"+str(serialnumber)
	url = URLPath + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Get ")
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		dataList = []
		for i in resultData:           
			idd = i.get("id")
			lineName = i.get("lineName")
			status = i.get("status")
			nextEquipment= i.get("nextEquipment")
			currentEquipment= i.get("currentEquipment")
			equipmentID= i.get("equipmentID")
			prodStatus= i.get("prodStatus")
			if prodStatus == True:
				prodStatus = "ok"
			elif prodStatus == False:
				prodStatus = "Not ok"
			runNumber= i.get("runNumber")
			fk_LineID= i.get("fk_LineID")
			isFinished= i.get("isFinished")
			if isFinished == True:
				isFinished = "Yes"
			elif isFinished == False:
				isFinished = "No"
			rawIsFinished= i.get("rawIsFinished")
			typeCode= i.get("typeCode")
			createdAt= i.get("createdAt") 
			myList = [idd,lineName,status,nextEquipment,currentEquipment,equipmentID,prodStatus,runNumber,fk_LineID,isFinished,rawIsFinished,typeCode,createdAt]        
			dataList.append(myList) 

		headers = ["idd","lineName","status","nextEquipment","currentEquipment","equipmentID","prodStatus","runNumber","fk_LineID","isFinished","rawIsFinished","typeCode","createdAt"]
		resultDetails = system.dataset.toDataSet(headers,dataList)    
		return resultDetails

	except Exception as e:
	    errorMessage= script_name  +' Exception - '+  str(e)
	    Authentication.exceptionLogger(errorMessage)
	    system.perspective.print(errorMessage)
	    
################## URL path ##################	 
def GetEquipmentValue(idd):
	script_name = "fpsi_ignition01.GetEquipmentValue"
	apiPath="equipment/get/equipmentValue/"+str(idd)
	url = URLPath + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Get ")
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		dataList = []
		for i in resultData:           
			fkTagID = i.get("fkTagID")
			val = i.get("val")
			tag = i.get("tag")
			tagName= i.get("tagName")

			myList = [fkTagID,val,tag,tagName]        
			dataList.append(myList) 

		headers = ["fkTagID","val","tag","tagName"]
		resultDetails = system.dataset.toDataSet(headers,dataList) 
		#print(resultDetails)   
		return resultDetails

	except Exception as e:
	    errorMessage= script_name  +' Exception - '+  str(e)
	    Authentication.exceptionLogger(errorMessage)
	    system.perspective.print(errorMessage)
	    #print(errorMessage)

      
################## URL path 1 ##################	       
def PostDowntimeLog():
	script_name = "fpsi_ignition01.PostDowntimeLog"
	apiPath ="downtime"
 	url = URLPath1 + apiPath	
	print(url)

	writeData = {
	  "startTime": "2024-01-08T08:15:00",
	  "endTime": "2024-01-08T08:45:00",
	  "reasonCode": 102,
	  "fkUserID": 321,
	  "description": "Makine arızası"
	}
	
	print(writeData)
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Post method ")
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		print("PostReturn",postReturn)
	except Exception as e:
		result =0
		errorMessage= script_name  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)
	return result


################## URL path 1 ##################
### For Downtime ###
def Getreasonsubtypelist():
	script_name = "fpsi_ignition01.Getreasonsubtypelist"
	apiPath="reasonSubType/public/get/reasonSubTypeList"
	url = URLPath1 + apiPath
	s_no = 0
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Get ")
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		dataList = []
		for i in resultData: 
			s_no = s_no+1          
			reasonSubTypeId = i.get("reasonSubTypeId")
			reasonSubTypeName = i.get("reasonSubTypeName")
#			createdBy = i.get("createdBy")
#			createdOn = i.get("createdOn")
#			modifiedBy = i.get("modifiedBy")
#			modifiedOn = i.get("modifiedOn")
#			isActive = i.get("isActive")
#			isArchive = i.get("isArchive")
#			reasonTypeId = i.get("reasonTypeId")

			myList = [s_no,reasonSubTypeId,reasonSubTypeName]#,createdBy,createdOn,modifiedBy,modifiedOn,isActive,isArchive,reasonTypeId]        
			dataList.append(myList) 

		headers = ["s_no","reasonSubTypeId","reasonSubTypeName"]#,"createdBy","createdOn","modifiedBy","modifiedOn","isActive","isArchive","reasonTypeId"]
		resultDetails = system.dataset.toDataSet(headers,dataList) 
		#print(resultDetails)   
		return resultDetails
	except Exception as e:
	    errorMessage= script_name  +' Exception - '+  str(e)
	    Authentication.exceptionLogger(errorMessage)
	    system.perspective.print(errorMessage)
	    
################## URL path 1 ##################
### For Downtime ###	    
def GetResoncode(idd):
	script_name = "fpsi_ignition01.GetResoncode"
	apiPath="reasonCode/public/get/reasonCodeBySubType/"+str(idd)
	url = URLPath1 + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Get ")
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		dataList = []
		s_no =0
		for i in resultData:  
			s_no = s_no+1          
			reasonCodeId = i.get("reasonCodeId")
			reasonCodeName = i.get("reasonCodeName")
#			code = i.get("code")
#			typeId = i.get("typeId")
#			reasonSubTypeId = i.get("reasonSubTypeId")
#			comments = i.get("comments")
#			createdBy = i.get("createdBy")
#			createdOn = i.get("createdOn")
#			modifiedBy = i.get("modifiedBy")
#			modifiedOn = i.get("modifiedOn")
#			isArchive = i.get("isArchive")
#			isActive = i.get("isActive")


			myList = [s_no,reasonCodeId,reasonCodeName]#,code,typeId,reasonSubTypeId,comments,createdBy,createdOn,modifiedBy,modifiedOn,isArchive,isActive]        
			dataList.append(myList) 

		headers = ["s_no","reasonCodeId","reasonCodeName"]#,"code","typeId","reasonSubTypeId","comments","createdBy","createdOn","modifiedBy","modifiedOn","isArchive","isActive"]
		resultDetails = system.dataset.toDataSet(headers,dataList) 
		#print(resultDetails)   
		return resultDetails

	except Exception as e:
	    errorMessage= script_name  +' Exception - '+  str(e)
	    Authentication.exceptionLogger(errorMessage)
	    system.perspective.print(errorMessage)

################## URL path 1 ##################
### For Hourly manual bad qty ###
def Getbadreasonsubtypelist():
	script_name = "fpsi_ignition01.Getbadreasonsubtypelist"
	apiPath="reasonCode/public/get/badQuantityReasonSubTypes"
	url = URLPath1 + apiPath
	s_no = 0
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Get ")
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		dataList = []
		for i in resultData: 
			s_no = s_no+1          
			reasonSubTypeId = i.get("reasonSubTypeId")
			reasonSubTypeName = i.get("reasonSubTypeName")
#		    "reasonTypeId": 5,
#		    "isActive": true,
#		    "isSuccess": false,
#		    "error": null

			myList = [s_no,reasonSubTypeId,reasonSubTypeName]#,createdBy,createdOn,modifiedBy,modifiedOn,isActive,isArchive,reasonTypeId]        
			dataList.append(myList) 

		headers = ["s_no","reasonSubTypeId","reasonSubTypeName"]#,"createdBy","createdOn","modifiedBy","modifiedOn","isActive","isArchive","reasonTypeId"]
		resultDetails = system.dataset.toDataSet(headers,dataList) 
		#print(resultDetails)   
		return resultDetails
	except Exception as e:
	    errorMessage= script_name  +' Exception - '+  str(e)
	    Authentication.exceptionLogger(errorMessage)
	    system.perspective.print(errorMessage)
	    #print(errorMessage)
	    
################## URL path 1 ##################
### For Hourly manual bad qty ###    
def GetbadResoncode(idd):
	script_name = "fpsi_ignition01.GetbadResoncode"
	apiPath="reasonCode/public/get/reasonCodeBySubTypeAndType/"+str(idd)
	url = URLPath1 + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Get ")
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		dataList = []
		s_no =0
		for i in resultData:  
			s_no = s_no+1          
			reasonCodeId = i.get("reasonCodeId")
			reasonCodeName = i.get("reasonCodeName")
#		    "code": "2A001",
#		    "typeId": 5,
#		    "reasonSubTypeId": 46,
#		    "isSuccess": false,
#		    "error": null


			myList = [s_no,reasonCodeId,reasonCodeName]#,code,typeId,reasonSubTypeId,comments,createdBy,createdOn,modifiedBy,modifiedOn,isArchive,isActive]        
			dataList.append(myList) 

		headers = ["s_no","reasonCodeId","reasonCodeName"]#,"code","typeId","reasonSubTypeId","comments","createdBy","createdOn","modifiedBy","modifiedOn","isArchive","isActive"]
		resultDetails = system.dataset.toDataSet(headers,dataList) 
		#print(resultDetails)   
		return resultDetails

	except Exception as e:
	    errorMessage= script_name  +' Exception - '+  str(e)
	    Authentication.exceptionLogger(errorMessage)
	    system.perspective.print(errorMessage)

### identify manual or auto the line is ### not test
def identify_auto_or_manual(lineid):
	script_name = "fpsi_ignition01.identify_auto_or_manual"
	URLPath_jemesSetup = "http://fpsi-ignition01/jemessetup/api/"
	apiPath="lineAttribute/get/lineAttributeByLineId"
 	url = URLPath_jemesSetup + apiPath	

 	writeData = {
 	  "plantHierarchyLineId": str(lineid)
 	}
 	jsonParams = system.util.jsonEncode(writeData)		
 	result = 1
 	dataList = []
 	try:
 		#system.perspective.print("API URL is: "+str(url))
 		#system.perspective.print("API Method is: Post method ")
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		data =  system.util.jsonDecode(postReturn)
		#print("PostReturn",data)
		#system.perspective.print(postReturn)
		postReturn1 = list(data)
		#print(type(postReturn1))
		#print(postReturn1)
		#system.perspective.print(data)
		for i in data:
			autoMode = i.get("autoMode")
			if autoMode == True:
				resultDetails = "Auto"
			elif autoMode == False:
				resultDetails = "Manual"
		return resultDetails
 	except Exception as e:
 		result =0
 		errorMessage= script_name  +' Exception - '+  str(e)
 		Authentication.exceptionLogger(errorMessage)
 		#system.perspective.print(errorMessage)
 		print(errorMessage)
 		return result

#list_1 = [1, 2, 3, 4]
#list_2 = ['a', 'b', 'c']
#
#for i, j in zip(list_1, list_2):

### manual and auto production grid ### -----
def Manual_auto_Production_details(lineID):
	script_name = "fpsi_ignition01.Manual_auto_Production_details"
	apiPath="prodCountCache/get/prodCountCacheByLineForCurrentShift/"+str(lineID)
	apiPath2="downtime/public/get/downtimeHistoryForCurrentShift/"+str(lineID)
	url = URLPath2 + apiPath
	url2 = URLPath2 + apiPath2
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Get ")
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
#		
#		system.perspective.print("API URL is: "+str(url2))
#		system.perspective.print("API Method is: Get ")
#		request1 = urllib2.Request(url2)
#		response1=urllib2.urlopen(request1)
#		data1 = system.net.httpGet(url2)
#		resultData1= system.util.jsonDecode(data1)
#		system.perspective.print(resultData1)
		
		dataList = []
	
		#new_data = fpsi_ignition01.Manual_auto_Downtime_grid(lineId=lineID)
		for i in resultData:          
			isSuccess = i.get("isSuccess")
			error = i.get("error")
			idd = i.get("id")
			badQuantity = i.get("badQuantity")
			goodQuantity = i.get("goodQuantity")
			fkLineID = i.get("fkLineID")
			hourStart = i.get("hourStart")
			hourEnd = i.get("hourEnd")
			downtime = 0
#			downtime = j.get("downtime")
			myList = [isSuccess,error,idd,badQuantity,goodQuantity,fkLineID,hourStart,hourEnd]        
			dataList.append(myList)
		
		
		
		headers = ["isSuccess","error","idd","badQuantity","goodQuantity","fkLineID","hourStart","hourEnd"]
		resultDetails = system.dataset.toDataSet(headers,dataList) 
#		resultDetails1 = fpsi_ignition01.Manual_auto_Downtime_grid(lineId)
#		redata = resultDetails + resultDetails1
#		system.perspective.print(redata) 
		return resultDetails
 	except Exception as e:
 		result =0
 		errorMessage= script_name  +' Exception - '+  str(e)
 		Authentication.exceptionLogger(errorMessage)
 		system.perspective.print(errorMessage)
 		#print(errorMessage)
 		return result



### insert downtime history ###	----
def Manual_auto_Downtime_grid(lineId): 
	script_name = "fpsi_ignition01.Manual_auto_Downtime_grid"
	apiPath="downtime/public/get/downtimeHistoryForCurrentShift/"+str(lineId)
	url = URLPath2 + apiPath
	print(url)
	result = 0
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Get ")
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		dataList = []
		
		
		for i in resultData:          
			#lineID = i.get("lineID")
			#hourStart = i.get("hourStart")
			#hourEnd = i.get("hourEnd")
			availability1 = i.get("availability") 
			system.perspective.print("avail")
			system.perspective.print(availability1)
			availability = availability1/60
			capacity1 = i.get("capacity")
			system.perspective.print(capacity1)
			capacity = capacity1/60
			performance1 = i.get("performance")
			system.perspective.print(performance1)
			performance = performance1/60
			downtime = [availability,capacity,performance]
#			downtime = [60,1140,1200]
			myList = [downtime]        
			dataList.append(myList) 

		headers = ["downtime"]
		resultDetails = system.dataset.toDataSet(headers,dataList) 

		#print(resultDetails)   
		return resultDetails
 	except Exception as e:
 		result =0
 		errorMessage= script_name  +' Exception - '+  str(e)
 		Authentication.exceptionLogger(errorMessage)
 		system.perspective.print(errorMessage)
 		#print(errorMessage)
 		return result
		

### manual good product load ### -----
def manual_good_product_post(startTime,endTime,quantity,fkLineID):
	script_name = "fpsi_ignition01.manual_good_product_post"
	apiPath="prodCountCache/create/putGoodProdCount"
	
 	url = URLPath2 + apiPath	

	writeData = {
	  "startTime": startTime,
	  "endTime": "2024-02-12T12:43:30.499Z",
	  "quantity": quantity,
	  "fkLineID": fkLineID,
	  "operatorId": 0
	}
	
	#print(writeData)
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Post method ")
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		print("PostReturn",postReturn)
	except Exception as e:
		result =0
		errorMessage= script_name  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print(errorMessage)
	return result

### manual bad product load ### ------
def manual_bad_product_post(startTime,endTime,quantity,fkLineID,status):
	script_name = "fpsi_ignition01.manual_bad_product_post"
	apiPath="prodCountCache/create/putBadProdCount"
	
 	url = URLPath2 + apiPath	
	writeData = {
	  "startTime": startTime,
	  "endTime": "2024-02-12T12:43:30.499Z",
	  "quantity": quantity,
	  "fkLineID": fkLineID,
	  "status": status,
	  "operatorId": 0
	}
	
	print(writeData)
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		#system.perspective.print("API URL is: "+str(url))
		#system.perspective.print("API Method is: Post method ")
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		print("PostReturn",postReturn)
	except Exception as e:
		result =0
		errorMessage= script_name  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)
	return result


def get_count_reasonslist_in_hour(startTime,endTime,lineID):
	script_name = "fpsi_ignition01.get_count_reasonslist_in_hour"
	apiPath="prodCountCache/get/badReasonsByTimeAndLine/"+str(startTime)+"/"+str(endTime)+"/"+str(lineID)
	url = URLPath2 + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Get ")
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		dataList = []
		for i in resultData:  
         	#reasonCodeName
			isSuccess = i.get("isSuccess")
			error = i.get("error")
			idd = i.get("id")
			badQuantity = i.get("badQuantity")
			status = i.get("status")
			fkLineID = i.get("fkLineID")
			hourStart = i.get("hourStart")
			hourEnd = i.get("hourEnd")
			reasonCodeName = i.get("reasonCodeName")		
			myList = [isSuccess,error,idd,badQuantity,status,fkLineID,hourStart,hourEnd,reasonCodeName]#,code,typeId,reasonSubTypeId,comments,createdBy,createdOn,modifiedBy,modifiedOn,isArchive,isActive]        
			dataList.append(myList) 
		headers = ["isSuccess","error","idd","badQuantity","status","fkLineID","hourStart","hourEnd","reasonCodeName"]#,"code","typeId","reasonSubTypeId","comments","createdBy","createdOn","modifiedBy","modifiedOn","isArchive","isActive"]
		resultDetails = system.dataset.toDataSet(headers,dataList) 
		#print(resultDetails)   
		return resultDetails

	except Exception as e:
	    errorMessage= script_name  +' Exception - '+  str(e)
	    Authentication.exceptionLogger(errorMessage)
	    #print(errorMessage)
	    system.perspective.print(errorMessage)


### manual downtime ### ----
def Downtime_manual_assign(startTime,endTime,reasonCode,fkUserID,comment,fkCreatedByID,lineID):
	script_name = "fpsi_ignition01.Downtime_manual_assign"
	apiPath="downtime/public/insert/downtimeHistory"
 	url = URLPath1 + apiPath	
	writeData = {
		  "startTime":startTime,
		  "endTime":endTime,
		  "reasonCode": reasonCode,
		  "fkUserID": fkUserID,
		  "comment": comment,
		  "fkCreatedByID": fkCreatedByID,
		  "lineID": lineID
		}

	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	system.perspective.print(startTime)
	system.perspective.print(endTime)
	system.perspective.print(reasonCode)
	system.perspective.print(fkUserID)
	system.perspective.print(comment)
	system.perspective.print(fkCreatedByID)
	system.perspective.print(lineID)
	
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Post method ")
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		#print("PostReturn",postReturn)
	except Exception as e:
		result =0
		errorMessage= script_name  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print(errorMessage)
	system.perspective.print("result")
	system.perspective.print(result)
	system.perspective.print("result")
	return result


###Downtime manual delete
def Downtime_history_manual_delete(downtimeiid):
	script_name = "fpsi_ignition01.Downtime_history_manual_delete"
	apiPath="downtime/public/delete/downtimeHistory"

 	url = URLPath1 + apiPath	
 	
	writeData = {
		"id": downtimeiid
	}
	
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Post method ")
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
	except Exception as e:
		result =0
		errorMessage= script_name  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)
	return result
	
	
### auto downtime ### -----
def Downtime_history_manual_update(idd,fkUserID,fkChangedByID,):
	script_name = "fpsi_ignition01.Downtime_history_manual_update"
	apiPath="downtime/public/update/downtimeHistory"

 	url = URLPath1 + apiPath	
 	
	writeData = {
		  "id":idd,
  		  "fkUserID": fkUserID,
		  "fkChangedByID": fkChangedByID,
		  "fkLineId": fkLineId,
		  "startTime": startTime,
		  "endTime": endTime,
		  "fkEquipmentId": fkEquipmentId,
		  "fkReasonCodeId": fkReasonCodeId,
		  "comment": comment
		}
	
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Post method ")
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
	except Exception as e:
		result =0
		errorMessage= script_name  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)
	return result
	
def Downtime_history_auto_update(idd,fkReasonCodeId):
	script_name = "fpsi_ignition01.Downtime_history_auto_update"
	apiPath="downtime/public/update/downtimeHistory"

 	url = URLPath1 + apiPath	
 	
	writeData = {
		  "id":idd,
#  		  "fkUserID": fkUserID,
#		  "fkChangedByID": fkChangedByID,
#		  "fkLineId": fkLineId,
#		  "startTime": startTime,
#		  "endTime": endTime,
#		  "fkEquipmentId": fkEquipmentId,
		  "fkReasonCodeId": fkReasonCodeId
#		  "comment": comment
		}
	
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Post method ")
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
	except Exception as e:
		result =0
		errorMessage= script_name  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)
	return result


def Downtime_history_get(lineid):
	script_name = "fpsi_ignition01.Downtime_history_auto_get"
	apiPath="production/get/downtimeHistoryForCurrentShift"
	#URLPath = "http://fpsi-ignition01/jemesreport/api/"
 	url = URLPath + apiPath	

 	writeData = 	{
 	  "fk_LineID": [
 	    {
 	      "item1": str(lineid),
 	      "item2": "0"
 	    }
 	  ],
 	  "culture": "string",
 	  "ignoreInterval": 0
 	}
 	jsonParams = system.util.jsonEncode(writeData)		
 	result = 1
 	dataList = []
 	actions = 0
 	try:
 		system.perspective.print("API URL is: "+str(url))
 		system.perspective.print("API Method is: Post method ")
 		#print(writeData)
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		#print(postReturn)
		data =  system.util.jsonDecode(postReturn)
		#print("PostReturn",data)
		postReturn1 = list(data)
		#print(type(postReturn1))
		system.perspective.print(data)
		for i in data:
			rowID = i.get("rowID")
			fkLineId = i.get("fkLineId")
			lineName = i.get("lineName")
			totalElapsedTime = i.get("totalElapsedTime")
			fkDowntimeId = i.get("fkDowntimeId")
			fkReasonCodeId = i.get("fkReasonCodeId")
			code = i.get("code")
			startTime = i.get("startTime")
			endTime = i.get("endTime")
			elapsedTime = i.get("elapsedTime")
			fkUserID = i.get("fkUserID")
			userName = i.get("userName")
			reasonSubTypeName = i.get("reasonSubTypeName")
			reasonCodeName = i.get("reasonCodeName")
			colorHEX = i.get("colorHEX")
			shiftName = i.get("shiftName")
			equipmentName = i.get("equipmentName")
			isDelete = i.get("isDelete")
			fkEquipmentId = i.get("fkEquipmentId")
			fkChangedByID = i.get("fkChangedByID")
			fkProjectID = i.get("fkProjectID")
			myList = [rowID,fkLineId,lineName,totalElapsedTime,fkDowntimeId,fkReasonCodeId,code,startTime,endTime,elapsedTime,fkUserID,userName,reasonSubTypeName,reasonCodeName,colorHEX,shiftName,equipmentName,isDelete,fkEquipmentId,fkChangedByID,fkProjectID,actions]    
			dataList.append(myList)
			headers = ["rowID","fkLineId","lineName","totalElapsedTime","fkDowntimeId","fkReasonCodeId","code","startTime","endTime","elapsedTime","fkUserID","userName","reasonSubTypeName","reasonCodeName","colorHEX","shiftName","equipmentName","isDelete","fkEquipmentId","fkChangedByID","fkProjectID","actions"]
			resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
 	except Exception as e:
 		result =0
 		errorMessage= script_name  +' Exception - '+  str(e)
 		Authentication.exceptionLogger(errorMessage)
 		system.perspective.print(errorMessage)
 		#print(errorMessage)
 		return result

def Downtime_auto_set_split(idd,splitTime,fkChangedByID,fkNewReasonCodeId):
	script_name = "fpsi_ignition01.Downtime_auto_set_split"
	apiPath="downtime/public/set/splitDt"
	#ur = "http://10.5.176.164/jemesReport/api/"
	#ur = "http://fpsi-ignition01/jemesReport/api"
 	url = URLPath1 + apiPath
# 	print(type(idd))
# 	print(idd)
# 	print(type(splitTime))
# 	print(splitTime)
# 	print(type(fkChangedByID))
# 	print(fkChangedByID)
# 	print(type(fkNewReasonCodeId))
# 	print(fkNewReasonCodeId)
 	writeData = {
 	  "id": int(idd),
 	  "splitTime": splitTime,
 	  "fkChangedByID": int(fkChangedByID),
 	  "fkNewReasonCodeId": int(fkNewReasonCodeId)
 	}
 	print(writeData)
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
#		print(url)
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Post method ")
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		print("PostReturn",postReturn)
	except Exception as e:
		result =0
		errorMessage= script_name  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print(errorMessage)
		#print(errorMessage)
	return result

### packing serail numbers ###	
def post_scanned_serialnumber(serialNumber,fkWorkOrderId):
	script_name = "fpsi_ignition01.post_scanned_serialnumber"
	apiPath="scannedProducts/get/getWorkorderItemAndSerialNo"
	url = URLPath2 + apiPath	
	system.perspective.print(url)
	writeData = 	{
		  "serialNumber": serialNumber,
		  "fkWorkOrderId": fkWorkOrderId
		}
#	system.perspective.print(writeData)
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Post method ")
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
#		system.perspective.print("PostReturn",postReturn)
	except Exception as e:
		result =0
		errorMessage= script_name  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print(errorMessage)
#	print(result)
	return result
	
def get_workorderitem_and_serialnumber(fkWorkOrderId):
	script_name = "fpsi_ignition01.get_workorderitem_and_serialnumber"
	apiPath="scannedProducts/get/getScannedProductsByWorkOrder"
	url = URLPath2 + apiPath
	writeData = {
	  "fkWorkOrderId": fkWorkOrderId
	}
 	jsonParams = system.util.jsonEncode(writeData)		
 	result = 1
 	dataList = []
 	try:
 		system.perspective.print("API URL is: "+str(url))
 		system.perspective.print("API Method is: Post method ")
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		data =  system.util.jsonDecode(postReturn)
		#print("PostReturn",data)
		postReturn1 = list(data)
		#print(postReturn1)
		#system.perspective.print(data)
		for i in data:
			whole_data = i.get("status")
			serialNumber = whole_data.get("serialNumber")
			controlValue = whole_data.get("controlValue")
			count = whole_data.get("count")
			ok = whole_data.get("ok")
			
			if ok == True:
				ok = "Ok"
			elif ok == False:
				ok = "Not ok"
			myList = [serialNumber,controlValue,count,ok]    
			dataList.append(myList)
			headers = ["serialNumber","controlValue","count","ok"]
			resultDetails = system.dataset.toDataSet(headers,dataList)
		return resultDetails
 	except Exception as e:
 		result =0
 		errorMessage= script_name  +' Exception - '+  str(e)
 		Authentication.exceptionLogger(errorMessage)
 		system.perspective.print(errorMessage)
 		print(errorMessage)
 		return result
 		
 		
### Bomsnap_Scrap  ### 		
def Getbomsnap_scrap(serialNumber):
	#URLPath_jemesSetup = "http://elephant040001/jemesSetup/api/"
	script_name = "fpsi_ignition01.Getbomsnap"
	apiPath="bom/get/bomsnap/"+str(serialNumber)
	url = URLPath2 + apiPath
	result = 0
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Get ")
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		dataList = []
		s_no =0
		actions = 0
		for i in resultData:  
			s_no = s_no+1          
			bomSnapId = i.get("bomSnapId")
			componentName = i.get("componentName")
			description = i.get("description")
			actualQty = i.get("actualQty")
			uom = i.get("uom")
			isChecked = i.get("isChecked")
			if isChecked == 1:
				isChecked = bool(1)
			if isChecked == 0:
				isChecked = bool(0)
			myList = [s_no,bomSnapId,componentName,description,actualQty,actions,uom,isChecked]#,code,typeId,reasonSubTypeId,comments,createdBy,createdOn,modifiedBy,modifiedOn,isArchive,isActive]        
			dataList.append(myList) 

		headers = ["s_no","bomSnapId","componentName","description","actualQty","actions","uom","isChecked"]#,"code","typeId","reasonSubTypeId","comments","createdBy","createdOn","modifiedBy","modifiedOn","isArchive","isActive"]
		resultDetails = system.dataset.toDataSet(headers,dataList) 
		#print(resultDetails)   
		return resultDetails

	except Exception as e:
	    errorMessage= script_name  +' Exception - '+  str(e)
	    Authentication.exceptionLogger(errorMessage)
	    system.perspective.print(errorMessage)
	    return result
	    


def Postbomsnap_scrap(serialNumber,reasonCode,listOfBomSnapID):
	script_name = "fpsi_ignition01.Postbomsnap_scrap"
	apiPath="lineAttribute/create/ScannedComponentTracking"
	url = URLPath2 + apiPath	
	resul = [{"fkBomSnapID":item} for item in listOfBomSnapID]
		
	system.perspective.print(url)
#	writeData = 	{
#	  "serialNo": "string",
#	  "reasonCode": 0,
#	  "listOfBomSnapID": [
#	    {
#	      "fkBomSnapID": 0
#	    }
#	  ]
#	}
	
	writeData = 	{
		  "serialNo": serialNumber,
		  "reasonCode": reasonCode,
		  "listOfBomSnapID": resul
		}
	system.perspective.print(writeData)
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Post method ")
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		system.perspective.print("PostReturn"+str(postReturn))
	except Exception as e:
		result =0
		errorMessage= script_name  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print(errorMessage)
#	print(result)
	return result
	    
	    

###  correlation_1 in  BOM snap
def Getbomsnap_correlations_detailedOtherSerialsInfo(serialNumber):
	#URLPath_jemesSetup = "http://elephant040001/jemesSetup/api/"
	script_name = "fpsi_ignition01.Getbomsnap_correlations_detailedOtherSerialsInfo"
	apiPath="SerialsInfo/get/detailedOtherSerialsInfo/"+str(serialNumber)
	url = URLPath2 + apiPath
	#print(url)
	result = 0
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Get ")
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		dataList = []
		actions = 0
		for i in resultData:          
			internalSerialID = i.get("internalSerialID")
			otherSerialID = i.get("otherSerialID")
			serialValueInternal = i.get("serialValueInternal")
			serialValueOther = i.get("serialValueOther")
			serialType = i.get("serialType")
			createdAt = i.get("createdAt")
			isSuccess = i.get("isSuccess")
			error = i.get("error")
			actions = i.get("actions")
			myList = [internalSerialID,otherSerialID,serialValueInternal,serialValueOther,serialType,createdAt,isSuccess,error,actions]#,code,typeId,reasonSubTypeId,comments,createdBy,createdOn,modifiedBy,modifiedOn,isArchive,isActive]        
			dataList.append(myList) 

		headers = ["internalSerialID","otherSerialID","serialValueInternal","serialValueOther","serialType","createdAt","isSuccess","error","actions"]#,"code","typeId","reasonSubTypeId","comments","createdBy","createdOn","modifiedBy","modifiedOn","isArchive","isActive"]
		resultDetails = system.dataset.toDataSet(headers,dataList) 
		#print(resultDetails)   
		return resultDetails

	except Exception as e:
	    errorMessage= script_name  +' Exception - '+  str(e)
	    Authentication.exceptionLogger(errorMessage)
	    system.perspective.print(errorMessage)
	    #print(errorMessage)
	    return result
	      
###  correlation_2 in  BOM snap	    	    	    	    
def post_correlations_separateAndAddUnmergedSerial(otherSerialID,fkCreatedByID):
	script_name = "fpsi_ignition01.post_correlations_separateAndAddUnmergedSerial"
	apiPath="SerialsInfo/create/separateAndAddUnmergedSerial"
	url = URLPath2 + apiPath	
	#print(url)
	writeData = 	{
		  "otherSerialID": otherSerialID,
		  "fkCreatedByID": 0
		}
	#print(writeData)
	#print(url)
	jsonParams = system.util.jsonEncode(writeData)		
	result = 0
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Post method ")
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		system.perspective.print("PostReturn",postReturn)
	except Exception as e:
		result =0
		errorMessage= script_name  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)
		system.perspective.print(errorMessage)
		#print(errorMessage)
	#print(result)
	return result