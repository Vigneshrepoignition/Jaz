import re
import json
import urllib2, urllib
import datetime
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_JEMESAdhocAPIZAC").value

def GetOPRInfo(enterpriseID,plantID,WorkOrderId,ShiftId):

    apiPath="ProductionSummary/GetOperatorRoleUsers/"+str(enterpriseID)+"/"+str(plantID)+"/"+str(WorkOrderId)+"/"+str(ShiftId)
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
    print "resultData",resultData
    dataList = []

    for i in resultData:            
        userName = i.get("userName")
        userId = i.get("userId")    
        myList = [userId,userName]         
        dataList.append(myList)    

    headers = ["userId","userName"]
    resultDetails = system.dataset.toDataSet(headers,dataList)    
    return resultDetails