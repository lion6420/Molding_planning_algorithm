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
A01 = Machine('A01', '130T',  'trans',  1, [], 24.0)
A02 = Machine('A02', '130T',  'trans',  1, [], 24.0)
A03 = Machine('A03', '130T',  'trans',  1, [], 24.0)
A04 = Machine('A04', '130T',  'others', 1, [], 24.0)
A05 = Machine('A05', '130T',  'trans',  1, [], 24.0)
A06 = Machine('A06', '100T',  'trans',  1, [], 24.0)
A07 = Machine('A07', '100T',  'trans',  1, [], 24.0)
A08 = Machine('A08', '100T',  'others', 1, [], 24.0)
A09 = Machine('A09', '100T',  'others', 1, [], 24.0)
A10 = Machine('A10', '100T',  'others', 1, [], 24.0)
A11 = Machine('A11', '130T',  'trans',  1, [], 24.0)
A12 = Machine('A12', '130T',  'others', 1, [], 24.0)
A13 = Machine('A13', '130T',  'trans',  1, [], 24.0)
A14 = Machine('A14', '130T',  'others', 1, [], 24.0)
A15 = Machine('A15', '130T',  'others', 1, [], 24.0)
A = Line('A', 15, 15, 0, [A01, A02, A03, A04, A05,\
                          A06, A07, A08, A09, A10,\
                          A11, A12, A13, A14, A15])

# E 線
E01 = Machine('E01', '130T',  'others', 1, [], 24.0)
E02 = Machine('E02', '130T',  'white',  1, [], 24.0)
E03 = Machine('E03', '130T',  'white',  1, [], 24.0)
E04 = Machine('E04', '130T',  'others', 1, [], 24.0)
E05 = Machine('E05', '130T',  'others', 1, [], 24.0)
E = Line('E', 5, 5, 0, [E01, E02, E03, E04, E05])

# G線
G01 = Machine('G01', '100T',  'others', 1, [], 24.0)
G02 = Machine('G02', '100T',  'trans',  1, [], 24.0)
G03 = Machine('G03', '100T',  'others', 1, [], 24.0)
G04 = Machine('G04', '100T',  'others', 1, [], 24.0)
G05 = Machine('G05', '100T',  'others', 1, [], 24.0)
G06 = Machine('G06', '100T',  'trans',  1, [], 24.0)
G07 = Machine('G07', '100T',  'others', 1, [], 24.0)
G08 = Machine('G08', '100T',  'others', 1, [], 24.0)
G = Line('G', 8, 8, 0, [G01, G02, G03, G04, G05, G06, G07, G08])

# D9、D10廠
Factory_NWE = Factory('NWE_molding', [A, E, G])
