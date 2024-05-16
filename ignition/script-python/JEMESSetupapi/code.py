import re
import json
import urllib2, urllib
import datetime
import system.date
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_JEMESSetupapi").value
#URLPath = "http://elephant040001/JEMESSetupapi/api/"


def Post_addworkorderchangeoverlogo(workOrderId):
	apiPath = "wochangeover/create/addworkorderchangeoverlog"
	script_name = "JEMESSetupapi.Post_addworkorderchangeoverlogo(workOrderId)"
	url = URLPath + apiPath	
	print(url)
	#system.perspective.print(t)	
	writeData = {
	  "workOrderId": workOrderId,
	}
	print(writeData)
	jsonParams = system.util.jsonEncode(writeData)		
	result = 1
	try:
		postReturn = system.net.httpPost(url,'application/json',jsonParams)
#		print("PostReturn",postReturn)
	except Exception as e:
		result =0
		errorMessage= script_name  +' Exception - '+  str(e)
		Authentication.exceptionLogger(errorMessage)
	return result


def PostShiftProductionDetails(ID,goodqty,badqty):
	apiPath = "shiftProduction/update/shiftProduction"
	script_name = "PostShiftProductionDetails(ID,goodqty,badqty)"
	url = URLPath + apiPath	
#	today = system.date.now()
#	t =  system.date.format(today, "yyyy-MM-dd HH:mm:ss.SSS")
#	system.perspective.print("date is")
	#system.perspective.print(t)	
	writeData = {
	  "id": ID,
	  "production": goodqty,
	  "scrap": badqty
	}
#	print(writeData)
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
#	print(result)
	return result