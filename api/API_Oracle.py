from utils.Oracle import API_Oracle
import cx_Oracle
from config.config import config_oracle
from Algorithm.molding import Mold

class NWE_Molding_Oracle(API_Oracle):
  def __init__(self,
    host=config_oracle['host'],
    port=config_oracle['port'],
    user=config_oracle['user'],
    password=config_oracle['password'],
    service_name=config_oracle['service_name']):
    super().__init__(host=host, port=port, user=user, password=password, service_name=service_name)

  def get_plasticNO(self, PN):
    filterArgs = {
      'PN': PN
    }
    sql = '''
      SELECT ITEM_NUMBER
      FROM BOM
      WHERE EXISTS (
        SELECT 1
        FROM "plastic_color_data"
        WHERE "plastic_part_NO" = BOM.ITEM_NUMBER
      )
      START WITH BOM.F_ITEM_NUMBER = :PN
      CONNECT BY PRIOR BOM.ITEM_NUMBER = BOM.F_ITEM_NUMBER
    '''
    plasticNO = self.customQuery(sql, queryType='one', filterArgs=filterArgs)
    if (plasticNO == None):
      return None
    return plasticNO[0]

  def get_onworking_order(self, order_start_time):
    filterArgs = {
      'time': order_start_time
    }
    cols = ['"machine_NO"', '"machine_ton"', '"mold_down_t"', '"plan_s_time"', '"plan_e_time"', '"plan_work_time"', '"Part_NO"', '"machine_CT"',\
            'UPH', '"mold_edit"', '"mold_Serial"', '"mold_NO"', '"mold_position"', '"package_size"', '"product_name"', '"plan_number"',\
            '"emergency"', '"mass_pro"', '"need"', '"same_mold_part_NO"', '"value"', '"total_value"', '"plastic_Part_NO"', '"mold_changeover_time"',\
            '"plastic_color"', '"note"', '"Seq"', '"timestamp"', '"has_been_open_work_list"', 'VER', 'HOLENUM']
    sql = '''
      SELECT "arrangement_result".*, MJ_DATA.HOLENUM
      FROM "arrangement_result"
      LEFT JOIN MJ_DATA
      ON "mold_NO" = CMDIE_NO AND "mold_Serial" = DIE_NO
      WHERE "plan_e_time" > :time
    '''
    onworking_order = self.customQuery(sql, filterArgs=filterArgs, cols=cols, returnType='dict')
    result = [{}]*len(onworking_order['"Seq"'])

    # 已在使用模具
    onWorkMold = {}
    
    for index, sequence in enumerate(onworking_order['"Seq"']):
      mold = Mold(
        onworking_order['"Part_NO"'][index],
        onworking_order['"machine_ton"'][index],
        onworking_order['"mold_NO"'][index],
        onworking_order['"mold_Serial"'][index],
        onworking_order['HOLENUM'][index],
        onworking_order['"mold_position"'][index],
        True
      )
      onWorkMold.update({mold.CMDIE_NO: True}) # 紀錄已在使用的模具
      result[index] = {
        '鴻海料號': onworking_order['"Part_NO"'][index],
        '帶版料號': onworking_order['"Part_NO"'][index] + 'W' + onworking_order['VER'][index],
        '版次': onworking_order['VER'][index],
        '機台': onworking_order['"machine_NO"'][index],
        '品名': onworking_order['"product_name"'][index],
        '噸位': onworking_order['"machine_ton"'][index],
        '模具': mold,
        '塑膠料號': onworking_order['"plastic_Part_NO"'][index],
        '顏色': onworking_order['"plastic_color"'][index],
        '總需求': onworking_order['"plan_number"'][index],
        '產能': onworking_order['UPH'][index],
        '生產時間': onworking_order['"plan_work_time"'][index],
        '換模時間': onworking_order['"mold_down_t"'][index],
        '起始時間': onworking_order['"plan_s_time"'][index],
        '結束時間': onworking_order['"plan_e_time"'][index],
        'priority': 0,
      }
    return onWorkMold, result

  def get_weeklyAmount(self, week):
    sql = '''
        SELECT "Part_NO", "plan_number", "real_NO", "delivery_time"
        FROM "week_plan" 
        WHERE "week_NO" =:week
      '''
    filterArgs = {'week': week}
    data = self.customQuery(sql=sql, filterArgs=filterArgs)
    result = {}
    PN_list = []
    def drop_moldSerial(PN):
      while(PN[-1] != 'W'):
        PN = PN[0:-1]
      return PN[0:-1]

    for row in data:
      temp_dict = {
        'Part_NO': row[0],
        'plan_number': row[1],
        'real_NO': row[2],
        'delivery_time': row[3],
        'planned': False,
      }
      PN = row[0]
      PN_withoutEdit = drop_moldSerial(PN)
      PN_list.append(PN_withoutEdit)
      result.update({PN_withoutEdit: temp_dict})
    return PN_list, result

  def update_weeklyAmount(self, amount, PN):
    finished_amount = self.queryFilterOne('week_plan', {'Part_NO__eq':PN})[4]
    if finished_amount !=None:
      amount = finished_amount + amount
    self.updateOne('week_plan', real_NO=amount, Part_NO=PN)
    return 'finish'

  def check_machineBinded(self, PN):
    queryResult = self.queryFilterAll('special_part_No', {'Part_NO__eq':PN})
    machine_list = []
    if queryResult != None:
      for query in queryResult:
        machine_list.append(query[0])
      return machine_list
    else:
      return []

  def check_stock(self, PN):
    data = self.queryFilterOne('SAP_STOCK', {'F_MATERIAL__eq':PN})
    if data:
      return data[3]
    else:
      return 0

