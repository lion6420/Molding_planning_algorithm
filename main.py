from preprocessing import preprocessing
import pandas as pd
import numpy as np
from setting import *
from planning import Planning

# # Weekly Preprocessing
# p = preprocessing()
# input = p.get_planning_input()

# Start planning
#initial model input
pre = preprocessing(path_basic)
emergency = []
weekly = pre.get_planning_input()


#start planning
P = Planning(emergency, weekly)
total_weekly_planning = P.main_function()

# Show and output result
Factory_NWE.show_line_information()
Factory_NWE.to_csv('result' + date)
Factory_NWE.output_daily_planning()
