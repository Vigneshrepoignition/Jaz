														--Created by :- Hari Mhasalekar,		Created ON:-11th  March 2023	Modified On:- 11th March 2023
														--Pupose	 :-	To Start the Workorder	Comment:- Please DO not Modify this code																	
exec usp_WorkOrderOperations
@WorkOrderId  =:WorkOrderId,        
@UserId =:UserId,   
@IsClubbed=:IsClubbed,  
@WorkOrderStatusId =:WorkOrderStatusId,
@ScanBadge =:ScanBadge,
@HoldReasonCodeId =:HoldReasonCodeId,
@Comment =:Comment
select 1
