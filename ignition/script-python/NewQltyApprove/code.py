import re
import json
import urllib2, urllib
import datetime
URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
defaultPath=system.tag.read("[default]JMES_InternalTags/DafaultTagPath").value

#---------------------------------------------Quality Scrap History----------------------------------------------------------
def getLotToQltyApprove(WorkorderNo,workorderId):	
	try:
		apiPath="OperatorConsole/GetproducedConatinerCountRemaningContainerCountBasedOnWorkorder?WorkOrderNo="+str(WorkorderNo)+("&WorkorderId=")+str(workorderId)	
		url = URLPath + apiPath
		try:
			system.perspective.print("API URL is: "+str(url))
#			system.perspective.print("API InputData is: "+str(jsonParams))
			system.perspective.print("API Method is: Get ")
		except:
			pass
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  APIResult=data.json
		  	
		QualityScrapHistory=[]
		Id=0	
		print("API Resul---->"+str(APIResult))
		for i in (APIResult):
			Id=Id+1
			LotNo=i.get("LotNo")
			ProductionQty=i.get("ProductionCount")
			ProducedContainer=i.get("ProducedContainer")
			RemainingContainer=i.get("RemaningContainer")
			NoofContainerstoApprove=0
			SacrapByFG=0.00000
			Approve=""

			DataList=[Id,LotNo,ProductionQty,ProducedContainer,RemainingContainer,NoofContainerstoApprove,SacrapByFG,Approve]
			QualityScrapHistory.append(DataList)
			
		print 'API Result:-->' +str(QualityScrapHistory)
		header=["Id","LotNo","ProductionQty","ProducedContainer","RemainingContainer","NoofContainerstoApprove","ScrapByFG","Approve"]
		Result = system.dataset.toDataSet(header,QualityScrapHistory)		
		return Result
	except Exception as e:
		print("print error "+str(e))
		return 0

#------------------------------Save Quality Scrap Reports----------------------------------------------
def ApproveContainerFromQlty(ContainerDetails):
	try:
#		apiPath = "OperatorConsole/AddUpdateQAScrapDetails"
		apiPath="OperatorConsole/UpdateProductionOperatorConsoleLotWiseContainers"
		url = URLPath + apiPath
		print url	
		writeData=	{
					  "cDetails":ContainerDetails
					}					
						
		jsonParams = system.util.jsonEncode(writeData)
#		system.perspective.print("Quality Json" +str(jsonParams))	
		try:
			system.perspective.print("API URL is: "+str(url))
			system.perspective.print("API InputData is: "+str(jsonParams))
			system.perspective.print("API Method is: Post ")
		except:
			pass	
		createdeffect = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
		except:
			createdeffect = 0
		return createdeffect
	except:			
		return 0
		

#------------------------------Save Quality Scrap Reports----------------------------------------------
def ScrapByFG(WorkorderNo,WorkorderId,LineId,ScrapByFG,LotNo):
	try:
		apiPath = "OperatorConsole/AddUpdateQualityScrapByFG"
		url = URLPath + apiPath
		print url	
		writeData=	{
						"workOrderNo": WorkorderNo,
						"workorderID": WorkorderId,
						"lineID": LineId,
						"scrapByFG":ScrapByFG,
						"lotNumber":LotNo					 
					}					
						
		jsonParams = system.util.jsonEncode(writeData)
		try:
			system.perspective.print("API URL is: "+str(url))
			system.perspective.print("API InputData is: "+str(jsonParams))
			system.perspective.print("API Method is: Post ")
		except:
			pass	
		createdeffect = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
			postReturn=system.util.jsonDecode(postReturn)
		except:
			postReturn = []
		return postReturn
	except Exception as e:
		print("print error "+str(e))
		return []
		
#---------------------------------------------Line Lead Main Landing page----------------------------------------------------------

#---------------------------------------------Line Lead Main Landing page----------------------------------------------------------
def getLotLineLeadMainlandingPage(enterpriseId,plantId,areaId,lineId,userId):
	try:
		apiPath = "OperatorConsole/GetWorkordersWhoseAtLeastOnContainerApprovedByQuality?enterpriseID="+str(enterpriseId)+"&plantID="+str(plantId)+"&areaID="+str(areaId)+"&lineID="+str(lineId)+"&userID="+str(userId)
		url = URLPath + apiPath
		try:
			system.perspective.print("API URL is: "+str(url))
#			system.perspective.print("API InputData is: "+str(jsonParams))
			system.perspective.print("API Method is: Get ")
		except:
			pass
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  APIResult=data.json
		  	
		LineLeadDetails=[]
		Id=0	
		print("API Resul---->"+str(APIResult))
		for i in (APIResult):
			Id=Id+1
			WorkOrderNo=i.get("WorkOrderNo")
			LotNo=i.get("LotNo")
			Name=i.get("Name")
			PartNumber=i.get("PartNumber")
			ProductionQty=i.get("ProductionQty")
			NoOfApprovedContainerFromQuality=i.get("NoOfApprovedContainerFromQuality")
			ContainerQuantity=i.get("ContainerQuantity")
			LineId=i.get("LineId")
			ReportBF=i.get("ReportBF")
			WorkorderId=i.get("WorkorderId")
			ViewDetails=''
			lineName = i.get("LineName")
			AreaId = i.get("AreaId")
			PlantId = i.get("PlantId")
			EnterpriseId = i.get("EnterpriseId")


			DataList=[Id,WorkOrderNo,lineName,Name,LotNo,PartNumber,ProductionQty,NoOfApprovedContainerFromQuality,ContainerQuantity,ViewDetails,LineId,ReportBF,WorkorderId,AreaId,PlantId,EnterpriseId]
			LineLeadDetails.append(DataList)
			
		print 'API Result:-->' +str(LineLeadDetails)
		header=["Id","WorkOrderNo","LineName","Status","LotNo","PartNumber","ProductionQty","NoOfApprovedContainerFromQuality","ContainerQuantity","ViewDetails","LineId","ReportBF","WorkorderId","AreaId","PlantId","EnterpriseId"]
		Result = system.dataset.toDataSet(header,LineLeadDetails)		
		return Result
	except Exception as e:
		print("print error "+str(e))
		return 0
		
#---------------------------------------------Production Scrap History----------------------------------------------------------
def getLineLeasdScrapHistory(screenNo,WorkorderId,partNo,factory,revision,partNoWithoutFactory,LineId,UserId,ScrapByFG,LotNo):
	try:	
#		apiPath="OperatorConsole/GetScrapDetailsForProductionPEAQA?WHICHSCREEN="+str(screenNo)+("&WorkOrderNo=")+str(WorkorderId)+str("&partNo=")+str(partNo)+str("&Factory=")+str(factory)+str("&Revision=")+str(revision)+str("&PartNoWithoutDetails=")+str(partNoWithoutFactory)+str("&LineID=")+str(LineId)+str("&UserID=")+str(UserId)+str("&LotNumber=")+str(LotNo)		
		apiPath="OperatorConsole/GetScrapDetailsForProductionPEAQA?WHICHSCREEN="+str(screenNo)+"&WorkOrderId="+str(WorkorderId)+"&partNo="+str(partNo)+"&Factory="+str(factory)+"&Revision="+str(revision)+"&PartNoWithoutDetails="+str(partNoWithoutFactory)+"&LineID="+str(LineId)+"&UserID="+str(UserId)+"&LotNumber="+str(LotNo)
#		apiPath="OperatorConsole/GetScrapDetailsForProductionPEAQA?WHICHSCREEN="+str(4&WorkOrderId=410821&partNo=1102-1020143_C_JCL&Factory=JCL&Revision=C&PartNoWithoutDetails=1102-1020143&LineID=6&UserID=64
		
		url = URLPath + apiPath
		ScrapByFG1=float(ScrapByFG)
		try:
			system.perspective.print("API URL is: "+str(url))
#			system.perspective.print("API InputData is: "+str(jsonParams))
			system.perspective.print("API Method is: Get ")
		except:
			pass
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
#		print('API Result:-->' +str(data))
		if data.good:    
		  APIResult=data.json
#		  print('API Result:-->' +str(APIResult))
	#	  APIResult=[{'WONo':'12976156','WOQty':432,'PartNo':'1339-10E0023','Revision':'A','WOCompletion':0,'WoStatus':'Not-Started','WorkFlow':'P_AA_2022-1020456EP_B_CNS','WorkFlowId':97,'WorkFlowOperation':'Molding','WorkFlowOperationId':97,'StartDate':'2021-03-27T23:22:00','EndDate':'2021-03-29T23:22:00','ActualStartDate':'2021-03-27T23:22:00','ActualEndDate':'2021-03-29T23:22:00','UOM':'EA','EntName':'JohnsonElectric','EntID':0,'PlantName':'Jiangmen','PlantId':0,'AreaName':'CNS','AreaId':6,'LineName':'AA','LineId':8,'CycleTime':2,'shift':'Shift-A'}]
		print"ResultData",(APIResult)	
		system.perspective.print('APIResult :' + str(APIResult))
		ProdScrapHistory=[]
		Id=0		
		for i in (APIResult):
			Id=Id+1
			BomName=i.get('BomName')			
			Revision=i.get('Revision')
			Description=i.get('Description')	
			UOM=i.get('UOM')
			UnitUsage=i.get('UnitUsage')
			ScrapByUnit=i.get('ScrapByUnit')
			ScrapByUnit=0.00
			ScrapByFG=i.get('ScrapByFG')
#			ScrapByFG=float(ScrapByFG1*UnitUsage)f
			TotalConsumption=i.get('TotalConsumption')
			TotalScrap=i.get('TotalScrap')
			LineLeadTotalScrap=i.get('LineLeadTotalScrap')
			ProductionScrap=i.get('ProductionScrap')
			QualityScrap=i.get('QualityScrap')	
			LotNumber=i.get('LotNumber')
			Vendorlot=i.get('Vendorlot')
			BomDetailsId=i.get('BomDetailsId')
			MstItemId=i.get('MstItemId')
			BomID=i.get('BomID')
			LineID=i.get('LineID')		
			MachineID=i.get('MachineID')
			BobbinsId=i.get('BobbinsId')
			HeadName=i.get('HeadName')
			EquipmentCode=i.get('EquipmentCode')
			OperationName=i.get('OperationName')
			RemainingQty=i.get('RemainLotQuantity')
			IsMaterialRequest = i.get("IsMaterialRequested")
			LLContainerWiseConsumtion = i.get("LLContainerWiseConsumtion")
			LLContainerWiseConsumtion=float(LLContainerWiseConsumtion)
			LineLeadScrapByFGCurrent = i.get("LineLeadScrapByFGCurrent")
			LineLeadScrapByFGCurrent=str(LineLeadScrapByFGCurrent)
			PEAScrap = i.get("PEAScrap")
			LabelType = i.get('LabelType')
			
			if 	str(LabelType) == str('1'):
				LabelType = 'LO'
			else:
				LabelType = 'EO'
				
			
			
			DataList=(Id,BomName,Revision,Description,UOM,UnitUsage,ScrapByUnit,ScrapByFG,TotalConsumption,TotalScrap,LineLeadTotalScrap,ProductionScrap,QualityScrap,LotNumber,Vendorlot,BomDetailsId,MstItemId,BomID,LineID,MachineID,BobbinsId,HeadName,EquipmentCode,OperationName,RemainingQty,IsMaterialRequest,LLContainerWiseConsumtion,LineLeadScrapByFGCurrent,PEAScrap,LabelType)
			ProdScrapHistory.append(DataList)			
		print('API Result:-->' +str(ProdScrapHistory))
		header=['Sr No','BOM Name','Revision','Description','UOM','UnitUsage','ScrapByUnit', 'ScrapByFG','TotalConsumption','TotalScrap','LineLeadTotalScrap','ProductionScrap','QualityScrap','JE Lot','Vendor Lot','BomDetailsId','MstItemId','BomID','LineID','MachineID','BobbinsId','HeadName','EquipmentCode','OperationName','RemainingQty','IsMaterialRequest','LLContainerWiseConsumtion','LineLeadScrapByFGCurrent','PEAScrap','LabelType']
		Result = system.dataset.toDataSet(header,ProdScrapHistory)		
		return Result
	except Exception as e:
		system.perspective.print("print error "+str(e))
		return 0
		
#------------------------------Save Line Lead Scrap By FG Reports----------------------------------------------
def LineLeadScrapByFG(WorkorderNo,WorkorderId,LineId,ScrapByFG,MESLotNo):
	try:
		apiPath = "OperatorConsole/AddUpdateLineLeadScrapByFG"
		url = URLPath + apiPath
		print url	
		writeData=	{
					  "workOrderNo": WorkorderNo,
					  "workorderID": WorkorderId,
					  "lineID": LineId,
					  "scrapByFG":ScrapByFG,
					  "lotNumber":MESLotNo
					}									
		jsonParams = system.util.jsonEncode(writeData)
		try:
			system.perspective.print("API URL is: "+str(url))
			system.perspective.print("API InputData is: "+str(jsonParams))
			system.perspective.print("API Method is: Post ")
		except:
			pass		
		createdeffect = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
			print postReturn
			postReturn=system.util.jsonDecode(postReturn)
		except Exception as k:
			print("print error "+str(k))
			postReturn=[]
		return postReturn
	except Exception as e:
		print("print error "+str(e))
		return 0
		
#------------------------------Save Line Lead Individual Scrap Reports----------------------------------------------
def LineLeadScrapByComponent(WorkorderNo,PartNo,LineId,componentDetails,userId,WorkorderId):
	try:
		apiPath = "OperatorConsole/AddUpdateLineLeadScrapDetails"
		url = URLPath + apiPath
		print url	
		writeData={
					  "workOrderNo":WorkorderNo,
					  "workorderId": WorkorderId,
					  "lineID": LineId,
					  "woPartNo": PartNo,
					  "lineLeadBomDetails":componentDetails,
					  "scrapCreatedBy":userId
					}					
		jsonParams = system.util.jsonEncode(writeData)
		try:
			system.perspective.print("API URL is: "+str(url))
			system.perspective.print("API InputData is: "+str(jsonParams))
			system.perspective.print("API Method is: Post ")
		except:
			pass		
		createdeffect = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)
		except:
			createdeffect = 0
		return createdeffect
	except Exception as e:
		system.perspective.print("print error "+str(e))
		return 0
 


def updateLLConsumption(WorkorderNo,WorkorderId,LineId,NoOfCotainers,LotNo):
	try:
		apiPath ="OperatorConsole/AddUpdateLineLeadTotalConsumptionDetails?Workorder="+str(WorkorderNo)+("&WorkorderId=")+str(WorkorderId)+("&Lineid=")+str(LineId)+("&NoOfContainerToApproved=")+str(NoOfCotainers)+str("&LotNo=")+str(LotNo)	
		url = URLPath + apiPath	
		try:
			system.perspective.print("API URL is: "+str(url))
#			system.perspective.print("API InputData is: "+str(jsonParams))
			system.perspective.print("API Method is: Get ")
		except:
			pass
		result = 1	
		try: 
			postReturn = system.net.httpPost(url,'application/json')
			print 'postReturn',postReturn
		except:		
			result = 0
			pass
		try:
			resultData= system.util.jsonDecode(postReturn)
		except:
			resultData = []
			pass

		return resultData
	except:
		import sys, os
		exc_type, exc_obj,tb = sys.exc_info()
		lineno = tb.tb_lineno
		errorMessage = "'Exception ::NEQQLTYApprove :"+ str(exc_obj) + "Code Line No: "+ str(lineno)
		system.perspective.print(errorMessage+' || Line No :' + str(lineno))


#------------------------------------------------------------Backflush To ERP-------------------------------------------
def BackFlushToErp(workorderNo,LotNo,PartNo,UserId,LineId,NoOfContainers,WorkorderId):
#	apiPath="OperatorConsole/FlustLotDetailsToERP?Workorder="+str(workorderNo)+("&LotNumber=")+str(LotNo)+("&Partno=")+str(PartNo)+("&UserId=")+str(UserId)+("&LineId=")+str(LineId)+("&Numberofcontainertobackflush=")+str(NoOfContainers)	
#	apiPath="OperatorConsole/FlustLotDetailsToERP?Workorder="+str(workorderNo)+("&LotNumber=")+str(LotNo)+"&Partno="+str(PartNo)+("&UserId=")+str(UserId)+("&LineId=")+str(LineId)+("&Numberofcontainertobackflush=")+str(NoOfContainers)+("&WorkorderId=")+str(WorkorderId)
	apiPath='OperatorConsole/FlustLotDetailsToERP?LotNumber='+str(LotNo)+'&Partno='+str(PartNo)+'&UserId='+str(UserId)+'&LineId='+str(LineId)+'&Numberofcontainertobackflush='+str(NoOfContainers)+'&WorkorderId='+str(WorkorderId)
	url = URLPath + apiPath	
	try:
		system.perspective.print("BF API URL is: "+str(url))
#		system.perspective.print("API InputData is: "+str(jsonParams))
		system.perspective.print("API Method is: Get ")
	except:
		pass
	result = 1
	try:
		postReturn1 = system.net.httpPost(url,'application/json')
		postReturn1 = system.util.jsonDecode(postReturn1)
		print("BackFlush PostREes : "+str(postReturn1))
		for i in(postReturn1):
			postReturn =i.get('Result')
			if 	postReturn==2:
				result = 1    #-----Validation Popup "Consumption is More Than Remaining Qty." 
				print "Open Validation"
			elif postReturn==1:
				result=1	#------BackFlushed Successfully------------------
			else:
				result=0	#-------Fail To Back Flush------------
	except Exception as e:
		print("print error "+str(e))
		result=0
		pass
	return result 


	