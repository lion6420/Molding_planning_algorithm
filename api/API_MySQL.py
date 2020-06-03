import pandas as pd
import numpy as np
import os
import datetime
from utils.MySQL import API_MySQL 


class NWE_Molding_MySQL(API_MySQL):
  def __init__(self, host, port, user, password, db):
    super().__init__(host=host, port=port, user=user, password=password, db=db)

  def get_weekly(self):
    data = self.queryAll('week_plan')
    return data

  def revise_weekly(self, PN, amount):
    totalAmount = self.queryFilterOne('week_plan', {'Part_NO__eq':PN})[0][1]
    remainingAmount = totalAmount - amount
    if remainingAmount < 0:
      remainingAmount = 0
    self.updateOne('week_plan', plan_number=remainingAmount, Part_NO=PN)
    return 'Revise finished'

  def write_planning_result(self, value):
    col = '(machine_NO, machine_ton, mold_down_t, plan_s_time, plan_e_time, plan_work_time, Part_NO, \
            machine_CT, UPH, mold_edit, mold_Serial, mold_NO, mold_position, package_size, product_name, \
            plan_number, emergency, mass_pro, need, same_mold_part_NO, value, total_value, plastic_Part_NO, \
            mold_changeover_time, plastic_color, note)'
    self.insertOne('arrangement_result', col, value)