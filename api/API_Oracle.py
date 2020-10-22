from utils.Oracle import API_Oracle
import cx_Oracle

config_oracle = {
  'host' : '10.132.131.222',
  'port' : 1521,
  'user' : 'NWEIAI',
  'password' : 'NWE123456',
  'service_name' : 'nweorcl'
}

class NWE_Molding_Oracle(API_Oracle):
  def __init__(self, host, port, user, password, service_name):
    super().__init__(host=host, port=port, user=user, password=password, service_name=service_name)

  def get_plasticNO(self, PN):
    self.plasticNO = None
    def queryPlasticNO(PN):
      if self.plasticNO != None:
        return
      checkPlastic = self.queryFilterOne('plastic_color_data', {'plastic_part_NO__eq':PN})
      if checkPlastic:
        self.plasticNO = checkPlastic[0]
        return
      else:
        data = self.queryFilterAll('BOM', {'F_ITEM_NUMBER__eq':PN})
        if (len(data) == 0):
          return
        for d in data:
          queryPlasticNO(d[2])
    queryPlasticNO(PN)

    return self.plasticNO

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
      if (len(PN.split('-')) == 3 or len(PN.split('.')) == 3): # Ex: 700-124961-01、440.00553.005
        while(PN[-1].isnumeric() == False):
          PN = PN[:-1]
        return PN
      else: # Ex: 1B51HEE00-01E
        count = 0
        while(PN[-1] != 'E' and (PN[-1].isnumeric() == False or (PN[-1].isnumeric() == True and count == 0))):
          PN = PN[:-1]
          count = count + 1
        if PN[-2].isnumeric(): # Ex: 1B51KCY00-02E
          return PN
        else:
          while(PN[-2] != 'E'):
            PN = PN[:-1]
          PN = PN[:-1]
        return PN

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

