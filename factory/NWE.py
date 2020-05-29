import pandas as pd
import numpy as np
from Algorithm.molding import *
import datetime
import os

# 多模穴查詢
planty_mold_chamber_dic = {'700-41438-02WA' : ['700-41439-02WA'], '700-110082-01WC' : ['700-110083-01WC']}

# 內外交料號不同
# ['1B41ATE00K01E','700-38589-01WA']

# 宣告工廠、線別、機台基本資訊
# A 線
A01 = Real_machine_status('A01', '130T',  'trans',  1, [], 24.0, 24.0, [],  None, None)
A02 = Real_machine_status('A02', '130T',  'trans',  1, [], 24.0, 24.0, [],  None, None)
A03 = Real_machine_status('A03', '130T',  'trans',  1, [], 24.0, 24.0, [],  None, None)
A04 = Real_machine_status('A04', '130T',  'others', 1, [], 24.0, 24.0, [],  None, None)
A05 = Real_machine_status('A05', '130T',  'trans',  1, [], 24.0, 24.0, [],  None, None)
A06 = Real_machine_status('A06', '100T',  'trans',  1, [], 24.0, 24.0, [],  None, None)
A07 = Real_machine_status('A07', '100T',  'trans',  1, [], 24.0, 24.0, [],  None, None)
A08 = Real_machine_status('A08', '100T',  'others', 1, [], 24.0, 24.0, [],  None, None)
A09 = Real_machine_status('A09', '100T',  'others', 1, [], 24.0, 24.0, [],  None, None)
A10 = Real_machine_status('A10', '100T',  'others', 1, [], 24.0, 24.0, [],  None, None)
A11 = Real_machine_status('A11', '130T',  'trans',  1, [], 24.0, 24.0, [],  None, None)
A12 = Real_machine_status('A12', '130T',  'others', 1, [], 24.0, 24.0, [],  None, None)
A13 = Real_machine_status('A13', '130T',  'trans',  1, [], 24.0, 24.0, [],  None, None)
A14 = Real_machine_status('A14', '130T',  'others', 1, [], 12.0, 12.0, [],  None, None)
A15 = Real_machine_status('A15', '130T',  'others', 1, [], 24.0, 24.0, [],  None, None)
A = Line('A', 15, 15, 0, [A01, A02, A03, A04, A05,\
                          A06, A07, A08, A09, A10,\
                          A11, A12, A13, A14, A15])

# E 線
E01 = Real_machine_status('E01', '130T',  'others', 1, [], 24.0, 24.0, [],  None, None)
E02 = Real_machine_status('E02', '130T',  'white',  1, [], 24.0, 24.0, [],  None, None)
E03 = Real_machine_status('E03', '130T',  'white',  1, [], 24.0, 24.0, [],  None, None)
E04 = Real_machine_status('E04', '130T',  'others', 1, [], 24.0, 24.0, [],  None, None)
E05 = Real_machine_status('E05', '130T',  'others', 1, [], 24.0, 24.0, [],  None, None)
E = Line('E', 5, 5, 0, [E01, E02, E03, E04, E05])

# G線
G01 = Real_machine_status('G01', '100T',  'others', 1, [], 24.0, 24.0, [],  None, None)
G02 = Real_machine_status('G02', '100T',  'trans',  1, [], 24.0, 24.0, [],  None, None)
G03 = Real_machine_status('G03', '100T',  'others', 1, [], 24.0, 24.0, [],  None, None)
G04 = Real_machine_status('G04', '100T',  'others', 1, [], 24.0, 24.0, [],  None, None)
G05 = Real_machine_status('G05', '100T',  'others', 1, [], 24.0, 24.0, [],  None, None)
G06 = Real_machine_status('G06', '100T',  'trans',  1, [], 24.0, 24.0, [],  None, None)
G07 = Real_machine_status('G07', '100T',  'others', 1, [], 24.0, 24.0, [],  None, None)
G08 = Real_machine_status('G08', '100T',  'others', 1, [], 24.0, 24.0, [],  None, None)
G = Line('G', 8, 8, 0, [G01, G02, G03, G04, G05, G06, G07, G08])

# D9、D10廠
Factory_NWE = Factory('NWE_molding', [A, E, G])
