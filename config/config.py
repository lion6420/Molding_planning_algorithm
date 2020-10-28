import cx_Oracle

#Oracle dsn_tns
dsn_tns = cx_Oracle.makedsn(
    '10.149.1.218',
    '1521',
    service_name = 'nweorcl'
)

# DB
config_mysql = {
  'host' : '10.124.131.81',
  'port' : 8871,
  'user' : 'root',
  'password' : 'foxconn168!',
  'db' : 'test'}

config_JTtest = {
  'host' : 'localhost',
  'port' : 3306,
  'user' : 'root',
  'password' : 'tony1234',
  'db' : 'planning_test'}

config_oracle = {
  'host' : '10.149.1.218',
  'port' : 1521,
  'user' : 'NWEIAI',
  'password' : 'NWE123456',
  'service_name' : 'nweorcl'
}