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
    if PN[0] == '7' or PN[0] == '8':
      return PN
    else:
      data = self.queryFilterAll('BOM', {'F_ITEM_NO__eq':PN})
      if data == []:
        return None
      for d in data:
        return self.get_plasticNO(d[5])

  def update_weeklyAmount(self, amount, PN):
    finished_amount = self.queryFilterOne('week_plan', {'Part_NO__eq':PN})[4]
    if finished_amount !=None:
      amount = finished_amount + amount
    self.updateOne('week_plan', real_NO=amount, Part_NO=PN)
    return 'finish'

  def check_machineBinded(self, PN):
    queryResult = self.queryFilterAll('special_part_No', {'Part_NO__eq':PN})
    if (PN == '1B33LM400-02EWA'):
      print(queryResult)
    machine_list = []
    if queryResult != None:
      for query in queryResult:
        machine_list.append(query[0])
      return machine_list
    else:
      return []

