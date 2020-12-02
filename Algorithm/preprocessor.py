import pandas as pd
import numpy as np
import os
from api.API_Oracle import NWE_Molding_Oracle
from Algorithm.molding import Mold
from tqdm import tqdm
from .DataStructure.Planning import ReadyQueue
import math
import datetime


class preprocessor():
	def __init__(self, week_plan_end_time, order_start_time):
		self.api_oracle = NWE_Molding_Oracle()
		self.PN_list, self.weeklyDemand = self.api_oracle.get_weeklyAmount()
		self.order_start_time = order_start_time
		self.week_plan_end_time = week_plan_end_time
		self.onworking_mold, self.onworking_order = self.api_oracle.get_onworking_order(order_start_time)
		# history
		self.historyLog = None
		self.history_mold = [] # 避免歷史紀錄的模具被其他機台拿走
		# output
		self.planningReadyQueue = ReadyQueue()
	

	def get_color(self, plastic_number):
		data = self.api_oracle.queryFilterOne('plastic_color_data', {'plastic_part_NO__eq':plastic_number})
		if data:
			return data[1]
		else:
			return 'others'

	def check_machineBinded(self, PN):
		machine_binded = self.api_oracle.check_machineBinded(PN)
		return machine_binded

	def cal_priority(self, moldAmount, urgent_tag, binded_machine, history_binded):
		if urgent_tag == True:
			return 1
		elif binded_machine:
			return 2
		elif history_binded:
			return 3
		elif moldAmount > 0.3:
			return 4
		elif moldAmount > 0.5: 
			return 5
		elif moldAmount > 1:
			return 6
		else:
			return 7

	def getEditNumber(self, PN):
		editNumber = PN.split('W')[-1]
		return editNumber

	def getHistory(self, PN):
		self.historyLog = self.api_oracle.getHistory(PN) # 歷史生產紀錄(return frame)
		self.history_mold = []
		for log_index in range(self.historyLog.height):
			self.history_mold.append(self.historyLog[log_index]['mold_NO'])
		
	def get_mold(self, PN):# 模具資料
		data = self.api_oracle.getMold(PN)
		if data.height > 0:
			best_mold_index = None
			for index in range(data.height):
				if data[index]['CMDIE_NO'] in self.onworking_mold:
					continue
				elif best_mold_index == None:
					best_mold_index = index
				elif int(data[index]['DIE_NO'][1:]) > int(data[best_mold_index]['DIE_NO'][1:]):
					best_mold_index = index
				else:
					continue
			if best_mold_index != None:
				mold_data = Mold(
					PN,
					data[best_mold_index]['MJDW'],
					data[best_mold_index]['CMDIE_NO'],
					data[best_mold_index]['DIE_NO'],
					data[best_mold_index]['HOLENUM'],
					data[best_mold_index]['STORE_ID'], 
					data[best_mold_index]['STATUS']
				)
				return mold_data
			else: # 找不到可用模具
				return None
		else: # 資料庫找不到模具
			return None

	def cal_UPH(self, PN):
		CT = self.api_oracle.getPartCT(PN)
		if (CT>0):
			UPH = 3600/CT
			return UPH
		else:
			return 0

	def getBasicInfomation(self, PN, PN_withEdit):
		name = self.api_oracle.getPartName(PN)
		UPH = self.cal_UPH(PN_withEdit)
		if self.historyLog.height>0:
			plastic_number = self.historyLog[0]['plastic_Part_NO'] # 找對應塑膠粒
		else:
			plastic_number = self.api_oracle.get_plasticNO(PN) # 找對應塑膠粒

		if plastic_number:
			color = self.get_color(plastic_number) # 查顏色
		else:
			color = 'others'
		if name == '導光柱' or name == '道光柱':
			color = '透明'

		return name, UPH, plastic_number, color

	def get_planning_input(self):
		# 已經在機台上料號
		for onworking_order_index, eachOnworkOrder in enumerate(self.onworking_order):
			PN = eachOnworkOrder['鴻海料號']
			if (PN not in self.weeklyDemand):
				continue
			PN_withEdit = self.weeklyDemand[PN]['Part_NO']
			self.weeklyDemand[PN]['planned'] = True

			# 檢查庫存
			stock_amount = self.api_oracle.check_stock(PN_withEdit)
			if (self.weeklyDemand[PN]['real_NO'] > 0): # 扣減本週已產數量、扣減庫存
				amount = self.weeklyDemand[PN]['plan_number'] - self.weeklyDemand[PN]['real_NO'] - stock_amount
			else:
				amount = self.weeklyDemand[PN]['plan_number'] - 0 - stock_amount
			
			if amount > 0:
				eachOnworkOrder['總需求'] = amount
				eachOnworkOrder['帶版料號'] = PN_withEdit
				eachOnworkOrder['生產時間'] = None
				eachOnworkOrder['換模時間'] = None
				eachOnworkOrder['開始時間'] = None
				eachOnworkOrder['結束時間'] = None
				eachOnworkOrder['onworking_tag'] = False
				self.planningReadyQueue.enqueue(eachOnworkOrder)
			else:
				continue

		for PN_index, PN in enumerate(tqdm(self.PN_list, ascii=True)):
			# 檢查是否排過
			if (self.weeklyDemand[PN]['planned'] == True):
				continue
			PN_withEdit = self.weeklyDemand[PN]['Part_NO']
			# 版次
			editNumber = self.getEditNumber(PN_withEdit)
			# 檢查庫存
			stock_amount = self.api_oracle.check_stock(PN_withEdit)
			if (self.weeklyDemand[PN]['real_NO'] > 0): # 扣減本週已產數量、扣減庫存
				amount = self.weeklyDemand[PN]['plan_number'] - self.weeklyDemand[PN]['real_NO'] - stock_amount
			else:
				amount = self.weeklyDemand[PN]['plan_number'] - 0 - stock_amount

			if amount>0:
				self.getHistory(PN) # 獲取歷史紀錄
				name, UPH, plastic_number, color = self.getBasicInfomation(PN, PN_withEdit) # 獲取基本資料

				if UPH > 0:
					## 計算模具數量
					dayRemained = (self.week_plan_end_time - self.order_start_time).days # 計算需要的模具數量(一週七天)
					if dayRemained<1:
						dayRemained = 1
					moldAmount = math.ceil(amount/(UPH*24*dayRemained)) # 大於7天的料號拆多台機，最多三台
					if moldAmount>3:
						moldAmount = 3

					machine_binded_list = self.check_machineBinded(PN)
					if len(machine_binded_list)>0 and moldAmount > len(machine_binded_list): # if 有綁定機台，最大機台數量依據綁定機台數量
						moldAmount = len(machine_binded_list)

					amount = amount//moldAmount # 單台機排程數量

					input_machine = None
					for mold_index in range(moldAmount):
						# 模具
						if self.historyLog.height > mold_index:
							if (self.historyLog[mold_index]['STATUS'] == '正常入庫' and self.historyLog[mold_index]['mold_NO'] not in self.onworking_mold):
								mold_chosen = Mold(
									PN,
									self.historyLog[mold_index]['MJDW'],
									self.historyLog[mold_index]['mold_NO'],
									self.historyLog[mold_index]['mold_Serial'],
									self.historyLog[mold_index]['mold_hole'],
									self.historyLog[mold_index]['mold_position'],
									self.historyLog[mold_index]['STATUS']
								)
							else:
								mold_chosen = self.get_mold(PN)
						else:
							mold_chosen = self.get_mold(PN) # 模具
						if mold_chosen == None: # 如果沒模具可以用
							break
						
						# 模具噸位
						tons = mold_chosen.MJDW

						# 機台綁定
						force_binded = False
						history_binded = False
						if len(machine_binded_list)>0: # forced bind
							input_machine = machine_binded_list[mold_index]
							force_binded = True
						elif self.historyLog.height > mold_index: # history bind
							input_machine = self.historyLog[mold_index]['machine_NO']
							history_binded = True
						
						priority = self.cal_priority(moldAmount, False, force_binded, history_binded) # calc Priority
						
						# update onworking mold
						self.onworking_mold.update({mold_chosen.CMDIE_NO: True})

						self.weeklyDemand[PN]['planned'] = True
						# put into queue
						self.planningReadyQueue.enqueue({
							'鴻海料號': PN,
							'帶版料號': PN_withEdit,
							'版次': editNumber,
							'機台': input_machine,
							'品名': name,
							'噸位': tons,
							'模具': mold_chosen,
							'塑膠料號': plastic_number,
							'顏色': color,
							'總需求': amount,
							'產能': UPH,
							'生產時間': None,
							'換模時間': None,
							'起始時間': None,
							'結束時間': None,
							'onworking_tag': False,
							'priority': priority
						})
				else:
					continue
			else:
				continue

		return self.planningReadyQueue
