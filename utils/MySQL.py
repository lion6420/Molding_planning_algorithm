# MySQL General CLASS
import pymysql

class API_MySQL():
  def __init__(self, host='localhost', port=3306, user='root', password='tony1234', db='test', cursor=None, conn=None):
    self.host = host
    self.port = port
    self.user = user
    self.password = password
    self.db = db
    self.cursor = cursor
    self.conn = conn

  def make_connection(self):
    self.conn = pymysql.connect(
      host=self.host,
      port=self.port,
      user=self.user,
      password=self.password,
      db=self.db)
    self.cursor = self.conn.cursor()
    
  def disconnection(self):
    self.cursor.close()
    self.conn.close()

  def queryAll(self, table):
    self.make_connection()
    sql = "SELECT * FROM " + table
    self.cursor.execute(sql)
    data = self.cursor.fetchall()
    self.disconnection()
    return data

  def queryFilter(self, table, **kwargs):
    self.make_connection()
    sql = "SELECT * FROM " + table + " WHERE "
    count = 0
    for k, v in kwargs.items():
      if count == 0:
        sql = sql + k + '=' + '"' + str(v) + '" '
        count+=1
      else: 
        sql = sql + 'and ' + k + '=' + '"' + str(v) + '" '
        count+=1
    self.cursor.execute(sql)
    data = self.cursor.fetchall()
    self.disconnection()
    return data

  def updateOne(self, table, **kwargs):
    self.make_connection()
    sql = "UPDATE " + table + " SET "
    count = 0
    for k, v in kwargs.items():
      if count == 0:
        sql = sql + k + '=' + str(v) + ' WHERE '
        count+=1
      elif count == 1:
        sql = sql + k + '=' + '"' + str(v) + '" '
        count+=1
      else:
        sql = sql + 'and ' + k + '=' + '"' + str(v) + '" '
        count+=1
    self.cursor.execute(sql)
    self.conn.commit()
    self.disconnection()
    return
    