import re
import json
import urllib,urllib2
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
#URLPath = system.tag.read("[default]JMES_InternalTags/urlSITAPI").value

def getSparePart():
	apiPath = "MaintenanceOperatorConsoleRM/GetSparePartDetailsBySparePartID/1"
	url = URLPath + apiPath
	print("URL path",url)
#	request = urllib2.Request(url)
#	response=urllib2.urlopen(request,timeout=10)
#	data = system.net.httpGet(url)
#	
#	resultData= system.util.jsonDecode(data)
#	dataList = []
#	print("spare part data",resultData)
#	for i in resultData:	
#		ID = i.get("id")
#		sparePartName = i.get("sparePartName")
#		myList = [ID,sparePartName] 		
#		dataList.append(myList)	
#		
#	headers = ["ID","sparePartName"]
#	resultDetails = system.dataset.toDataSet(headers,dataList)
#	return resultDetails
