import re
import json
import urllib2, urllib
import datetime
import system.date
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_JEMESAdhocAPIZAC").value  
#URLPath1 = system.tag.readAsync("[default]JMES_InternalTags/urlAPI_zag").value
#URLPath = "http://elephant040001/JEMESAdhocAPIZAC/api/"      
def GetOPRInfo(enterpriseID,plantID,WorkOrderId,ShiftId):
	script_name = "AdhocAPIZAC.GetOPRInfo(enterpriseID,plantID,WorkOrderId,ShiftId)"
	apiPath="ProductionSummary/GetOperatorRoleUsers/"+str(enterpriseID)+"/"+str(plantID)+"/"+str(WorkOrderId)+"/"+str(ShiftId)
	url = URLPath + apiPath
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Get ")
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		dataList = []
		dataList1 = []
		s_no = 0
		for i in resultData: 
			           
			LoginId = i.get("LoginId")
			userName = i.get("userName")
			userId = i.get("userId")
			s_no =  s_no +1  
			myList = [s_no,userId,userName,LoginId]
			#myList1 = [userId,userName]         
			dataList.append(myList) 
			#dataList1.append(myList1)   
		headers = ["s_no","userId","LoginId","userName"]
		#headers1 = ["userId","userName"]
		resultDetails = system.dataset.toDataSet(headers,dataList)    
		#resultDetails1 = system.dataset.toDataSet(headers1,dataList1)
		return resultDetails

	except Exception as e:
	    errorMessage= script_name  +' Exception - '+  str(e)
	    Authentication.exceptionLogger(errorMessage)
	    
def Date_db_format_to_UI(date_string):
	date_format = "yyyy-MM-dd hh:mm:ss"
	d = date_string.replace("T", " ")
	date = system.date.parse(d, date_format)
	d =system.date.format(date, "yyyy-MM-dd hh:mm:ss")
	return d
	
def Date_UI_format_to_db(date_string):
	#d ="23-12-15 06:54:29.000"
	t =system.date.parse(str(date_string),"yyyy-MM-dd HH:mm:ss")
	endTime = str(system.date.format(t,"yyyy-MM-dd'T'HH:mm:ss.ss'Z'"))
	return endTime
	       
def PostOPRInfo(userID,workOrderId,operatorId,startTime,endTime,comment,shiftId,lineId,isDirectLabour):
	apiPath = "OperatorInfo/CreateOperatorInfo"
	script_name = "AdhocAPIZAC.PostOPRInfo(enterpriseID,plantID,WorkOrderId,ShiftId,lineId,isDirectLabour)"
	url = URLPath + apiPath	
	print("date is")
#	today = system.date.now()
#	t =  system.date.format(today, "yyyy-MM-dd HH:mm:ss.SSS")
	print(url)
	system.perspective.print("date is")
	#system.perspective.print(t)	
	writeData = {
	  "isActive": True,
	  "createdBy": userID,
	  "createdOn": "2023-12-15T06:54:29.002Z",
	  "modifiedBy": 0,
	  "modifiedOn":"2023-12-15T06:54:29.002Z",
	  "workOrderId": workOrderId,
	  "workorderDate":"2023-12-15T06:54:29.002Z",
	  "operatorId": operatorId,
	  "startTime": Date_UI_format_to_db(startTime),
	  "endTime":Date_UI_format_to_db(endTime),
	  "comment": comment,
	  "shiftId": shiftId,
	  "lineId": lineId,
	  "isDirectLabour": isDirectLabour
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
	print(result)
	return result
	
def PostOPRInfo_endtime(ID,userID,operatorId,startTime,endTime,comment,isDirectLabour):
	apiPath = "OperatorInfo/UpdateOperatorInfo/"+str(ID)
	script_name = "AdhocAPIZAC.PostOPRInfo_endtime(ID,userID,operatorId,startTime,endTime,comment,isDirectLabour)"
	url = URLPath + apiPath	
	print("date is")
	print(url)
	system.perspective.print("date is")	
	writeData = {
	  "isActive": True,
	  "createdBy": 0,
	  "createdOn": "2023-12-15T06:54:29.002Z",
	  "modifiedBy": userID,
	  "modifiedOn":"2023-12-15T06:54:29.002Z",
	  "workOrderId":0,
	  "id": ID,
	  "workorderDate":"2023-12-15T06:54:29.002Z",
	  "operatorId": operatorId,
	  "startTime": Date_UI_format_to_db(startTime),
	  "endTime":Date_UI_format_to_db(endTime),
	  "comment": comment,
	  "shiftId": 0,
	  "lineId": 0,
	  "isDirectLabour": isDirectLabour
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
	print(result)
	return result


	
def GetOPRInfoList(WorkOrderId,ShiftId,LineId):
	script_name = "AdhocAPIZAC.GetOPRInfoList(WorkOrderId,ShiftId,LineId)"
	apiPath="OperatorInfo/GetOperatorInfoList/"+str(WorkOrderId)+"/"+str(ShiftId)+"/"+str(LineId)
	url = URLPath + apiPath
	print(url)
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: Get ")
		request = urllib2.Request(url)
		response=urllib2.urlopen(request)
		data = system.net.httpGet(url)
		resultData= system.util.jsonDecode(data)
		dataList = []
		dataList1 = []
		s_no = 0
		for i in resultData: 
			actions = "actions" 
			Id = i.get("Id")
			OperatorId = i.get("OperatorId")
			EmployeeName = i.get("EmployeeName")
			EmployeeId = i.get("EmployeeId")
			StartTime = Date_db_format_to_UI(i.get("StartTime"))
			EndTime = Date_db_format_to_UI(i.get("EndTime"))
			OperatorType = i.get("OperatorType")
			Comment =  i.get("Comment")
			s_no =  s_no +1   
			myList = [Id,s_no,OperatorId,EmployeeName,StartTime,EndTime,OperatorType,actions,EmployeeId,Comment]        
			dataList.append(myList)    
		headers = ["Id","s_no","operatorId","employeeName","startTime","EndTime","OperatorType","actions","EmployeeId","Comment"]
		resultDetails = system.dataset.toDataSet(headers,dataList)    
		return resultDetails

	except Exception as e:
	    errorMessage= script_name  +' Exception - '+  str(e)
	    Authentication.exceptionLogger(errorMessage)
	    
	    
def DeleteOPRInfo(ID):
	apiPath = "OperatorInfo/DeleteOperatorInfo/"+str(ID)
	script_name = "AdhocAPIZAC.DeleteOPRInfo(ID)"
	url = URLPath + apiPath	
	print(url)	
	writeData = {
	  "id": ID
	}
	print(writeData)
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		system.perspective.print("API URL is: "+str(url))
		system.perspective.print("API Method is: post ")
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
		system.perspective.print("DeleteReturn"+str(postReturn))
	except Exception as e:
		result =0
		errorMessage= script_name  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)
	print(result)
	return result


