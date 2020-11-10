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
	def __init__(self, path_basic, week_plan_end_time, order_start_time):
		self.api_oracle = NWE_Molding_Oracle()
		self.basic_df = pd.read_excel(path_basic + 'molding_basic_information.xlsx')
		self.PN_list, self.weeklyDemand = self.api_oracle.get_weeklyAmount()
		self.order_start_time = order_start_time
		self.week_plan_end_time = week_plan_end_time
		self.onworking_mold, self.onworking_order = self.api_oracle.get_onworking_order(order_start_time)
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

	def cal_priority(self, moldAmount, urgent_tag, binded_machine):
		if urgent_tag == True:
			return 1
		elif binded_machine:
			return 2
		elif moldAmount > 0.3:
			return 3
		elif moldAmount > 0.5: 
			return 4
		elif moldAmount > 1:
			return 5
		else:
			return 6

	def getEditNumber(self, PN):
		editNumber = PN.split('W')[-1]
		return editNumber

	def get_mold(self, PN):# 模具資料
		cols = ['HH_NO1', 'MJDW', 'CMDIE_NO', 'DIE_NO', 'HOLENUM', 'STORE_ID', 'STATUS']
		data = self.api_oracle.queryFilterAll('MJ_DATA', {'HH_NO1__eq':PN, 'STATUS__eq':'正常入庫'}, cols=cols, returnType='frame')
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
				historyLog = self.api_oracle.getHistory(PN) # 歷史生產紀錄
				if historyLog.height>0:
					plastic_number = historyLog[0]['plastic_Part_NO'] # 找對應塑膠粒
				else:
					plastic_number = self.api_oracle.get_plasticNO(PN) # 找對應塑膠粒

				basic_information = self.basic_df[self.basic_df['鴻海料號'] == PN] # 找基本資料(噸位、UPH、品名)
				if len(basic_information)>0:
					tons = basic_information['需求機台'].tolist()[0]
					UPH = round(basic_information['產能(PCS/H)'].tolist()[0], 2)
					name = basic_information['品名'].tolist()[0]
				else:
					continue
				if UPH > 0:
					if plastic_number:
						color = self.get_color(plastic_number) # 查顏色
					else:
						color = 'others'
					if name == '導光柱' or name == '道光柱':
						color = '透明'

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
						if historyLog.height > mold_index:
							mold_chosen = Mold(
								PN,
								historyLog[mold_index]['MJDW'],
								historyLog[mold_index]['mold_NO'],
								historyLog[mold_index]['mold_Serial'],
								historyLog[mold_index]['mold_hole'],
								historyLog[mold_index]['mold_position'],
								historyLog[mold_index]['STATUS']
							)
						else:
							mold_chosen = self.get_mold(PN) # 模具
						if mold_chosen == None: # 如果沒模具可以用
							break

						# 機台綁定
						if historyLog.height > mold_index:
							input_machine = historyLog[mold_index]['machine_NO']
						elif len(machine_binded_list)>0:
							input_machine = machine_binded_list[mold_index]

						priority = self.cal_priority(moldAmount, False, input_machine) # calc Priority
						
						# update onworking mold
						self.onworking_mold.update({mold_chosen.CMDIE_NO: True})
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
							'priority': priority
						})
				else:
					continue
			else:
				continue

		return self.planningReadyQueue
