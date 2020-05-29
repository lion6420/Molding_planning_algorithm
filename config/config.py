import cx_Oracle

#Oracle dsn_tns
dsn_tns = cx_Oracle.makedsn(
    '10.132.131.222',
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

config_oracle = {
  'host' : '10.132.131.222',
  'port' : 1521,
  'user' : 'NWEIAI',
  'password' : 'NWE123456',
  'service_name' : 'nweorcl'
}