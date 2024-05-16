def getSubstitueComponentDetails(WoNumber,workflowId,operation,process):
	try:
		apiPath = "OperatorConsole/GetAttachedWorkFlowProcessComponentsWithSubstituteForOperatorConsole"
		url = URLPath + apiPath
		
		params = {
		  "workOrderNo":WoNumber,
		  "workflowId": workflowId,
		  "workflowOperationId": operation,
		  "workflowProcessId": process,
		  "headerName": "ADD PARTS TO BE consumed"
			}
		
		jsonParams = system.util.jsonEncode(params)			 
		result = 1
		try:
			postReturn = system.net.httpPost(url,'application/json',jsonParams)			
		except:		
			result = 0
			postReturn = ''
			pass
		try:
			resultData= system.util.jsonDecode(postReturn)		
		except:
			resultData = []				
		k=1
		dataList = []
		print str(resultData)
		for i in resultData:
			partNumber = i.get("PartNo")
			if str(partNumber).lower()!=str(None).lower() :
				SrNo = k
				ID = i.get("SelectedId")
				revision = i.get("Revision")
				componentName = i.get("PartWithRevision")   # str(partNumber)+"_"+str(revision)
				uom = i.get("UOMName")
				isSubstituteAvailableFlag = i.get("isSubstituteAvailable")
				SubstituteIdentification = i.get("SubstituteIdentification")		
				SubstituteItemId = i.get("SubstituteItemId")
				SubstituteItemPartNo = i.get("SubstituteItemPartNoWithRevision")	
				lotNo = i.get("LotNo")
				serialNo = 0					
				consumeQty = i.get("ConsumedQty")
				ComponentExpiryDate = i.get("ComponentExpiryDate")
				ERPTransferLot = MaterialRequestAPI.isNotBlank(i.get('TransferLot'))
				ERPTransferQty = MaterialRequestAPI.isNotBlank(i.get('TransferQty'))
				ERPFactoryName = MaterialRequestAPI.isNotBlank(i.get('FactoryName'))
				ERPVendorName = MaterialRequestAPI.isNotBlank(i.get('VendorName'))
				ERPExpirationDate=MaterialRequestAPI.isNotBlank(i.get('ExpirationDate'))
				ERPVendorCode = ''
				if str(ERPTransferQty) == "":
					ERPTransferQty = 'Qty Not Transfered'
				else:
					pass
				today = system.date.now()
				TodayDate= system.date.format(today, "dd/MM/yyyy,HH:mm:ss")
				ComponentExpiryDateDefault = "01/01/1900,00:00:00"
				
#				if ComponentExpiryDate >= TodayDate or ComponentExpiryDate == None or ComponentExpiryDateDefault == ComponentExpiryDate:
#					IsExpired = 0
#					print "Not Expired--->"
#				else:
#					IsExpired = 1
#					print "Expired-------> "
				print 'ERPExpirationDate',ERPExpirationDate
				if ERPExpirationDate >= TodayDate or ERPExpirationDate == None or str(ERPExpirationDate).strip().lower() == str("None").strip().lower():
					IsExpired = 0
					print "Not Expired--->"
				else:
					IsExpired = 1
					print "Expired-------> "

				myList = [SrNo,ID,componentName,uom,isSubstituteAvailableFlag,SubstituteIdentification,SubstituteItemId,SubstituteItemPartNo,serialNo,lotNo,consumeQty,IsExpired,ERPTransferLot,ERPTransferQty,ERPFactoryName,ERPVendorName,ERPExpirationDate,ERPVendorCode] 		
				dataList.append(myList)
				k = k+1
			else:
				print 'No Record'
		headers = ["SrNo","Id","Parameter","uom","isSubstituteAvailableFlag","SubstituteIdentification","SubstituteItemId","SubstituteItemPartNo","SerialNumber","LotNumber","ConsumeQty","IsExpired","ERPTransferLot","ERPTransferQty","ERPFactoryName","ERPVendorName","ERPExpirationDate","ERPVendorCode"]
		resultDetails = system.dataset.toDataSet(headers,dataList)	
		return resultDetails
	except:
		exc_type, exc_obj,tb = sys.exc_info()
		errorMessage = "Error:"+ str(exc_obj)
		lineno = tb.tb_lineno
		print 'errorMessage:', errorMessage
		print 'LineNo', lineno