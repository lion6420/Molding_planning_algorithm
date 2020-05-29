from api.API_Oracle import NWE_Molding_Oracle
from config.config import config_oracle

api = NWE_Molding_Oracle(
	config_oracle['host'],
	config_oracle['port'], 
	config_oracle['user'], 
	config_oracle['password'], 
	config_oracle['service_name'])

def check_stock(PN):
  data = api.queryFilterOne('SAP_STOCK', {'F_MATERIAL__eq':PN})
  if data:
    return data[3]
  else:
    return 0