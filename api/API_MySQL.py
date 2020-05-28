import pandas as pd
import numpy as np
import os
import datetime
from utils.MySQL import API_MySQL 

config = {
  'host' : '10.124.131.81',
  'port' : 8871,
  'user' : 'root',
  'password' : 'foxconn168!',
  'db' : 'test'}


class NWE_Molding_MySQL(API_MySQL):
  def __init__(self, host, port, user, password, db):
    super().__init__(host=host, port=port, user=user, password=password, db=db)

  def get_weekly(self):
    data = self.queryAll('week_plan')
    return data

  def revise_weekly(self, PN, amount):
    totalAmount = self.queryFilter('week_plan', Part_NO=PN)[0][1]
    remainingAmount = totalAmount - amount
    if remainingAmount < 0:
      remainingAmount = 0
    self.updateOne('week_plan', plan_number=remainingAmount, Part_NO=PN)
    return 'Revise finished'