from api.API_Oracle import NWE_Molding_Oracle
from config.config import config_oracle
import datetime
from factory.NWE import *

api = NWE_Molding_Oracle(
	config_oracle['host'],
	config_oracle['port'],
	config_oracle['user'],
	config_oracle['password'],
	config_oracle['service_name'])

def get_onworking_order(order_start_time):
  filterArgs = {
    'plan_e_time__gt': order_start_time
  }
  
  onworking_order = api.queryFilterAll('arrangement_result', filterArgs)
  result = [{}]*len(onworking_order)
  for index, order in enumerate(onworking_order):
    result[index] = {
      '鴻海料號': order[6],
      '帶版料號': '',
      '機台': order[0],
      '品名': order[14],
      '噸位': order[1],
      '顏色': order[24],
      '總需求': order[15],
      '產能': order[8],
      '生產時間': order[5],
      '起始時間': order[3],
      '結束時間': order[4],
    }
  return result
