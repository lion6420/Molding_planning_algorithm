from weekly_order import preprocessing
import pandas as pd
import numpy as np
from setting import *
from planning import Planning
from onworking_order import get_onworking_order

#模型初始化
onworking_order = get_onworking_order() # 在機上工單初始化
emergency_order = [] # 急件資料初始化
prep = preprocessing(path_basic) # 週計畫初始化
weekly_order = prep.get_planning_input()

#start planning
P = Planning(onworking_order, emergency_order, weekly_order)
total_weekly_planning = P.main_function()

# Show and output result
Factory_NWE.show_line_information()
Factory_NWE.to_csv('result' + date)
Factory_NWE.output_daily_planning()
