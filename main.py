from Algorithm.weekly_order import preprocessing
import pandas as pd
import numpy as np
from factory.NWE import *
from Algorithm.planning import Planning
from Algorithm.onworking_order import get_onworking_order, get_onworking_order_TEST

# 週數
week = '22'

# 宣告工單起始、結束時間
#timeNow_list = datetime.datetime.now().date().strftime('%Y-%m-%d').split('-')
dateNow_list = ['2020', '06', '03']
dateAfter_list = ['2020', '06', '04']
date = dateNow_list[0] + dateNow_list[1] + dateNow_list[2]
dateAfter = dateAfter_list[0] + dateAfter_list[1] + dateAfter_list[2]
order_start_time = datetime.datetime.strptime((dateNow_list[0] + '-' + dateNow_list[1] + '-' + dateNow_list[2] + ' 19:30:00'), '%Y-%m-%d %H:%M:%S')
order_end_time = order_start_time + datetime.timedelta(days=1)

order_start_time_day = datetime.datetime.strptime((dateAfter_list[0] + '-' + dateAfter_list[1] + '-' + dateAfter_list[2] + ' 07:30:00'), '%Y-%m-%d %H:%M:%S')
order_end_time_day = order_start_time_day + datetime.timedelta(hours=12)

order_start_time_night = datetime.datetime.strptime((dateNow_list[0] + '-' + dateNow_list[1] + '-' + dateNow_list[2] + ' 19:30:00'), '%Y-%m-%d %H:%M:%S')
order_end_time_night = order_start_time_night + datetime.timedelta(hours=12)

# 宣告路徑
path_basic = './basic_information/'
path_initial = path_basic + '/Initial_condition/WK' + week + '/'

#模型初始化
onworking_order = get_onworking_order_TEST(order_start_time) # 在機上工單初始化
emergency_order = [] # 急件資料初始化
prep = preprocessing(path_basic) # 週計畫初始化
weekly_order = prep.get_planning_input()

#start planning
basic_setting = {
  'order_start_time': order_start_time,
  'order_end_time': order_end_time
}
P = Planning(onworking_order, emergency_order, weekly_order, basic_setting)
total_weekly_planning = P.main_function()

# Show and output result
Factory_NWE.show_line_information()
Factory_NWE.to_csv('result' + date)
Factory_NWE.output_daily_planning()
