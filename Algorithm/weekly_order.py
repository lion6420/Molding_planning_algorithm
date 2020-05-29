import pandas as pd
import numpy as np
import os
from api.API_MySQL import NWE_Molding_MySQL
from api.API_Oracle import NWE_Molding_Oracle
from config.config import config_mysql, config_oracle
from Algorithm.molding import Mold
from tqdm import tqdm


class preprocessing():
	def __init__(self, path_basic):
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
		self.weeklyDemand = self.api_oracle.queryAll('week_plan')
		self.base10List = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	
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
		for w_d in tqdm(self.weeklyDemand, ascii=True):
			amount = amount = w_d[1] - w_d[4]
			if amount>0:
				PN = w_d[0]
				PN_withoutEdit = self.drop_moldSerial(w_d[0])
				plastic_number = self.api_oracle.get_plasticNO(PN)
				name = self.api_oracle.queryFilterOne('MATERIAL', {'ITEM_NO__eq':PN})[7]
				basic_information = self.basic_df[self.basic_df['鴻海料號'] == PN_withoutEdit]
				if len(basic_information)>0:
					tons = basic_information['需求機台'].tolist()[0]
					UPH = round(basic_information['產能(PCS/H)'].tolist()[0], 2)
				else:
					continue
				if UPH > 0:
					if plastic_number:
						color = self.get_color(self.drop_moldSerial(plastic_number))
					else:
						color = 'others'
					if name == '導光柱' or name == '道光柱':
						color = '透明'
					result.append({
						'鴻海料號': PN_withoutEdit,
						'帶版料號': PN,
						'機台': None,
						'品名': name,
						'噸位': tons,
						'顏色': color,
						'總需求': amount,
						'產能': UPH,
						'生產時間': None,
						'起始時間': None,
						'結束時間': None,
					})
				else:
					continue
			else:
				continue
		print('Prerocessing succeeded.')
		print('Start planning...')
		return result
