import re
import json
import urllib2, urllib
from datetime import datetime


URLPath = 'http://172.28.3.206/FactoryMagixTOKENAPI/api/'

loginId = 'ODD919472'
Password = 'ODD@123'
TokenDetails = Authentication.Login(loginId,Password)
token = TokenDetails['token']

#GET API ------------------------------------------------------------------------------>      : 
apiPath = "MaintenanceOperatorConsoleRM/GetMaintenanceOperatorConsoleWorkOrdersonInput?EnterpriseId="+str(0)+"&PlantId="+str(0)+"&AreaId="+str(0)+"&LineId="+str(0)+"&MachineId="+str(0)+"&UserId="+str(63)
url = URLPath + apiPath

resultData=None
client = system.net.httpClient()
header= {'Authorization': 'Bearer ' + token}

data = client.get(url,headers=header)
if data.good:    
	resultData=data.json
print 'ResultData : ', resultData


#POST  API ------------------------------------------------------------------------------>      : 
apiPath = "MaintenanceOperatorConsoleRM/AddRMNotes"
url = URLPath + apiPath

writeData = {
			  "isActive": True,
			  "createdBy": 1,
			  "rmNotes": 'TEST AUTH',
			  "rmOrderId": int(93),
			  "shiftId": int(1)
			}

jsonParams = system.util.jsonEncode(writeData)		
header= {'Authorization': 'Bearer ' + token}

try:
	postReturn = system.net.httpPost(url,'application/json',jsonParams,headerValues=header)
	print 'postReturn',postReturn
except:
	pass