runas_connection = automationassets.get_automation_connection("AzureRunAsConnection")
bt=get_automation_runas_token()
sub=str(runas_connection["SubscriptionId"])
headers = {'Authorization': 'Bearer ' + bt, 'Content-Type': 'application/json'}
crg=None
crf="azurerm"
cde=False
az2tfmess="# File generated by az2tf see: https://github.com/andyt530/az2tf \n"
