# Oracle Database General CLASS
import cx_Oracle

class API_Oracle():
  def __init__(self, host, port, user, password, service_name, cursor=None, conn=None):
    self.user = user
    self.password = password
    self.dsn_tns = cx_Oracle.makedsn(
      host,
      port,
      service_name = service_name
    )
    self.cursor = cursor
    self.conn = conn

  def make_connection(self):
    self.conn = cx_Oracle.connect(
      user = self.user,
      password = self.password,
      dsn = self.dsn_tns,
      encoding="UTF-8"
    )
    self.cursor = self.conn.cursor()

  def disconnection(self):
    self.cursor.close()
    self.conn.close()

  def queryAll(self, table):
    self.make_connection()
    sql = 'SELECT * FROM "' + table + '"'
    self.cursor.execute(sql)
    data = self.cursor.fetchall()
    self.disconnection()
    return data

  def queryFilterAll(self, table, **kwargs):
    self.make_connection()
    sql = 'SELECT * FROM "' + table + '" WHERE "'
    count = 0
    input = {}
    for k, v in kwargs.items():
      if count == 0:
        sql = sql + k + '"=:' + k
        input.update({k:v})
        count+=1
      else: 
        sql = sql + ' and "' + k + '"=:' + k
        input.update({k:v})
        count+=1
    self.cursor.execute(sql, input)
    data = self.cursor.fetchall()
    self.disconnection()
    return data

  def queryFilterOne(self, table, **kwargs):
    self.make_connection()
    sql = 'SELECT * FROM "' + table + '" WHERE "'
    count = 0
    input = {}
    for k, v in kwargs.items():
      if count == 0:
        sql = sql + k + '"=:' + k
        input.update({k:v})
        count+=1
      else: 
        sql = sql + ' and "' + k + '"=:' + k
        input.update({k:v})
        count+=1
    self.cursor.execute(sql, input)
    data = self.cursor.fetchone()
    self.disconnection()
    return data

  def updateOne(self, table, **kwargs):
    self.make_connection()
    sql = 'UPDATE "' + table + '" SET "'
    count = 0
    input={}
    for k, v in kwargs.items():
      if count == 0:
        input.update({k:v})
        sql = sql + k + '"=:' + k + ' WHERE "'
        count+=1
      elif count == 1:
        input.update({k:v})
        sql = sql + k + '"=:' + k
        count+=1
      else:
        input.update({k:v})
        sql = sql + ' and "' + k + '"=:' + k
        count+=1
    self.cursor.execute(sql, input)
    self.conn.commit()
    self.disconnection()
    return

  