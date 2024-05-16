import smtplib	
import system
import re
import json
import urllib2, urllib

URLPath = system.tag.read("[default]JMES_InternalTags/urlAPI_zag").value
#URLPath = system.tag.read("[default]JMES_InternalTags/urlSITAPI").value

def sendMail(LineName,operationId,WoNumber,senderUserName,loggedUserId,reasonName,comments,emailId):	
	import smtplib	
	import system
	import re

	lineName = str(LineName)
	operationId = str(operationId)
	WoNumber = str(WoNumber)
	senderUsername = str(senderUserName)
	loggedUserId =str(loggedUserId)
	reasonSelected = str(reasonName)
	commentEntered = comments

	receiverEmailId = str(emailId)
	receiverEmailId = receiverEmailId.strip()
	system.perspective.print('Sent Email to : ' + str(receiverEmailId))
	try:	
		scriptName=' Email Function Send Mail'	
		smtpval = system.tag.read("[default]JMES_InternalTags/Send_Email/SMTP.value").value
		smtp = smtpval.strip()
		senderEmailId = system.tag.read("[default]JMES_InternalTags/Send_Email/Sender_SMPT.value").value
		senderEmailId = senderEmailId.strip()
		subject = "Work-Order Operator Console Alerts"
			
		emailBody = """<html  style="font-family:verdana;font-size:11px">
											<body>
											<table border="0" cellspacing="0" cellpadding="0" width="100%" style="width: 100.0%;
												mso-cellspacing: 0in; mso-padding-alt: 0in 0in 0in 0in">
														<tr style="mso-yfti-irow: 0; mso-yfti-firstrow: yes; height: 37.5pt">
															<td width="78%" style="width: 78.74%; background: #FFA500; padding: 0in 0in 0in 15.0pt;
																height: 37.5pt">
																<p style="mso-margin-top-alt: auto; mso-margin-bottom-alt: auto">
																	<span style="font-size: 16.5pt; font-family: Verdana; color: white; letter-spacing: 1.5pt">
																	 JEMES Operator Console Alerts </span><o:p></o:p></p>
															</td>
															<td width="21%" valign="bottom" style="width: 21.26%; background: #FFA500; padding: 0in 7.5pt 3.75pt 0in;
																height: 37.5pt; -moz-background-clip: initial; -moz-background-origin: initial;
																-moz-background-inline-policy: initial; background-position-x: 0%; background-position-y: 50%">
																<p class="MsoNormal" align="right" style="mso-margin-top-alt: auto; mso-margin-bottom-alt: auto;
																	text-align: right">
																	<b><span style="font-size: 9.0pt; font-family: Verdana; color: white; letter-spacing: 1.5pt">
																		</span></b><o:p></o:p></p>
															</td>
														</tr>
														<tr style="mso-yfti-irow: 1; height: 15.0pt">
															<td colspan="2" style="border-top: solid #444444 1.5pt; border-left: none; border-bottom: solid windowtext 1.0pt;
																border-right: none; background: #FFFACD; padding: 0in 0in 0in 15.0pt; height: 15.0pt;
																-moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;
																background-position-x: 0%; background-position-y: 50%">
														
															</td>
														</tr>
														<tr style="mso-yfti-irow: 2; mso-yfti-lastrow: yes">
															<td width="100%" colspan="2" style="width: 100.0%; padding: 15.0pt 0in 0in 15.0pt">
													</table>
								
													<table border = "1" cellspacing="0" cellpadding="0" width="100%" style="width: 100.0%;
																				mso-cellspacing: 0in; mso-padding-alt: 0in 0in 0in 0in">
													<tr style="font-family:verdana;font-size:11px">
														<td bgcolor="#fff6e6" style="font-family:verdana;font-size:12px : font-weight: bold :font-weight: 900"  > SrNo </td>
														<td bgcolor="#fff6e6" style="font-family:verdana;font-size:10px : font-weight: bold :font-weight: 900">Line Name </td>
														

														
														<td bgcolor="#fff6e6" style="font-family:verdana;font-size:10px : font-weight: bold :font-weight: 900"> Workorder Number </td> 
														
														<td bgcolor="#fff6e6" style="font-family:verdana;font-size:10px : font-weight: bold :font-weight: 900"> Raised By  </td> 
														
														<td bgcolor="#fff6e0" style="font-family:verdana;font-size:10px : font-weight: bold :font-weight: 900"> Logged By </td> 
														
														<td bgcolor="#fff6e6" style="font-family:verdana;font-size:10px : font-weight: bold :font-weight: 900"> Reason  </td> 
														
		        										<td bgcolor="#fff6e6" style="font-family:verdana;font-size:10px : font-weight: bold :font-weight: 900"> Comment </td> 
														
													</tr>
													<tr style="font-family:verdana;font-size:11px; height:90px">
														
															<td bgcolor="#FFFFFF" style="font-family:verdana;font-size:10px; word-break:break-all;"> 1 </td>
														
															<td bgcolor="#FFFFFF" style="font-family:verdana;font-size:10px; word-break:break-all;"> """+lineName+""" </td>
														

															
															<td bgcolor="#FFFFFF" style="font-family:verdana;font-size:10px; word-break:break-all;"> """+WoNumber+""" </td>
															
															<td bgcolor="#FFFFFF" style="font-family:verdana;font-size:10px; word-break:break-all;"> """+senderUsername+""" </td>
														
															<td bgcolor="#FFFFFF" style="font-family:verdana;font-size:10px; word-break:break-all;"> """+senderUsername+""" </td>
															
															<td bgcolor="#FFFFFF" style="font-family:verdana;font-size:10px; word-break:break-all;"> """+reasonSelected+""" </td>
														
		        											<td bgcolor="#FFFFFF" style="font-family:verdana;font-size:10px; word-break:break-all;"> """+commentEntered+""" </td>
		        											
														
														</tr>
																
												</table>
												</br>
												</br>
												</br>
												</br>
												</br>
												</br>
												</br>
												</br>
												 <b>Note:</b>
												Please Visit <a href="https://www.johnsonelectric.com/">https://www.johnsonelectric.com/</a> for more details.</br>
												</br>
												</br>
												
												<span style="font-family:verdana;font-size:11px">(Please do not reply to this mail as it is auto generated) </span></body></html>"""

		system.net.sendEmail(smtp,senderEmailId,subject,emailBody,1,receiverEmailId)
		print("Send SuccessFully")

	except:	
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)

def getEmailIdDetails(UserId):
	apiPath = "User/GetUser/" +str(UserId)
	url = URLPath + apiPath
	
#	request = urllib2.Request(url)
#	response=urllib2.urlopen(request)
#	data = system.net.httpGet(url)
#	resultData= system.util.jsonDecode(data)
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	return resultData

def getReasonCodeName(reasonId):
	apiPath = "ReasonCode/GetReasonCode/" +str(reasonId)				
	url = URLPath + apiPath
	
#	request = urllib2.Request(url)
#	response=urllib2.urlopen(request)
#	data = system.net.httpGet(url)
#	resultData= system.util.jsonDecode(data)
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  resultData=data.json
	return resultData
	
	
# ----------------------------Get The Wo List-----------------------------------------------------------
def getWOlistForMail(entId,plantId,areaId,lineId,userId):	
	apiPath='OperatorConsole/GetOperatorConsoleWorkOrdersDetails?EnterpriseId='+str(entId)+'&PlantId='+str(plantId) + '&AreaId='+str(areaId)+'&LineId='+str(lineId)+'&MachineId='+str(0)+'&UserId='+str(userId)
	url = URLPath + apiPath
#	print url
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  APIResult=data.json
#	print"ResultData",(APIResult)	
	WODetailList=[]
	Id=0
	for i in (APIResult):
		Id=Id+1
		WoStatus=i.get('WoStatus')
		if WoStatus=='In-Progress':
			WONo=i.get('WONo')
			WorkorderID=i.get('WorkOrderId')				
			WorkFlowId=i.get('WorkFlowId')
			WorkFlowOperation=i.get('WorkFlowOperation')
			WorkFlowOperationId=i.get('WorkFlowOperationId')
			LineName=i.get('LineName')
			LineId=i.get('LineId')
			WOType=i.get('WorkOrderType')
			parameters={"WONo":WONo,"WorkorderID":WorkorderID,"WorkFlowOperation":WorkFlowOperation,"WorkFlowOperationId":WorkFlowOperationId,"LineName":LineName,"LineId":LineId,"WOType":WOType}			
			WODetailList.append(parameters)
		else:
			pass
	return	WODetailList
# ----------------------------Get The Wo List-----------------------------------------------------------
def getmachineListagainstWo(Wono,WoId):	
	apiPath="OperatorConsole/GetMachineDetailsBasedOnWorkorderForOperatorConsole?Workorder="+str(Wono)+("&Workorderid=")+str(WoId)
	url = URLPath + apiPath
#	print url
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	APIResult=[]
	if data.good:    
	  APIResult=data.json
	print"ResultData",(APIResult)	
	MachineList=[]
	Id=0
	for i in (APIResult):
		Id=Id+1
		WorkOrder=i.get('WorkOrder')
		
		MachineName=i.get('MachineName')
	
		MachineStatusId=i.get('MachineStatusId')
		MachineStatus=i.get('MachineStatus')		
		parameters={"WorkOrder":WorkOrder,"MachineName":MachineName,"MachineStatusId":MachineStatusId,"MachineStatus":MachineStatus}			
		MachineList.append(parameters)
		
	return	MachineList	
#-------------------------------------------Sent Machine Disconneted Mail---------------------------
def MachineDisconnectsendMail(machineName,LineName,operationId,WoNumber,senderUserName,loggedUserId,reasonName,comments,emailId):	
	import smtplib	
	import system
	import re	
	lineName = str(LineName)
	operationId = str(operationId)
	WoNumber = str(WoNumber)
	senderUsername = str(senderUserName)
	loggedUserId =str(loggedUserId)
	reasonSelected = str(reasonName)
	commentEntered = comments
	receiverEmailId = str(emailId)
	receiverEmailId = receiverEmailId.strip()
	
	try:	
		scriptName=' Email Function Send Mail'	
		smtpval = system.tag.read("[default]JMES_InternalTags/Send_Email/SMTP.value").value
		smtp = smtpval.strip()
		senderEmailId = system.tag.read("[default]JMES_InternalTags/Send_Email/Sender_SMPT.value").value
		senderEmailId = senderEmailId.strip()
		subject = "Machine Disconnect Alerts"
			
		emailBody = """<html  style="font-family:verdana;font-size:11px">
													<body>
													<table border="0" cellspacing="0" cellpadding="0" width="100%" style="width: 100.0%;
														mso-cellspacing: 0in; mso-padding-alt: 0in 0in 0in 0in">
																<tr style="mso-yfti-irow: 0; mso-yfti-firstrow: yes; height: 37.5pt">
																	<td width="78%" style="width: 78.74%; background: #FFA500; padding: 0in 0in 0in 15.0pt;
																		height: 37.5pt">
																		<p style="mso-margin-top-alt: auto; mso-margin-bottom-alt: auto">
																			<span style="font-size: 16.5pt; font-family: Verdana; color: white; letter-spacing: 1.5pt">
																			 JEMES Production Operator Console Alerts </span><o:p></o:p></p>
																	</td>
																	<td width="21%" valign="bottom" style="width: 21.26%; background: #FFA500; padding: 0in 7.5pt 3.75pt 0in;
																		height: 37.5pt; -moz-background-clip: initial; -moz-background-origin: initial;
																		-moz-background-inline-policy: initial; background-position-x: 0%; background-position-y: 50%">
																		<p class="MsoNormal" align="right" style="mso-margin-top-alt: auto; mso-margin-bottom-alt: auto;
																			text-align: right">
																			<b><span style="font-size: 9.0pt; font-family: Verdana; color: white; letter-spacing: 1.5pt">
																				</span></b><o:p></o:p></p>
																	</td>
																</tr>
																<tr style="mso-yfti-irow: 1; height: 15.0pt">
																	<td colspan="2" style="border-top: solid #444444 1.5pt; border-left: none; border-bottom: solid windowtext 1.0pt;
																		border-right: none; background: #FFFACD; padding: 0in 0in 0in 15.0pt; height: 15.0pt;
																		-moz-background-clip: initial; -moz-background-origin: initial; -moz-background-inline-policy: initial;
																		background-position-x: 0%; background-position-y: 50%">
																
																	</td>
																</tr>
																<tr style="mso-yfti-irow: 2; mso-yfti-lastrow: yes">
																	<td width="100%" colspan="2" style="width: 100.0%; padding: 15.0pt 0in 0in 15.0pt">
															</table>
										
															<table border = "1" cellspacing="0" cellpadding="0" width="100%" style="width: 100.0%;
																						mso-cellspacing: 0in; mso-padding-alt: 0in 0in 0in 0in">
															<tr style="font-family:verdana;font-size:11px">
																<td bgcolor="#fff6e6" style="font-family:verdana;font-size:12px : font-weight: bold :font-weight: 900"  > SrNo </td>
																<td bgcolor="#fff6e6" style="font-family:verdana;font-size:10px : font-weight: bold :font-weight: 900">Machine Name </td>
																<td bgcolor="#fff6e6" style="font-family:verdana;font-size:10px : font-weight: bold :font-weight: 900">Line Name </td>
																
																<td bgcolor="#fff6e6" style="font-family:verdana;font-size:10px : font-weight: bold :font-weight: 900"> Operation Selected </td>
																
																<td bgcolor="#fff6e6" style="font-family:verdana;font-size:10px : font-weight: bold :font-weight: 900"> Workorder Number </td> 
																
																<td bgcolor="#fff6e6" style="font-family:verdana;font-size:10px : font-weight: bold :font-weight: 900"> Raised By  </td> 
																
																<td bgcolor="#fff6e0" style="font-family:verdana;font-size:10px : font-weight: bold :font-weight: 900"> Logged Id </td> 
																
																<td bgcolor="#fff6e6" style="font-family:verdana;font-size:10px : font-weight: bold :font-weight: 900"> Reason  </td> 
																
				        										<td bgcolor="#fff6e6" style="font-family:verdana;font-size:10px : font-weight: bold :font-weight: 900"> Comment </td> 
																
															</tr>
															<tr style="font-family:verdana;font-size:11px; height:90px">
																
																	<td bgcolor="#FFFFFF" style="font-family:verdana;font-size:10px; word-break:break-all;"> 1 </td>
																	
																	<td bgcolor="#FFFFFF" style="font-family:verdana;font-size:10px; word-break:break-all;"> """+machineName+""" </td>
																
																	<td bgcolor="#FFFFFF" style="font-family:verdana;font-size:10px; word-break:break-all;"> """+lineName+""" </td>
																
																	<td bgcolor="#FFFFFF" style="font-family:verdana;font-size:10px; word-break:break-all;"> """+operationId+""" </td>
																	
																	<td bgcolor="#FFFFFF" style="font-family:verdana;font-size:10px; word-break:break-all;"> """+WoNumber+""" </td>
																	
																	<td bgcolor="#FFFFFF" style="font-family:verdana;font-size:10px; word-break:break-all;"> """+senderUsername+""" </td>
																
																	<td bgcolor="#FFFFFF" style="font-family:verdana;font-size:10px; word-break:break-all;"> """+loggedUserId+""" </td>
																	
																	<td bgcolor="#FFFFFF" style="font-family:verdana;font-size:10px; word-break:break-all;"> """+reasonSelected+""" </td>
																
				        											<td bgcolor="#FFFFFF" style="font-family:verdana;font-size:10px; word-break:break-all;"> """+commentEntered+""" </td>
				        											
																
																</tr>
																
														</table>
														</br>
														</br>
														</br>
														</br>
														</br>
														</br>
														</br>
														</br>
														 <b>Note:</b>
														Please Visit <a href="https://www.johnsonelectric.com/">https://www.johnsonelectric.com/</a> for more details.</br>
														</br>
														</br>														
														<span style="font-family:verdana;font-size:11px">(Please do not reply to this mail as it is auto generated) </span></body></html>"""																																												
		system.net.sendEmail(smtp,senderEmailId,subject,emailBody,1,receiverEmailId)
		print("Send SuccessFully")
		return 1								
	except:	
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)

def MachineDisconectMail():		
	ListOfWos = EmailFunction.getWOlistForMail(0,0,0,0,1)
	defaultPath=system.tag.read("[default]JMES_InternalTags/DafaultTagPath").value
#	listofMail=[{"Id":"Hari.mhasalekar@tatatechnologies.com"},{"Id":"sushant.chavan@tatatechnologies.com"},{"Id":"Tejes.Yadav@tatatechnologies.com"}]		
	for i in (ListOfWos):
		woNo=i.get('WONo')	
		LineName=i.get('LineName')
		operationId=i.get('WorkFlowOperationId')
		WoId=i.get('WorkorderID')		
		LineName=LineName
		print "woNo: "+str(woNo)
		WoNumber=woNo		
		senderUserName='messupport@johnsoneectric.com'
		loggedUserId=1
		reasonName='Machine is disconnected from Kepware'
		comments='Please check the machine connectivity with kepware.'
		MachineList=EmailFunction.getmachineListagainstWo(WoNumber,WoId)
		
		print "MachineList Mail Script---:"+str(MachineList)
		for i in (MachineList):
			machineName=i.get('MachineName')
			parameterName="MachineConnection"
			tagPath = str(defaultPath)+str(machineName)+"/"+str(parameterName)
			parameterValue = system.tag.read(tagPath).value	
			listofMail=EmailFunction.getEmailId(WoNumber)
			for mail in(listofMail):
				emailId=mail.get("EmailId")		
				print "parameterValue: "+str(parameterValue)	
				if parameterValue==1:
					mailResult=EmailFunction.MachineDisconnectsendMail(machineName,LineName,operationId,WoNumber,senderUserName,loggedUserId,reasonName,comments,emailId)
					if mailResult==1:
						print "WoNumber:--"+str(WoNumber)
						print"Machine Status--"+str(parameterValue)
						print 'Mail Sent For Machine---'+str(machineName)
						print 'Mail Sentcsuccessfully---'+str(emailId)
						print"======================================================================"	
					else:
						pass
				else:
					pass				
						
def getEmailId(WONumber):
	try:
		apiPath = "OperatorConsole/GetMachineAlertEmails/"+str(WONumber)	
		url = URLPath + apiPath	
		resultData=None
		client = system.net.httpClient()
		data = client.get(url)
		if data.good:    
		  resultData=data.json
		  EmailList=resultData
	 	listOfEmail=[]
		for i in (EmailList):
			EmailId=i.get('EmailIds')
		splitEmails = EmailId.split(";")
		lengthOfLis=len(splitEmails)
		for i in range(lengthOfLis):
			email=splitEmails[i]
			eID={'EmailId':email}
			listOfEmail.append(eID)			  	  	  
		return listOfEmail
	except Exception as e:
		print("Email Error "+str(e))
		return []
		
		
#-----------------------------------------------------Mail alerts for PM Tool------------------------------------------------		
def getPMEmailId(WorkorderId):
			try:
				apiPath = "ProductionOperatorConsole/PMAlertEmails/"+str(WorkorderId)	
				url = URLPath + apiPath	
				resultData=None
				client = system.net.httpClient()
				data = client.get(url)
				if data.good:    
				  resultData=data.json
				  EmailList=resultData
			 	listOfEmail=()
			 	print "EmailList"+str(EmailList)
			 	if EmailList!=[]:
					for i in (EmailList):
						EmailId=i.get('EmailIds')
						AreaId = i.get('AreaId')
						EmailIdList = {"EmailId1":EmailId,'AreaId':AreaId}		  	  	  
					return EmailIdList
				else:
					emptylist = {"EmailId1":''}
					return emptylist  
			except Exception as e:
				print("Email Error "+str(e))
#				return []		

# ----------------------------Get The Wo List For PM Tools-----------------------------------------------------------
		# Application use: List of workorder for PM Life Alerts
		# Developer Name: Hari Mhasalekar
		# Created On: 25/05/2023
		# Updated By : 
		# Updated On :
def getWOlistForPMMail(entId,plantId,areaId,lineId,userId):	
	apiPath='OperatorConsole/GetOperatorConsoleWorkOrdersDetails?EnterpriseId='+str(entId)+'&PlantId='+str(plantId) + '&AreaId='+str(areaId)+'&LineId='+str(lineId)+'&MachineId='+str(0)+'&UserId='+str(userId)
	url = URLPath + apiPath
#	print url
	resultData=None
	client = system.net.httpClient()
	data = client.get(url)
	if data.good:    
	  APIResult=data.json
#	print"ResultData",(APIResult)	
	WODetailList=[]
	Id=0
	for i in (APIResult):
		Id=Id+1
		WoStatus=i.get('WoStatus')
		if WoStatus=='In-Progress' or WoStatus=='On-Hold' or WoStatus=='Not-Started':
			WONo=i.get('WONo')
			WorkorderID=i.get('WorkOrderId')				
			WorkFlowId=i.get('WorkFlowId')
			WorkFlowOperation=i.get('WorkFlowOperation')
			WorkFlowOperationId=i.get('WorkFlowOperationId')
			LineName=i.get('LineName')
			LineId=i.get('LineId')
			AreaId=i.get('AreaId')
			WOType=i.get('WorkOrderType')
			parameters={"WONo":WONo,"WorkorderID":WorkorderID,"WorkFlowOperation":WorkFlowOperation,"WorkFlowOperationId":WorkFlowOperationId,"LineName":LineName,"LineId":LineId,"WOType":WOType,"AreaId":AreaId}			
			WODetailList.append(parameters)
		else:
			pass
	return	WODetailList

#---------------------------------------------------------------------------------------------------------------------
		# Application use: Mail Body for PM Tool life Alerts @ 9AM china Time
		# Developer Name: Hari Mhasalekar
		# Created On: 25/05/2023
		# Updated By : 
		# Updated On :
def PMToolLifeMailAlert(EmailId,TD,AreaName):	
	import smtplib	
	import system
	import re	
	receiverEmailId = str(EmailId)
	receiverEmailId = receiverEmailId.strip()	
	try:	
		scriptName=' Email Function Send Mail'	
		smtpval = system.tag.read("[default]JMES_InternalTags/Send_Email/SMTP.value").value
		smtp = smtpval.strip()
		senderEmailId = system.tag.read("[default]JMES_InternalTags/Send_Email/Sender_SMPT.value").value
		senderEmailId = senderEmailId.strip()
		subject = "Tool Life Alerts"
			
		emailBody = """<html style="font-family:verdana;font-size:11px">
		  <style>
		    table,
		    th,
		    td {
		      border: 1px solid black;
		      border-collapse: collapse;
		    }
		  </style>
		  <body>
		    <table
		      border="0"
		      cellspacing="0"
		      cellpadding="0"
		      width="100%"
		      style="width: 100.0%;mso-cellspacing: 0in; mso-padding-alt: 0in 0in 0in 0in"
		    >
		      <tr style="mso-yfti-irow: 0; mso-yfti-firstrow: yes; height: 37.5pt">
		        <td
		          width="100%"
		          style="width: 100%; background: #FFA500; padding: 0in 0in 0in 15.0pt;height: 37.5pt"
		        >
		          <p style="mso-margin-top-alt: auto; mso-margin-bottom-alt: auto">
		            <span
		              style="font-size: 16.5pt; font-family: Verdana; color: white; letter-spacing: 1.5pt"
		            >
		              JEMES -Tool Life Alerts
		            </span>
		            <o:p></o:p>
		          </p>
		        </td>
		      </tr>
		    </table>
		    <div><b>Hello Team</b></div>
		    <p> Actual Production Count Exceeds the Set Alert Quantity for Area '"""+str(AreaName)+"""'. User Action Required:</p>
		    <p>
		      <b>List Of Tools </b>
		    </p>
		    <table style="width:100%">
		      <tr style="background-color: #B8E8FC;">
		        <td>Sr. No.</td>		    
		        <td>Tool Name</td>
		        <td>Tool Code</td>
		        <td>Max Tool Life</td>	
		        <td>Alert Qty Setting</td>
		        <td>Total Produced Qty</td>		       		   
		      	       		   
		        
		      </tr>
		      <tbody>
		        
		        """+TD+"""		        
		      </tbody>
		    </table>
		  </body>
		  </br>
		 <b>Note:</b>
		Please Visit <a href="https://www.johnsonelectric.com/">https://www.johnsonelectric.com/</a> for more details.</br>
		</br>
		</br>														
		<span style="font-family:verdana;font-size:11px">(Please do not reply to this mail as it is auto generated)
		</html>"""																																												
		system.net.sendEmail(smtp,senderEmailId,subject,emailBody,1,receiverEmailId)
		print("Email Sent SuccessFully For ID: ")+str(receiverEmailId)
		return 1								
	except:	
		import sys, os
		errorMessage=scriptName  +' Exception : '+  str(sys.exc_info()[1])
		Authentication.exceptionLogger(errorMessage)
		print errorMessage
		
#---------------------------------------------------------------------------------------------------------------------
		# Application use: Generate Email Alerts for PM Tool Life Everyday @ 9AM china Time
		# Developer Name: Hari Mhasalekar
		# Created On: 25/05/2023
		# Updated By : 
		# Updated On :			
def PMToolmailAlerts():
	ListOfWos =EmailFunction.getWOlistForPMMail(0,0,0,0,1)
	TD = ""
	TD2 = ""
	SrNo=0
	EmailIdListforMail =[]
	checkduplicateTool = []
	AllTools = []
	AreaIdList = []
#	EmailIdList =[]
	Reason = "Actual Production Qty is Greater Than Alert Qty Setting"
	for i in (ListOfWos):
		woNo=i.get('WONo')
		LineId=i.get('LineId')
		AreaIdInTool=i.get('AreaId')
#		print "AreaIdInTool: "+str(AreaIdInTool)
		WorkorderId=i.get('WorkorderID')
		machineID=0
#		print"WoId "+str(WorkorderId)
#		print"Wo Number "+str(woNo)		
		ToolDetails= ProductionOperatorConsole.NewgetMoldAssignmentDetails(WorkorderId,machineID)
#		print ("ToolDetails :")+str(ToolDetails)

				
		for toolList in (ToolDetails):
			ToolCode=toolList.get('MoldCode')
			ToolName=toolList.get('ToolName')
			AlertQty=toolList.get('AlertQty')
			MaxLife=toolList.get('MaxLife')
			IsLoaded=toolList.get('isLoaded')
			
			ActualProductionCount=toolList.get('ActualLife')

			if ToolCode not in checkduplicateTool:
				if ActualProductionCount>AlertQty:
					
					AllTools1 = {"ToolCode":ToolCode,"ToolName":ToolName,"AlertQty":AlertQty,"MaxLife":MaxLife,"ActualProductionCount":ActualProductionCount,"WoAreaId":AreaIdInTool}					
					AllTools.append(AllTools1)
					
					checkduplicateTool.append(ToolCode)	
		
					ToolName = ToolName
					ToolCode = ToolCode
					SrNo = SrNo+1
					if AreaIdInTool not in AreaIdList:
						AreaIdList.append(AreaIdInTool)

	print 'Area List '+ str(AreaIdList)
	for sortAreId in (AreaIdList):

		TD = ''
		SrNo = 0
		for sortToolAreawise in (AllTools):
			
			woAreaId = sortToolAreawise.get('WoAreaId')
			if woAreaId == sortAreId:
				SrNo = SrNo+1
				ToolCode = sortToolAreawise.get('ToolCode')
				ToolName = sortToolAreawise.get('ToolName')
				MaxLife = sortToolAreawise.get('MaxLife')
				AlertQty = sortToolAreawise.get('AlertQty')
				ActualProductionCount = sortToolAreawise.get('ActualProductionCount')
				TD1="""<tr>
						<td>"""+str(SrNo)+"""</td>												
						<td>"""+str(ToolName)+"""</td>
						<td>"""+str(ToolCode)+"""</td>
						<td>"""+str(MaxLife)+"""</td>
						<td>"""+str(AlertQty)+"""</td>						
						<td>"""+str(ActualProductionCount)+"""</td>											         	          
				        </tr>""" 
				TD += TD1
				checkduplicateTool.append(ToolCode)
			print TD
			parameters = {'AreaId':sortAreId}
	 		Emaillist = system.db.runNamedQuery('WorkorderOperation/ToolAlerts',parameters)
	 		eId = Emaillist.getValueAt(0,'EmailIds')
	 		AreaName = Emaillist.getValueAt(0,'AreaName')
	 		eId = eId.split(';')
	
		 	print "AreaName:"+str(AreaName)
			if TD!='':
				for Elist in range(len(eId)):
					EmailId = eId[Elist]		
					EmailFunction.PMToolLifeMailAlert(EmailId,TD,AreaName)

			
	

