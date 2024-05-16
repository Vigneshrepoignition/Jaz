#Production Operator Console Screen
def updateMESControls(workorderId):
	#---------------------------------------------
	apiPath = "ProductionOperatorConsole/GetMESControlMachinesDetails/WorkOrderId:int?WorkOrderId="+str(workorderId)		
	url = URLPath + apiPath
	resultData = None
	client = system.net.httpClient()
	data = client.get(url)

	if data.good:    
		resultData = data.json

	dataList = []		
	SrNo = 0
	print resultData
	if 	resultData:
		print "Inside If going for For Loop"
		for i in resultData:	
			print "Inside For Loop"		
			componentFeedQty = i.get("RMQty")
			machineName = i.get("MachineName")
			loadedMoldId = i.get("LoadedTool")	
	#----------------------------------------------
			print "Checkpoint 1"	
			if (componentFeedQty > 0.00) and (componentFeedQty != 'Null'):
				isComponentFeed = 1
			else:
				isComponentFeed = 0
				
			if loadedMoldId > 0 and loadedMoldId != 'Null':
				isMoldLoaded = 1
			else:
				isMoldLoaded = 0	
			print("machineName :- " +str(machineName))	
			print "Checkpoint 2"	
			defaultTagPath = system.tag.read("[default]JMES_InternalTags/DafaultTagPath.value").value	
			print "Checkpoint 3"
			mesMsgTagPath = defaultTagPath + machineName + "/MESMessage.value"
			print "Checkpoint 4"
			MESOnOffTagPath = str(defaultTagPath)+str(machineName)+"/MESOnOff.value"
			print "Checkpoint 5"					
			MESOnOff = system.tag.read(MESOnOffTagPath).value	
			print "Checkpoint 6"
			print("MESOnOff :- " +str(MESOnOff))	
			if 	MESOnOff == 1 or MESOnOff == True:	
				MESControlTagPath = str(defaultTagPath)+str(machineName)+"/MESControl.value"															
				machineStatusTagPath = str(defaultTagPath)+str(machineName)+"/MachineStatus.value"
				machineStatus = system.tag.read(machineStatusTagPath).value
				machineRepairTagPath = str(defaultTagPath)+str(machineName)+"/Repair.value"					
				machineRepair = system.tag.read(machineRepairTagPath).value					
				print("machineStatus :- " +str(machineStatus))
				print("machineRepair :- " +str(machineRepair))
				print("isComponentFeed :- " +str(isComponentFeed))
				print("isMoldLoaded :- " +str(isMoldLoaded))
				if (machineStatus==5):		
					system.tag.writeAsync(MESControlTagPath,2)
					print("MESControlTag :- 2")
					system.tag.writeAsync(mesMsgTagPath,"Machine is in Alert Mode.")
					print("Machine is in Alert Mode.")
				elif (machineRepair==2):
					system.tag.writeAsync(MESControlTagPath,2)
					print("MESControlTag :- 2")
					system.tag.writeAsync(mesMsgTagPath,"Machine is in Rapair Mode.")	
					print("Machine is in Rapair Mode.")
				elif isComponentFeed == 0:	
					system.tag.writeAsync(MESControlTagPath,2)
					print("MESControlTag :- 2")			
					system.tag.writeAsync(mesMsgTagPath,"Component Validations is Not OK")	
					print("Component Validations Are Not OK")
				elif isMoldLoaded == 0:	
					system.tag.writeAsync(MESControlTagPath,2)
					print("MESControlTag :- 2")			
					system.tag.writeAsync(mesMsgTagPath,"Mold Valodation Not Ok")	
					print("Mold Validations Are Not Ok")
				else:
					system.tag.writeAsync(MESControlTagPath,1)
					print("MESControlTag :- 1")
					system.tag.writeAsync(mesMsgTagPath,"Validations Are OK")
					print("Validations Are OK")	
			else :
				print("Not Applicable")
				mesMsgTagPath = defaultTagPath + machineName + "/MESMessage.value"
				system.tag.writeAsync(mesMsgTagPath,"Not Applicable")	
			print "------------------------------------------------------------------------"	
	else:		
#		system.perspective.print("No Machine present with MES Control ON ")
		print("No Machine present with MES Control ON ")
		pass