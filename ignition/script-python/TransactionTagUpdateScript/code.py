import re
import json
import urllib2, urllib
import system
import sys
import traceback
import decimal
import random
import time

URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
defaultPath=system.tag.read("[default]JMES_InternalTags/DafaultTagPath").value

def updateTransactionTags():	
#	machineDetailsList = [{"machineId":29,"machineName":'MD279J_001_WF'},
#	{"machineId":30,"machineName":'MD275C_002'},
#	{"machineId":54,"machineName":'MD279B_002'},
#	{"machineId":32,"machineName":'MYE_AFUS_120A_005'},
#	{"machineId":33,"machineName":'MYE_AFUS_120A_006'},
#	{"machineId":36,"machineName":'MYE_AVIS_131A_001'},
#	{"machineId":31,"machineName":'MYE_COMM_100A_003'},
#	{"machineId":41,"machineName":'MYE_EASS_200A_003'},
#	{"machineId":39,"machineName":'MYE_FWSS_210A_003'},
#	{"machineId":42,"machineName":'MYE_MASS_301A_001'},
#	{"machineId":8,"machineName":'QCH_AVIS_130_001'}
#BA_H01_0050_0009
#BA_H01_0050_0008,BA_H01_0050_0019
#	
#	]
	
	machineDetailsList = [	{"machineId":28,"machineName":'BA_H01_0050_0008'},
							{"machineId":29,"machineName":'BA_H01_0050_0009'},
							{"machineId":00,"machineName":'BA_H01_0050_0016'},
							{"machineId":00,"machineName":'BA_H01_0050_0035'},
#							{"machineId":42,"machineName":'BA_H01_0220_0041'},
							
							{"machineId":8,"machineName":'QCH_AVIS_130_001'},
							{"machineId":00,"machineName":'MYE_COMM_100A_003'},
							{"machineId":00,"machineName":'MYE_WIND_110A_011'},
							{"machineId":30,"machineName":'MD275C_002'}	
						]
	for machineDetails in machineDetailsList:
		machineId = machineDetails.get("machineId")
		machineName = machineDetails.get("machineName")		
		parameterList = ["GoodQty"] #updateMasterTable.getParameterList(machineId)
		currentHour = system.date.getHour24(system.date.now())
		currentMinute= system.date.getMinute(system.date.now())

		for parameterName in parameterList:
			tagPath = str(defaultPath)+str(machineName)+"/"+str(parameterName)
			print tagPath
			parameterValue = system.tag.read(tagPath).value
			print "parameterValue:" + str(parameterValue)
			if currentHour in [6,14,22] and currentMinute<2:					
				system.tag.writeAsync(tagPath, 0)						
			elif parameterName=="GoodQty":			
				addNum = random.choice([0,1,2,3])	
				print "addNum"
				print addNum	
				system.tag.writeAsync(tagPath, (parameterValue+addNum))				
			print parameterValue
			
def simulateMachineStatusTags():	
	machineDetailsList = [{"machineId":156,"machineName":'MD279J_001_WF'},{"machineId":30,"machineName":'MD275C_002'},{"machineId":109,"machineName":'MD279B_002'},{"machineId":109,"machineName":'MYE_AFUS_120A_005'},{"machineId":109,"machineName":'MYE_AFUS_120A_006'},{"machineId":109,"machineName":'MYE_AVIS_131A_001'},{"machineId":109,"machineName":'MYE_COMM_100A_003'},{"machineId":109,"machineName":'MYE_EASS_200A_003'},{"machineId":109,"machineName":'MYE_FWSS_210A_003'},{"machineId":109,"machineName":'MYE_MASS_301A_001'}]
	for machineDetails in machineDetailsList:
		machineId = machineDetails.get("machineId")
		machineName = machineDetails.get("machineName")		
		parameterList = ["MachineStatus","NGQty"] 
		for parameterName in parameterList:
			tagPath = "[default]JEMESMachines/"+str(machineName)+"/"+str(parameterName)
			parameterValue = system.tag.read(tagPath).value
			if parameterValue >= 500000:
				system.tag.writeAsync(tagPath, 0)
			elif parameterName=="NGQty":	
				#time.sleep(180000)
				addNum = random.choice([0,1])			
				system.tag.writeAsync(tagPath, (parameterValue+addNum))		
			else :
				#time.sleep(180000)
				machineStatus = random.choice([1,2,4,5])
				system.tag.writeAsync(tagPath, machineStatus)
			print parameterValue			
			
