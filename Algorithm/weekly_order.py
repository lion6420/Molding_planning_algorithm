import pandas as pd
import numpy as np
import os
from api.API_MySQL import NWE_Molding_MySQL
from api.API_Oracle import NWE_Molding_Oracle
from config.config import config_mysql, config_oracle
from Algorithm.molding import Mold
from Algorithm.check_stock import check_stock
from tqdm import tqdm
from .DataStructure.Planning import ReadyQueue
import math


class preprocessing():
	def __init__(self, path_basic, week_plan_input_time, week_plan_end_time, order_start_time, onworking_order):
		self.api_mysql = NWE_Molding_MySQL(
			config_mysql['host'],
			config_mysql['port'], 
			config_mysql['user'], 
			config_mysql['password'], 
			config_mysql['db'])
		self.api_mysql_nwe = NWE_Molding_MySQL(
			config_mysql['host'],
			config_mysql['port'], 
			config_mysql['user'], 
			config_mysql['password'], 
			'NWE')
		self.api_oracle = NWE_Molding_Oracle(
			config_oracle['host'],
			config_oracle['port'], 
			config_oracle['user'], 
			config_oracle['password'], 
			config_oracle['service_name']
		)
		self.basic_df = pd.read_excel(path_basic + 'molding_basic_information.xlsx')
		self.weeklyDemand = self.api_oracle.queryFilterAll('week_plan', {'timestamp__gt': week_plan_input_time})
		self.order_start_time = order_start_time
		self.week_plan_end_time = week_plan_end_time
		self.onworking_order = onworking_order
		self.base10List = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		self.planningReadyQueue = ReadyQueue()
	
	def if_int(self, str):
		if str in self.base10List:
			return True
		else:
			return False

	def drop_moldSerial(self, PN):
		while(PN[-1] != 'E' and self.if_int(PN[-1]) == False):
			PN = PN[:-1]
		return PN

	def get_color(self, plastic_number):
		data = self.api_oracle.queryFilterOne('plastic_color_data', {'plastic_part_NO__eq':plastic_number})
		if data:
			return data[1]
		else:
			return 'others'

	def check_machineBinded(self, PN):
		machine_binded = self.api_oracle.check_machineBinded(PN)
		return machine_binded

	def cal_priority(self, moldAmount, urgent_tag, binded, onWork_tag):
		if onWork_tag == True:
			return 0
		if urgent_tag == True:
			return 1
		elif len(binded) > 0:
			return 2
		elif moldAmount > 1:
			return 3
		elif moldAmount > 0.5: 
			return 4
		elif moldAmount > 0.3:
			return 5
		else:
			return 6

	# def get_UPH(self, PN):# 模具資料
	# 	data = self.api_oracle.queryFilterAll('MJ_DATA', {'HH_NO1__eq':PN})
	# 	if data:
	# 		keep_best_mold = data[0]
	# 		for d in data:
	# 			if d[15]!=None and d[15] < keep_best_mold[15]:
	# 				keep_best_mold = d
	# 			else:
	# 				continue
	# 		if keep_best_mold[15] == None:
	# 			print('second')
	# 			return None
	# 		mold_data = Mold(PN, keep_best_mold[8], keep_best_mold[11], keep_best_mold[15], keep_best_mold[12], keep_best_mold[30])
	# 		return mold_data.get_UPH()
	# 	else:
	# 		print(PN)
	# 		return None


	def get_planning_input(self):
		result = []
		print('Start order preprocessing...')
		print('-----------------------------')
		# temp for debug #
		PN_debug = []
		tons_debug = []
		UPH_debug = []
		color_debug = []
		amount_debug = []
		# #
		for index, w_d in enumerate(tqdm(self.weeklyDemand, ascii=True)):
			# 檢查庫存
			stock_amount = check_stock(w_d[0])
			if (w_d[4]):
				amount = w_d[1] - w_d[4] - stock_amount
			else:
				amount = w_d[1] - 0 - stock_amount

			# 扣減庫剩餘需求
			if amount>0:
				PN = w_d[0]
				PN_withoutEdit = self.drop_moldSerial(w_d[0])
				plastic_number = self.api_oracle.get_plasticNO(PN) # 找對應塑膠粒
				# find_name = self.api_oracle.queryFilterOne('MATERIAL', {'ITEM_NO__eq':PN}) # 找品名
				# if find_name:
				# 	name = find_name[7]
				# else:
				# 	name = None
				basic_information = self.basic_df[self.basic_df['鴻海料號'] == PN_withoutEdit] # 找基本資料(噸位、UPH、品名)
				if len(basic_information)>0:
					tons = basic_information['需求機台'].tolist()[0]
					UPH = round(basic_information['產能(PCS/H)'].tolist()[0], 2)
					name = basic_information['品名'].tolist()[0]
					PN_debug.append(PN) #debug
					tons_debug.append(tons) #debug
					UPH_debug.append(UPH) #debug
					amount_debug.append(amount) #debug
				else:
					continue
				if UPH > 0:
					if plastic_number:
						color = self.get_color(self.drop_moldSerial(plastic_number)) # 查顏色
					else:
						color = 'others'
					if name == '導光柱' or name == '道光柱':
						color = '透明'
					color_debug.append(color) #debug

					## 計算模具數量
					dateRemaind = (self.week_plan_end_time - self.order_start_time).days # 計算需要的模具數量(一週七天)
					if dateRemaind<1:
						dateRemaind = 1
					moldAmount = amount/(UPH*24*dateRemaind)

					machine_binded_list = self.check_machineBinded(PN)
					moldNumber = math.ceil(moldAmount) # 大於7天的料號拆多台機，最多三台
					if moldNumber>3:
						moldNumber = 3
					if len(machine_binded_list)>0 and moldNumber > len(machine_binded_list): # if 有綁定機台，最大機台數量依據綁定機台數量
						moldNumber = len(machine_binded_list)
					amount = amount//moldNumber

					input_machine = None
					for i in range(moldNumber):
						onWork_tag = False
						if len(machine_binded_list)>0:
							input_machine = machine_binded_list[i]
						else:
							# onwork_binded
							for onworking_order_index, eachOnworkOrder in enumerate(self.onworking_order):
								if eachOnworkOrder['鴻海料號'] == PN_withoutEdit:
									if input_machine == eachOnworkOrder['機台']:
										continue
									else:
										onWork_tag = True
										input_machine = eachOnworkOrder['機台']
						priority = self.cal_priority(moldAmount, False, machine_binded_list, onWork_tag) # calc Priority
						
						# put into queue
						self.planningReadyQueue.enqueue({
							'鴻海料號': PN_withoutEdit,
							'帶版料號': PN,
							'機台': input_machine,
							'品名': name,
							'噸位': tons,
							'顏色': color,
							'總需求': amount,
							'產能': UPH,
							'生產時間': None,
							'起始時間': None,
							'結束時間': None,
							'模具數': moldAmount,
							'priority': priority
						})
				else:
					continue
			else:
				continue
		print('Prerocessing succeeded.')
		print('Start planning...')
		debug_dic = {'PN': PN_debug, 'tons': tons_debug, 'UPH': UPH_debug, 'color': color_debug, 'amount': amount_debug}
		debug_df = pd.DataFrame(debug_dic)
		debug_df.to_csv('./' + 'debug_20200731' + '.csv', encoding='utf_8_sig', index=False) 
		return self.planningReadyQueue
