import pandas as pd
import numpy as np
from molding import *
import datetime
import os
import cx_Oracle

#資料庫
dsn_tns = cx_Oracle.makedsn(
    '10.132.131.222',
    '1521',
    service_name = 'nweorcl'
)

# 週數
week = '20'

# 宣告工單起始、結束時間
#timeNow_list = datetime.datetime.now().date().strftime('%Y-%m-%d').split('-')
dateNow_list = ['2020', '05', '20']
dateAfter_list = ['2020', '05', '21']
date = dateNow_list[0] + dateNow_list[1] + dateNow_list[2]
dateAfter = dateAfter_list[0] + dateAfter_list[1] + dateAfter_list[2]
order_start_time = datetime.datetime.strptime((dateNow_list[0] + '-' + dateNow_list[1] + '-' + dateNow_list[2] + ' 19:30:00'), '%Y-%m-%d %H:%M:%S')
order_end_time = order_start_time + datetime.timedelta(days=1)

order_start_time_day = datetime.datetime.strptime((dateAfter_list[0] + '-' + dateAfter_list[1] + '-' + dateAfter_list[2] + ' 07:30:00'), '%Y-%m-%d %H:%M:%S')
order_end_time_day = order_start_time_day + datetime.timedelta(hours=12)

order_start_time_night = datetime.datetime.strptime((dateNow_list[0] + '-' + dateNow_list[1] + '-' + dateNow_list[2] + ' 19:30:00'), '%Y-%m-%d %H:%M:%S')
order_end_time_night = order_start_time_night + datetime.timedelta(hours=12)

# 多模穴查詢
planty_mold_chamber_dic = {'700-41438-02WA' : ['700-41439-02WA'], '700-110082-01WC' : ['700-110083-01WC']}

# 內外交料號不同
# ['1B41ATE00K01E','700-38589-01WA']



# 宣告路徑
path_basic = './basic_information/'
path_initial = path_basic + '/Initial_condition/WK' + week + '/'

# initial_df = pd.read_excel(path_initial + 'daily_initial_condition_' + dateNow_list[1] + dateNow_list[2] + '.xlsx')

# # Temp for simulating the real situation of machine
# Order_A = []
# df_A = initial_df[initial_df['線別'] == 'A']
# machine_name_A = df_A['機台號'].tolist()
# part_number_A = df_A['鴻海料號'].tolist()
# part_name_A = df_A['品名'].tolist()
# demand_A = df_A['總需求'].tolist()
# UPH_A = df_A['產能'].tolist()

# Order_G = []
# df_G = initial_df[initial_df['線別'] == 'G']
# machine_name_G = df_G['機台號'].tolist()
# part_number_G = df_G['鴻海料號'].tolist()
# part_name_G = df_G['品名'].tolist()
# demand_G = df_G['總需求'].tolist()
# UPH_G = df_G['產能'].tolist()

# Order_E = []
# df_E = initial_df[initial_df['線別'] == 'E']
# machine_name_E = df_E['機台號'].tolist()
# part_number_E = df_E['鴻海料號'].tolist()
# part_name_E = df_E['品名'].tolist()
# demand_E = df_E['總需求'].tolist()
# UPH_E = df_E['產能'].tolist()

# last_name = ''
# order_list = []
# for a, m_name in enumerate(machine_name_A):
#     time_needed_A = round(int(demand_A[a])/int(UPH_A[a]), 2)
#     hour_needed_A = int(str(time_needed_A).split('.')[0])
#     minute_needed_A = (int(str(time_needed_A).split('.')[1])/100)*60
#     delayed_order_end_time_A = order_start_time + datetime.timedelta(hours=hour_needed_A, minutes=minute_needed_A)
#     if part_number_A[a] == 'None':
#         newOrder = None
#     else:
#         newOrder = Order(part_number_A[a], part_name_A[a], demand_A[a], demand_A[a], UPH_A[a], order_start_time, delayed_order_end_time_A, \
#                      order_start_time, delayed_order_end_time_A, time_needed_A, urgent_tag=False)
    
#     if last_name == '':
#         order_list.append(newOrder)
#         last_name = m_name
#     elif last_name == m_name:
#         order_list.append(newOrder)
#     else:
#         Order_A.append(order_list)
#         order_list = [newOrder]
#         last_name = m_name
#     if a == len(machine_name_A)-1:
#         Order_A.append(order_list)


# last_name = ''
# order_list = []
# for e, m_name in enumerate(machine_name_E):
#     time_needed_E = round(int(demand_E[e])/int(UPH_A[e]), 2)
#     hour_needed_E = int(str(time_needed_E).split('.')[0])
#     minute_needed_E = (int(str(time_needed_E).split('.')[1])/100)*60
#     delayed_order_end_time_E = order_start_time + datetime.timedelta(hours=hour_needed_E, minutes=minute_needed_E)
#     if part_number_E[e] == 'None':
#         newOrder = None
#     else:
#         newOrder = Order(part_number_E[e], part_name_E[e], demand_E[e], demand_E[e], UPH_E[e], order_start_time, delayed_order_end_time_E, \
#                          order_start_time, delayed_order_end_time_E, time_needed_E, urgent_tag=False)

#     if last_name == '':
#         order_list.append(newOrder)
#         last_name = m_name
#     elif last_name == m_name:
#         order_list.append(newOrder)
#     else:
#         Order_E.append(order_list)
#         order_list = [newOrder]
#         last_name = m_name
#     if e == len(machine_name_E)-1:
#         Order_E.append(order_list)

# last_name = ''
# order_list = []
# for g, m_name in enumerate(machine_name_G):
#     time_needed_G = round(int(demand_G[g])/int(UPH_G[g]), 2)
#     hour_needed_G = int(str(time_needed_G).split('.')[0])
#     minute_needed_G = (int(str(time_needed_G).split('.')[1])/100)*60
#     delayed_order_end_time_G = order_start_time + datetime.timedelta(hours=hour_needed_G, minutes=minute_needed_G)
#     if part_number_G[g] == 'None':
#         newOrder = None
#     else:
#         newOrder = Order(part_number_G[g], part_name_G[g], demand_G[g], demand_G[g], UPH_G[g], order_start_time, delayed_order_end_time_G, \
#                      order_start_time, delayed_order_end_time_G, time_needed_G, urgent_tag=False)

#     if last_name == '':
#         order_list.append(newOrder)
#         last_name = m_name
#     elif last_name == m_name:
#         order_list.append(newOrder)
#     else:
#         Order_G.append(order_list)
#         order_list = [newOrder]
#         last_name = m_name
#     if g == len(machine_name_G)-1:
#         Order_G.append(order_list)


# 宣告工廠、線別、機台基本資訊
# A 線
A01 = Real_machine_status('A01', '130T',  'trans',  1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
A02 = Real_machine_status('A02', '130T',  'trans',  1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
A03 = Real_machine_status('A03', '130T',  'trans',  1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
A04 = Real_machine_status('A04', '130T',  'others', 1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
A05 = Real_machine_status('A05', '130T',  'trans',  1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
A06 = Real_machine_status('A06', '100T',  'trans',  1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
A07 = Real_machine_status('A07', '100T',  'trans',  1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
A08 = Real_machine_status('A08', '100T',  'others', 1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
A09 = Real_machine_status('A09', '100T',  'others', 1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
A10 = Real_machine_status('A10', '100T',  'others', 1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
A11 = Real_machine_status('A11', '130T',  'trans',  1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
A12 = Real_machine_status('A12', '130T',  'others', 1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
A13 = Real_machine_status('A13', '130T',  'trans',  1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
A14 = Real_machine_status('A14', '130T',  'others', 1, [], 12.0, 12.0, [],  order_start_time, order_end_time)
A15 = Real_machine_status('A15', '130T',  'others', 1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
A = Line('A', 15, 15, 0, [A01, A02, A03, A04, A05,\
                          A06, A07, A08, A09, A10,\
                          A11, A12, A13, A14, A15])

# E 線
E01 = Real_machine_status('E01', '130T',  'others', 1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
E02 = Real_machine_status('E02', '130T',  'white',  1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
E03 = Real_machine_status('E03', '130T',  'white',  1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
E04 = Real_machine_status('E04', '130T',  'others', 1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
E05 = Real_machine_status('E05', '130T',  'others', 1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
E = Line('E', 5, 5, 0, [E01, E02, E03, E04, E05])

# G線
G01 = Real_machine_status('G01', '100T',  'others', 1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
G02 = Real_machine_status('G02', '100T',  'trans',  1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
G03 = Real_machine_status('G03', '100T',  'others', 1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
G04 = Real_machine_status('G04', '100T',  'others', 1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
G05 = Real_machine_status('G05', '100T',  'others', 1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
G06 = Real_machine_status('G06', '100T',  'trans',  1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
G07 = Real_machine_status('G07', '100T',  'others', 1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
G08 = Real_machine_status('G08', '100T',  'others', 1, [], 24.0, 24.0, [],  order_start_time, order_end_time)
G = Line('G', 8, 8, 0, [G01, G02, G03, G04, G05, G06, G07, G08])

# D9、D10廠
Factory_NWE = Factory('NWE_molding', [A, E, G])
