import re
import json
import urllib2, urllib

defaultPath=system.tag.read("[default]JMES_InternalTags/DafaultTagPath").value	
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value

def CheckCurrentRMOrders():
	#-Start->---This is used to add Maintenance Flag to the Machine if there is any already RM Order running.
	apiPath = 'MaintenanceLeadConsole/GetManualWorkOrders'
	url = URLPath + apiPath		
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData=data.json
	print "resultData Checking the available RM Orders",resultData
	myList = []
	for i in resultData:
		Status = i.get('Status')
		if str(Status).lower() != str('Completed').lower():
			machineName = i.get('Machine')
			tagPath = str(defaultPath)+str(machineName)+'/RepairAlarm.value'
			IsMaintenanceFlag = system.tag.read(str(tagPath)).value
			print 'IsMaintenanceFlag :',machineName,' :' ,IsMaintenanceFlag
			if IsMaintenanceFlag == False or IsMaintenanceFlag == 0:
				system.tag.write(tagPath,1)
			else:
				pass
		else:
			pass	



def ADDMaintenanceMachines():   
	#-Start->---This is used to add Maintenance Flag to the Machine if there is any already RM Order running.
	apiPath = 'MaintenanceLeadConsole/GetManualWorkOrders'
	url = URLPath + apiPath		
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
		resultData=data.json
	print "resultData Checking the available RM Orders",resultData
	myList = []
	for i in resultData:
		Status = i.get('Status')
		if str(Status).lower() != str('Completed').lower():
			machineName = i.get('Machine')
			tagPath = str(defaultPath)+str(machineName)+'/IsRMGenerated.value'
			IsMaintenanceFlag = system.tag.read(str(tagPath)).value
			print 'IsMaintenanceFlag :',machineName,' :' ,IsMaintenanceFlag 
			if IsMaintenanceFlag == False or IsMaintenanceFlag == 0:
				system.tag.write(tagPath,1)
			else:
				pass
		else:
			pass	
	#-END->---This is used to add Maintenance Flag to the Machine if there is any already RM Order running.
	
	#-Start-> This is used to check active workorders and add to the common dataset whihch will use to add RM / Alert
	Result = PackingAndLabelling.getActiveWorkOrderMachineList()
	print 'Active Workorders Result',Result
	for row in Result:
		machineName = row.get("MachineName")
		machineId = row.get("MachineId")
		WorkOrderNo = row.get('WorkOrderNo')
		LineId =  row.get('LineId')
		WorkflowOperationsId = row.get('WorkflowOperationsId')
		WorkflowId =  row.get('WorkflowId')
						
		tagPath = str(defaultPath)+str(machineName)
		repairValue = system.tag.read(str(tagPath)+'/Repair.value').value
		machineStatusTag = system.tag.read(str(tagPath)+'/MachineStatus.value').value
		IsMaintenanceFlag = system.tag.read(str(tagPath)+'/IsRMGenerated.value').value
		
		print "==============" + str(machineName)+ "==================="
		print "Repair tag Value: ",repairValue
		print "machineStatusTag tag Value: ",machineStatusTag
		print "IsMaintenanceFlag tag Value: ",IsMaintenanceFlag
		print "========================================================"
		Machinelist = []
		if ((IsMaintenanceFlag == False or IsMaintenanceFlag == 0)):
#			repairTagHistoryDS = system.tag.read(str(tagPath)+"/RepairHistory").value
			if repairValue == int(2) or machineStatusTag == int(5):
				tagPath = str(defaultPath)
				tableMaintenance = system.tag.read(str(tagPath)+"/MachinesForMaintenance").value
				
				if tableMaintenance.getRowCount()>0:
					MachineNAMES = tableMaintenance.getColumnAsList(0)
					if machineName not in MachineNAMES:
						print 'Is not present : ',machineName 
						newRow = [machineName,machineId,6,WorkOrderNo,LineId,WorkflowOperationsId,WorkflowId]
						updateRow = system.dataset.addRow(tableMaintenance, newRow)
						system.tag.write(str(tagPath)+"/MachinesForMaintenance",updateRow)
						print 'Added New Row',updateRow
					else:
						pass
				else:
					myList = [machineName,machineId,6,WorkOrderNo,LineId,WorkflowOperationsId,WorkflowId]
					Machinelist.append(myList)
					header = ["MachineName","MachineId","Value","WorkOrderNo","LineId","WorkflowOperationsId","WorkflowId"]	
					data = system.dataset.toDataSet(header,Machinelist)
					print "data",data
					tagPath = str(defaultPath)
					system.tag.write(str(tagPath)+"/MachinesForMaintenance",data)
					print "DS Binded Successfully",data
			else:
				pass
				
				
#-Start-> This is used to Create RM Order/ Breakdown alert from machine-->											
def BreakdownRMGeneration():
	#Harcoded PAramteter which is required for the RM Generation..
	reasonTypeId = 11
	reasonSubtypeId = 63
	reasoncodeId = 11388
	priorityId = 3
	userId = 1
	remarks = "Machine Generated RMOrder"
	
	scanBadgeText = "Machine"
	downtimeReasonId = 11388
	commentText = "Machine Generated Breakdown Alert"
	
	tagPath = str(defaultPath)
	tableMaint = system.tag.read(str(tagPath)+"/MachinesForMaintenance").value
	
	print 'Print 1 : Repair Machine Table: ', tableMaint  
	if tableMaint.getRowCount() >0:
		Machinelist = []
		for i in range(tableMaint.getRowCount()):
			machineName= tableMaint.getValueAt(i,"MachineName")
			machineId= tableMaint.getValueAt(i,"MachineId")
			value= tableMaint.getValueAt(i,"Value")
			newvalue = value-1
#			machineStatusTag = tableMaint.getValueAt(i,"machineStatusTag")
			WorkOrderNo = tableMaint.getValueAt(i,"WorkOrderNo")
			LineId = tableMaint.getValueAt(i,"LineId")
			WorkflowOperationsId = tableMaint.getValueAt(i,"WorkflowOperationsId")
			WorkflowId = tableMaint.getValueAt(i,"WorkflowId")
			
			myList = [machineName,machineId,newvalue,WorkOrderNo,LineId,WorkflowOperationsId,WorkflowId]
			Machinelist.append(myList)
			
		header = ["MachineName","MachineId","Value","WorkOrderNo","LineId","WorkflowOperationsId","WorkflowId"]	
		newData = system.dataset.toDataSet(header,Machinelist)
		tagPath = str(defaultPath)
		system.tag.write(str(tagPath)+"/MachinesForMaintenance",newData)
		
		tagPath = str(defaultPath)
		tableMaintenance = system.tag.read(str(tagPath)+"/MachinesForMaintenance").value
		print 'Print 2 : After Value Reduce Machine Table: ', tableMaintenance
		for i in range(tableMaintenance.getRowCount()):
			machineName= tableMaintenance.getValueAt(i,"MachineName")
			machineId= tableMaintenance.getValueAt(i,"MachineId")
			value= tableMaintenance.getValueAt(i,"Value")
			print 'value: '+str(value)
			print "machineName : ",machineName," :",value
			if value <= 0:
				tagPath = str(defaultPath)+str(machineName)
				repairValue = system.tag.read(str(tagPath)+'/Repair.value').value
				machineStatus = system.tag.read(str(tagPath)+'/MachineStatus.value').value  #will used to generate Breakdown Alert
				if repairValue == int(2):
					MakeModelId1=ProductionOperatorConsole.getMakeModelbyMachineId(machineId)
					MakeModelId =MakeModelId1[0]
					makeId=MakeModelId.get('MakeId')
					modelId=MakeModelId.get('ModelId')
					createRMOrder=ProductionOperatorConsole.createRMorder(machineId,makeId,modelId,reasonTypeId,reasonSubtypeId,reasoncodeId,priorityId,userId,remarks)
					print 'createRMOrder:'+str(createRMOrder)
					if createRMOrder == int(1):
						tagPath = str(defaultPath)
						tableMaintenance1 = system.tag.read(str(tagPath)+"/MachinesForMaintenance").value
						print 'print 3: Table for Repair:' ,tableMaintenance1
						for i in range(tableMaintenance1.getRowCount()):
							rowIndices = [i]
							newDS = system.dataset.deleteRows(tableMaintenance1,rowIndices)
							tagPath = str(defaultPath)
							system.tag.write(str(tagPath)+"/MachinesForMaintenance",newDS)
							system.tag.write(str(tagPath)+str(machineName)+"/IsRMGenerated.value",1)  #Added to avoid multiple generation of RM order
							print "RM Order Generated for :",machineName
							break
							pass
				
				elif machineStatus == int(5):
				 	WorkflowOperationsId = tableMaintenance.getValueAt(i,"WorkflowOperationsId")
				 	WoNumber = tableMaintenance.getValueAt(i,"WorkOrderNo")
				 	lineID = tableMaintenance.getValueAt(i,"LineId")
				 	WorkflowId = tableMaintenance.getValueAt(i,"WorkflowId")
				 	userID = 1
				 	
					saveResult = WorkOrderDetailsAPI.updateDowntimes(WorkflowOperationsId,WoNumber,scanBadgeText,downtimeReasonId,commentText,lineID,machineId,userID)			
					AddDowntime= WorkOrderDetailsAPI.AddDowntime(WorkflowOperationsId,WoNumber,WorkflowId,userID,machineId)
					tagPath = str(defaultPath)
					tableMaintenance1 = system.tag.read(str(tagPath)+"/MachinesForMaintenance").value
					print 'print 3: Table for Repair:' ,tableMaintenance1
					for i in range(tableMaintenance1.getRowCount()):
						rowIndices = [i]
						newDS = system.dataset.deleteRows(tableMaintenance1,rowIndices)
						tagPath = str(defaultPath)
						system.tag.write(str(tagPath)+"/MachinesForMaintenance",newDS)
						system.tag.write(str(tagPath)+str(machineName)+"/IsRMGenerated.value",1)  #Added to avoid multiple generation of RM order
						print "Breakdown Alert generated for :",machineName
						break
						pass
				else:
					tagPath = str(defaultPath)
					tableMaintenance1 = system.tag.read(str(tagPath)+"/MachinesForMaintenance").value
					rowIndices = [i]
					newDS = system.dataset.deleteRows(tableMaintenance1,rowIndices)
					tagPath = str(defaultPath)
					system.tag.write(str(tagPath)+"/MachinesForMaintenance",newDS)
	else:
		print 'No records'