from Algorithm.weekly_order import preprocessing
import pandas as pd
import numpy as np
from factory.NWE import *
from Algorithm.planning import Planning
from Algorithm.onworking_order import get_onworking_order, get_onworking_order_TEST

# 宣告工單起始、結束時間、需求導入時間
week = 38
dateNow_list = datetime.datetime.now().date().strftime('%Y-%m-%d').split('-')
dateAfter_list = (datetime.datetime.now()+datetime.timedelta(days=1)).date().strftime('%Y-%m-%d').split('-')

# 計算本週剩餘生產日
week_day = datetime.datetime.now().weekday() + 1
remained_day = 5 - week_day
if (remained_day<0):
  remained_day = 0

# 本週結算時間
week_plan_end_day = (datetime.datetime.now()+datetime.timedelta(days=remained_day)).date().strftime('%Y-%m-%d').split('-')

# 工單起始、結束時間
order_start_time = datetime.datetime.strptime((dateNow_list[0] + '-' + dateNow_list[1] + '-' + dateNow_list[2] + ' 19:30:00'), '%Y-%m-%d %H:%M:%S')
order_end_time = order_start_time + datetime.timedelta(days=1)
# 需求導入時間
week_plan_end_time = datetime.datetime.strptime((week_plan_end_day[0] + '-' + week_plan_end_day[1] + '-' + week_plan_end_day[2] + ' 00:00:00'), '%Y-%m-%d %H:%M:%S')

# 宣告路徑
path_basic = './basic_information/'

#模型初始化
onworking_order = get_onworking_order(order_start_time) # 在機上工單初始化
emergency_order = [] # 急件資料初始化
prep = preprocessing(path_basic, week, week_plan_end_time, order_start_time, onworking_order) # 週計畫初始化
weekly_order = prep.get_planning_input() # get週計畫ReadyQueue
weekly_order.InsertionSort() # 根據priority排序

#start planning
time_setting = {
  'order_start_time': order_start_time,
  'order_end_time': order_end_time
}
P = Planning(onworking_order, emergency_order, weekly_order, time_setting)
total_weekly_planning = P.main_function()

print('---------------Process succeed--------------')
# Show and output result
Factory_NWE.show_line_information()
Factory_NWE.to_csv('result_' + datetime.datetime.now().date().strftime('%Y-%m-%d'))
# Factory_NWE.output_daily_planning()
