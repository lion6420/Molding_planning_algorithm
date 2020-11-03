from utils.Oracle import API_Oracle
import cx_Oracle
from config.config import config_oracle
from Algorithm.molding import Mold
import datetime

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
    onworking_order = self.customQuery(sql, filterArgs=filterArgs, cols=cols, returnType='frame')
    result = [{}]*onworking_order.height

    # 已在使用模具
    onWorkMold = {}
    
    for index in range(onworking_order.height):
      mold = Mold(
        onworking_order[index]['"Part_NO"'],
        onworking_order[index]['"machine_ton"'],
        onworking_order[index]['"mold_NO"'],
        onworking_order[index]['"mold_Serial"'],
        onworking_order[index]['HOLENUM'],
        onworking_order[index]['"mold_position"'],
        True
      )
      onWorkMold.update({mold.CMDIE_NO: True}) # 紀錄已在使用的模具
      result[index] = {
        '鴻海料號': onworking_order[index]['"Part_NO"'],
        '帶版料號': onworking_order[index]['"Part_NO"'] + 'W' + onworking_order[index]['VER'],
        '版次': onworking_order[index]['VER'],
        '機台': onworking_order[index]['"machine_NO"'],
        '品名': onworking_order[index]['"product_name"'],
        '噸位': onworking_order[index]['"machine_ton"'],
        '模具': mold,
        '塑膠料號': onworking_order[index]['"plastic_Part_NO"'],
        '顏色': onworking_order[index]['"plastic_color"'],
        '總需求': onworking_order[index]['"plan_number"'],
        '產能': onworking_order[index]['UPH'],
        '生產時間': onworking_order[index]['"plan_work_time"'],
        '換模時間': onworking_order[index]['"mold_down_t"'],
        '起始時間': onworking_order[index]['"plan_s_time"'],
        '結束時間': onworking_order[index]['"plan_e_time"'],
        'priority': 0,
      }
    return onWorkMold, result

  def get_weeklyAmount(self):
    sql = '''
        SELECT "Part_NO", "plan_number", "real_NO", "delivery_time"
        FROM "week_plan", (
          SELECT MAX("week_NO") AS MWEEK
          FROM "week_plan", (
            SELECT MAX("year") AS MYEAR
            FROM "week_plan"
          ) maxYear
          WHERE "week_plan"."year" = maxYear.MYEAR
        ) resultTable
        WHERE "week_NO" = MWEEK
      '''
    data = self.customQuery(sql=sql)
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

  def getHistory(self, PN):
    date = datetime.datetime.now()
    dateBefore = date - datetime.timedelta(days=14) # cache 兩週
    cols = ['machine_NO', 'UPH', 'plastic_Part_NO', 'mold_NO', 'mold_Serial', 'mold_position', 'mold_hole', 'update_time', 'STATUS', 'MJDW']
    filterArgs = {
      'PN': PN,
      'time': str(dateBefore).split('.')[0]
    }
    sql = '''
      WITH MJTABLE AS 
      (
        SELECT CMDIE_NO, STATUS, MJDW
        FROM MJ_DATA
        WHERE "HH_NO1" = :PN
      ), 
      FINALTABLE AS 
      (
        SELECT "machine_NO", UPH, "plastic_Part_NO", "mold_NO",
              "mold_Serial", "mold_position", "mold_hole", "update_time",
              MJTABLE.STATUS, MJTABLE.MJDW
        FROM "work_list_schedule_his" 
        LEFT JOIN MJTABLE
        ON "mold_NO" = MJTABLE.CMDIE_NO
        WHERE "Part_NO" = :PN AND "update_time" >= TO_DATE(:time, 'YYYY-MM-DD HH24:MI:SS')
      )
      SELECT "machine_NO", UPH, "plastic_Part_NO", "mold_NO",
            "mold_Serial", "mold_position", "mold_hole", "update_time",
            FINALTABLE.STATUS, FINALTABLE.MJDW, count(*)
      FROM FINALTABLE
      WHERE STATUS = '正常入庫'
      GROUP BY "machine_NO", UPH, "plastic_Part_NO", "mold_NO",
              "mold_Serial", "mold_position", "mold_hole", "update_time",
              FINALTABLE.STATUS, FINALTABLE.MJDW
      ORDER BY "update_time" DESC
    '''
    historyLog = self.customQuery(sql, filterArgs=filterArgs, cols=cols, returnType='frame')

    return historyLog
