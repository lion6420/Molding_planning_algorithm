from Algorithm.molding import *

# 多模穴查詢
planty_mold_chamber_dic = {'700-41438-02WA' : ['700-41439-02WA'], '700-110082-01WC' : ['700-110083-01WC']}

# 內外交料號不同
# ['1B41ATE00K01E','700-38589-01WA']

# 宣告工廠、線別、機台基本資訊
# A線
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

# B線
B01 = Machine('B01', '200T',  'others',  1, [], 24.0)
B02 = Machine('B02', '200T',  'others',  1, [], 24.0)
B03 = Machine('B03', '200T',  'others',  1, [], 24.0)
B04 = Machine('B04', '120T',  'others', 1, [], 24.0)
B05 = Machine('B05', '350T',  'others',  1, [], 24.0)
B06 = Machine('B06', '350T',  'others',  1, [], 24.0)
B07 = Machine('B07', '350T',  'others',  1, [], 24.0)
B08 = Machine('B08', '350T',  'others', 1, [], 24.0)
B09 = Machine('B09', '350T',  'others', 1, [], 24.0)
B10 = Machine('B10', '350T',  'others', 1, [], 24.0)
B11 = Machine('B11', '350T',  'others',  1, [], 24.0)
B12 = Machine('B12', '350T',  'others', 1, [], 24.0)
B13 = Machine('B13', '350T',  'others',  1, [], 24.0)
B14 = Machine('B14', '450T',  'others', 1, [], 24.0)
B = Line('B', 14, 14, 0, [B01, B02, B03, B04, B05,\
                          B06, B07, B08, B09, B10,\
                          B11, B12, B13, B14])

# C線
C01 = Machine('C01', '350T',  'others',  1, [], 24.0)
C02 = Machine('C02', '350T',  'others',  1, [], 24.0)
C03 = Machine('C03', '350T',  'others',  1, [], 24.0)
C04 = Machine('C04', '350T',  'others', 1, [], 24.0)
C05 = Machine('C05', '350T',  'others',  1, [], 24.0)
C06 = Machine('C06', '350T',  'others',  1, [], 24.0)
C07 = Machine('C07', '350T',  'others',  1, [], 24.0)
C08 = Machine('C08', '350T',  'others', 1, [], 24.0)
C09 = Machine('C09', '350T',  'others', 1, [], 24.0)
C10 = Machine('C10', '350T',  'others', 1, [], 24.0)
C11 = Machine('C11', '450T',  'others',  1, [], 24.0)
C12 = Machine('C12', '450T',  'others', 1, [], 24.0)
C = Line('C', 12, 12, 0, [C01, C02, C03, C04, C05,\
                          C06, C07, C08, C09, C10,\
                          C11, C12])

# D線
D01 = Machine('D01', '180T',  'others',  1, [], 24.0)
D02 = Machine('D02', '180T',  'others',  1, [], 24.0)
D03 = Machine('D03', '180T',  'others',  1, [], 24.0)
D04 = Machine('D04', '180T',  'others', 1, [], 24.0)
D05 = Machine('D05', '180T',  'others',  1, [], 24.0)
D06 = Machine('D06', '180T',  'others',  1, [], 24.0)
D07 = Machine('D07', '180T',  'others',  1, [], 24.0)
D08 = Machine('D08', '180T',  'others', 1, [], 24.0)
D09 = Machine('D09', '180T',  'others', 1, [], 24.0)
D10 = Machine('D10', '180T',  'others', 1, [], 24.0)
D11 = Machine('D11', '180T',  'others',  1, [], 24.0)
D12 = Machine('D12', '180T',  'others', 1, [], 24.0)
D13 = Machine('D13', '180T',  'others',  1, [], 24.0)
D14 = Machine('D14', '180T',  'others',  1, [], 24.0)
D15 = Machine('D15', '180T',  'others',  1, [], 24.0)
D16 = Machine('D16', '180T',  'others', 1, [], 24.0)
D17 = Machine('D17', '180T',  'others',  1, [], 24.0)
D18 = Machine('D18', '180T',  'others',  1, [], 24.0)
D19 = Machine('D19', '180T',  'others',  1, [], 24.0)
D = Line('D', 19, 19, 0, [D01, D02, D03, D04, D05,\
                          D06, D07, D08, D09, D10,\
                          D11, D12, D13, D14, D15,\
                          D16, D17, D18, D19])

# E線
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
Factory_NWE = Factory('NWE_molding', [A, B, C, D, E, G])
