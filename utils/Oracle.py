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

  def customQuery(self, sql, queryType='all', filterArgs={}):
    self.make_connection()
    self.cursor.execute(sql, filterArgs)
    if (queryType == 'all'):
      data = self.cursor.fetchall()
    elif (queryType == 'one'):
      data = self.cursor.fetchone()
    
    return data

  def queryAll(self, table):
    self.make_connection()
    sql = 'SELECT * FROM "' + table + '"'
    self.cursor.execute(sql)
    data = self.cursor.fetchall()
    self.disconnection()
    return data

  def queryFilterAll(self, table, filterArgs, cols=[], returnType='tuple'):
    self.make_connection()
    if (len(cols)>0):
      result = {}
      sql = 'SELECT '
      for (index,col) in enumerate(cols):
        result.update({col:[]})
        if (index == len(cols)-1): sql = sql + col + ' FROM "' + table + '" WHERE '
        else: sql = sql + col + ','
    else:
      sql = 'SELECT * FROM "' + table + '" WHERE '
    count = 0
    input = {}
    for k, v in filterArgs.items():
      key = k.split('__')[0]
      operater = k.split('__')[1]
      if operater == 'eq':
        sql_toAppend = '"' + key + '"=:' + key
        input.update({key:v})
      elif operater == '!eq':
        sql_toAppend = '"' + key + '"!=:' + key
        input.update({key:v})
      elif operater == 'gt':
        sql_toAppend = '"' + key + '">:' + key
        input.update({key:v})
      elif operater == 'gte':
        sql_toAppend = '"' + key + '">=:' + key
        input.update({key:v})
      elif operater == 'lt':
        sql_toAppend = '"' + key + '"<:' + key
        input.update({key:v})
      elif operater == 'lte':
        sql_toAppend = '"' + key + '"<=:' + key
        input.update({key:v})
      elif operater == 'bt':
        sql_toAppend = '"' + key + '" BETWEEN :' + key + '_1 AND :' + key + '_2'
        input.update({key + '_1':v[0]})
        input.update({key + '_2':v[1]})
      if count == 0:
        sql = sql + sql_toAppend
      else:
        sql = sql + ' and ' + sql_toAppend
      count+=1
    self.cursor.execute(sql, input)
    data = self.cursor.fetchall()
    self.disconnection()

    # return dict
    if (returnType == 'dict'):
      for row in data:
        for (row_index, row_ele) in enumerate(row):
          result[cols[row_index]].append(row_ele)
      return result
    # return tuple
    elif (returnType == 'tuple'):
      return data

  def queryFilterOne(self, table, filterArgs, cols=[], returnType='tuple'):
    self.make_connection()
    if (len(cols)>0):
      result = {}
      sql = 'SELECT '
      for (index,col) in enumerate(cols):
        result.update({col:[]})
        if (index == len(cols)-1): sql = sql + col + ' FROM "' + table + '" WHERE '
        else: sql = sql + col + ','
    else:
      sql = 'SELECT * FROM "' + table + '" WHERE '
    count = 0
    input = {}
    for k, v in filterArgs.items():
      key = k.split('__')[0]
      operater = k.split('__')[1]
      if operater == 'eq':
        sql_toAppend = '"' + key + '"=:' + key
        input.update({key:v})
      elif operater == '!eq':
        sql_toAppend = '"' + key + '"!=:' + key
        input.update({key:v})
      elif operater == 'gt':
        sql_toAppend = '"' + key + '">:' + key
        input.update({key:v})
      elif operater == 'gte':
        sql_toAppend = '"' + key + '">=:' + key
        input.update({key:v})
      elif operater == 'lt':
        sql_toAppend = '"' + key + '"<:' + key
        input.update({key:v})
      elif operater == 'lte':
        sql_toAppend = '"' + key + '"<=:' + key
        input.update({key:v})
      elif operater == 'bt':
        sql_toAppend = '"' + key + '" BETWEEN :' + key + '_1 AND :' + key + '_2'
        input.update({key + '_1':v[0]})
        input.update({key + '_2':v[1]})
      if count == 0:
        sql = sql + sql_toAppend
      else:
        sql = sql + ' and ' + sql_toAppend
      count+=1
    self.cursor.execute(sql, input)
    data = self.cursor.fetchone()
    self.disconnection()

    # return dict
    if (returnType == 'dict'):
      for row in data:
        for (row_index, row_ele) in enumerate(row):
          result[cols[row_index]].append(row_ele)
      return result
    # return tuple
    elif (returnType == 'tuple'):
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

  