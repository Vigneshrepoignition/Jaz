exec  usp_AddReturnFromSparePartRequest_Ignition

 @woNumber =:workOrderNumber  ,             
 @requestNumberId =   :requestNumberId ,                  
 @sparePartId =   :sparePartNumberId ,                            
 @returningQty =  :returningQty ,                  
 @returningSlotId =  :slotId ,                  
 @createdBy =  :userId ,
 @returnBy = :returnBy 
 
 Select 1
