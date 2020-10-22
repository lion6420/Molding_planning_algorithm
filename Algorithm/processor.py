import pandas as pd
import numpy as np
import os
import datetime
from .molding import *
from factory.NWE import *
import math
from .identification import Identification
from api.API_Oracle import NWE_Molding_Oracle

api_oracle = NWE_Molding_Oracle()

Id = Identification()

class Processor():
	def __init__(self, onworking_order, emergency, total_weekly_planning, basic_setting):
		self.onworking_order = onworking_order
		self.emergency = emergency
		self.total_weekly_planning = total_weekly_planning
		self.basic_setting = basic_setting
		self.record_ordered_part_number = []
		self.buffer_list = []
		self.urgent = False
		self.release = False
		self.buffer = False
		self.bind_machine = None
		self.if_stop = False
		self.mold_change = True
		self.plastic_change = True

	def planning(self, order):
		## Get fitted machine
		if order['機台'] == None or order['結束時間'] == None:
			if order['機台'] != None: # Special PN binded to specific machine
				machine_chosen = Factory_NWE.get_machine_by_name(order['機台'])
				if machine_chosen == None:
					return False
				if machine_chosen.remaining_time == 0:
					return False
			else: # Normal PN
				machine_chosen = self.find_fitted_machine(order)
			if machine_chosen == None: # No machine available for this order
				return False
				
			## Time calculation
			start_time, end_time, time_needed = self.time_function(order, machine_chosen)
			if time_needed == None:
				return False

			## Put into order
			newOrder = Order(order['鴻海料號'], order['品名'], order['噸位'], order['模具'], order['塑膠料號'], order['顏色'], math.ceil(time_needed*order['產能']), \
											order['產能'], start_time, end_time, time_needed, urgent_tag=self.urgent)
			machine_chosen.order_list.append(newOrder)

			# 修改資料庫週數量
			api_oracle.update_weeklyAmount(math.ceil(time_needed*order['產能']), order['帶版料號'])

		else: # Onworking order
			machine_chosen = Factory_NWE.get_machine_by_name(order['機台'])
			end_time = order['結束時間']
			newOrder = Order(order['鴻海料號'], order['品名'], order['噸位'], order['模具'], order['塑膠料號'], order['顏色'], order['總需求'], \
										   order['產能'], order['起始時間'], order['結束時間'], order['生產時間'], urgent_tag=self.urgent)
			machine_chosen.order_list.append(newOrder)

		#機台剩餘時間扣減	
		remainig_time = self.machine_remaining_time_calculation(machine_chosen, end_time)
		machine_chosen.remaining_time = remainig_time
		
		self.record_ordered_part_number.append(newOrder.part_number)

		# Reset default status
		self.bind_machine = None
		self.mold_change = True
		self.plastic_change = True

		return True

	def find_fitted_machine(self, order):
		tons = order['噸位']
		color = order['顏色']

		# Find fittable machine
		machine_chosen_list = []
		machine_chosen = None
		#-3 Condition 3: Normal
		for line in Factory_NWE.line_list:
			temp_list = line.get_ok_machine() # step 1: check if machines are able to be used
			if temp_list == []:
				continue
			temp_list = line.get_machine_by_tons(tons, machine_list=temp_list) # step 2: tons
			if temp_list == []:
				continue
			temp_list = line.get_machine_by_color(color, machine_list=temp_list) # step 3: color
			if temp_list == []:
				continue
			machine_chosen = line.get_biggest_remaining_time(machine_list=temp_list) # step 4: remaining time
			if machine_chosen:
				machine_chosen_list.append(machine_chosen)
		
		if machine_chosen_list == []: #-3-(1) Type2: if no machine is usable, return None
			return None

		else: #-3-(2) Type3: plural machine is usable, find the best one (the longest remaining time); or the best machine had been found
			keep_max = machine_chosen_list[0]
			for m in machine_chosen_list:
				if m.remaining_time > keep_max.remaining_time:
					keep_max = m
			machine_chosen = keep_max
			return machine_chosen
			

	
	def time_function(self, order, machine_chosen):

		# Calculate time needed
		time_needed = round((order['總需求'] / order['產能']), 2)
		# 該工單生產時間計算，if大於三天截斷
		if time_needed > 24.0:
			time_needed = 24.0

		if len(machine_chosen.order_list) == 0:
			self.mold_change = False
		elif machine_chosen.order_list[-1].part_number == order['鴻海料號']:
			self.mold_change = False

		# Calculate start time, end time
		# if it is no need mold changing
		if self.mold_change == False:
			start_time, end_time, time_needed = self.time_calculation(False, time_needed, machine_chosen)

			# if mold changing is required, another 4 hours is needed
		else:
			start_time, end_time, time_needed = self.time_calculation(True, time_needed, machine_chosen)
		
		if time_needed == None:
			return None, None, None
		
		return start_time, end_time, time_needed

	def time_calculation(self, if_moldChange, time_needed, machine_chosen):
		if if_moldChange == True:
			# 起始、結束時間計算
			hour_needed = int(str(time_needed).split('.')[0])
			minute_needed = (int(str(time_needed).split('.')[1])/100)*60
			if machine_chosen.order_list:
				start_time = machine_chosen.order_list[-1].end_time + datetime.timedelta(hours=4)
			else:
				start_time = self.basic_setting['order_start_time'] + datetime.timedelta(hours=4)
			end_time = start_time + datetime.timedelta(hours=hour_needed, minutes=minute_needed)
			return start_time, end_time, time_needed
		else:
			# 起始、結束時間計算
			hour_needed = int(str(time_needed).split('.')[0])
			minute_needed = (int(str(time_needed).split('.')[1])/100)*60
			if machine_chosen.order_list:
				start_time = machine_chosen.order_list[-1].end_time
			else:
				start_time = self.basic_setting['order_start_time']
			end_time = start_time + datetime.timedelta(hours=hour_needed, minutes=minute_needed)
			return start_time, end_time, time_needed

	def machine_remaining_time_calculation(self, machine_chosen, end_time):
		delta_time = (self.basic_setting['order_end_time'] - end_time)
		remaining_time = delta_time.days*24 + round(delta_time.seconds/3600, 2)
		if remaining_time < 0:
			remaining_time = 0
		return remaining_time
			
	def main_function(self):
		# 1. Yesterday delayed
		for input in self.onworking_order:
			if_succeed = self.planning(input)

		weekly_order_number = self.total_weekly_planning.get_orderNumber()
		while(weekly_order_number>0):
			weekly_order_number-=1
			input = self.total_weekly_planning.dequeue().value
			if_succeed = self.planning(input)
			if self.if_stop == True:
				break

		return self.total_weekly_planning