#################
# Molding Class #
#################

import numpy as np
import pandas as pd
import datetime
import cx_Oracle

def myconverter(r):
  if isinstance(r, datetime.datetime):
    return r.__str__()

# 工單
class Order():
    part_number = ''
    part_name = ''
    start_time = ''
    end_time = ''
    planning_time = ''
    def __init__(self, part_number, part_name, amount, remaining_amount, UPH, start_time, end_time, real_start_time, real_end_time, planning_time, \
                 urgent_tag=False):
        self.part_number = part_number
        self.part_name = part_name
        self.amount = amount
        self.remaining_amount = remaining_amount
        self.UPH = UPH
        self.start_time = start_time
        self.end_time = end_time
        self.real_start_time = real_start_time
        self.real_end_time = real_end_time
        self.planning_time = planning_time
        self.urgent_tag = urgent_tag


# 模具
class Mold():
	def __init__(self, PN, CMDIE_NO, DIE_NO, CT, HOLENUM, STORE_ID):
		self.PN = PN
		self.CMDIE_NO = CMDIE_NO
		self.DIE_NO = DIE_NO
		self.CT = CT
		self.HOLENUM = HOLENUM
		self.STORE_ID = STORE_ID

	def show_mold_information(self):
		print('鴻海料號: ', self.PN)
		print('模號: ', self.CMDIE_NO)
		print('模序: ', self.DIE_NO)
		print('Cycle time: ', self.CT)
		print('UPH: ', self.get_UPH())
		print('儲位: ', self.STORE_ID)

	def get_UPH(self):
		UPH = 3600/float(self.CT)*int(self.HOLENUM)
		return UPH


# 機台
class Machine():
    name = ''
    tons = ''
    color = ''
    status = 1
    order_list = []
    max_usable_time = 24.0
    def __init__(self, name, tons, color, status, order_list, max_usable_time):
        self.name = name
        self.tons = tons
        self.color = color
        self.status = status
        self.order_list = order_list
        self.max_usable_time = max_usable_time

    def get_order_name_list(self):
        result_list = []
        for o in self.order_list:
            result_list.append(o.part_number)
        return result_list

# 線別
class Line():
    total_machine = 10
    normal = 10
    abnormal = 0
    def __init__(self, name, total_machine, normal, abnormal, machine_list):
        self.name = name
        self.total_machine = total_machine
        self.normal = normal
        self.abnormal = abnormal
        self.machine_list = machine_list

    def get_machine(self, number):
        return self.machine_list[number]
    
    def list_machine(self):
        return self.machine_list
    
    def get_ok_machine(self):
        result_list = []
        for m in self.machine_list:
            if m.status == 1:
                result_list.append(m)
            else:
                continue
        return result_list

    def get_ng_machine(self):
        result_list = []
        for m in self.machine_list:
            if m.status == 0:
                result_list.append(m)
            else:
                continue
        return result_list

    def get_machine_by_tons(self, tons, machine_list=[]):
        if machine_list == []:
            machine_list = self.machine_list
        result_list = []
        for m in machine_list:
            if m.tons == tons and m.status == 1:
                result_list.append(m)
            else:
                continue
        return result_list

    def get_machine_by_color(self, color, machine_list=[]):
        if machine_list == []:
            machine_list = self.machine_list
        result_list = []
        
        if color == '透明':
            for m in machine_list:
                if m.color == 'trans' and m.status == 1:
                    result_list.append(m)
                else:
                    continue
            return result_list
            
        elif color == '白色':
            for m in machine_list:
                if m.color == 'white' and m.status == 1:
                    result_list.append(m)
                else:
                    continue
            return result_list
        else:
            for m in machine_list:
                if m.color == 'others' and m.status == 1:
                    result_list.append(m)
                else:
                    continue
            return result_list
           
    def show_machine_name_list(self, machine_list):
        result_list = []
        for m in machine_list:
            result_list.append(m.name)
        print(result_list)
        return
    
    def get_zero_remaining_time(self, machine_list=[]):
        if machine_list == []:
            machine_list = self.machine_list
        result_list = []
        for m in machine_list:
            if m.remaining_time == 0:
                result_list.append(m)
            else:
                continue
        return result_list

        

    def get_biggest_remaining_time(self, machine_list=[]):
        if machine_list == []:
            machine_list = self.machine_list
        record_biggest = machine_list[0]
        for m in machine_list:
            if record_biggest.remaining_time < m.remaining_time:
                record_biggest = m
            else:
                continue
        if record_biggest.remaining_time == 0:
            return None
        return record_biggest

    def show_information(self, machine=None, machine_list=[]):
        if machine:
            m = self.get_machine_by_name(machine)
            if m:
                m.show_machine_information()
                return
            else:
                E = Error_message()
                E.wrong_input_machine_name(machine)
                return
        if machine_list:
            for m_name in machine_list:
                if m:
                    m = self.get_machine_by_name(m_name)
                    m.show_machine_information()
                    print('---------------------------')
                else:
                    E = Error_message()
                    E.wrong_input_machine_name(m_name)
                    return
            return
        for m in self.machine_list:
            m.show_machine_information()
            print('---------------------------')
        return

    def get_machine_by_name(self, name):
        for m in self.machine_list:
            if m.name == name:
                return m
            else:
                continue

# 工廠
class Factory():
    name = ''
    line_list = []
    def __init__(self, name, line_list):
        self.name = name
        self.line_list = line_list

    def get_machine_by_tons(self, tons):
        result_list = []
        for l in self.line_list:
            for m in l.machine_list:
                if m.tons == tons:
                    result_list.append(m)
                else:
                    continue
        return result_list

    def get_machine_by_yesterday_order_amount(self, yesterday_order_amount):
        result_list = []
        for l in self.line_list:
            for m in l.machine_list:
                if m.yesterday_order_amount <= yesterday_order_amount:
                    result_list.append(m)
                else:
                    continue
        return result_list
    
    def get_ok_machine(self):
        result_list = []
        for l in self.line_list:
            for m in l.machine_list:
                if m.status == 1:
                    result_list.append(m)
                else:
                    continue
        return result_list
    
    def get_ng_machine(self):
        result_list = []
        for l in self.line_list:
            for m in l.machine_list:
                if m.status == 0:
                    result_list.append(m)
                else:
                    continue
        return result_list
    
    def show_factory_information(self):
        print('Factory : ', self.name)
        print('Lines : ', self.line_list)
        return

    def show_line_information(self):
        for line in self.line_list:
            line.show_information()
        return
    
    def output_daily_planning(self):
        from setting import dsn_tns
        conn = cx_Oracle.connect(
            user = 'NWEIAI',
            password = 'NWE123456',
            dsn = dsn_tns,
            encoding="UTF-8"
        )
        cursor = conn.cursor()
        # sql = ''' DELETE FROM "arrangement_result" '''
        # cursor.execute(sql)
        # conn.commit()
        

        for line in self.line_list:
            for m in line.machine_list:
                for o in m.order_list:
                    if m.tons == '100T':
                        tons = 100
                    elif m.tons == '130T':
                        tons = 130

                    data = (m.name, tons, str(o.end_time), str(o.start_time), str(o.end_time), float(o.planning_time), o.part_number, 0, float(o.UPH), 'M2', 'M2', 'M2', 'M2', 'M2', o.part_name, o.amount, 1, 'M', 'M', 'M2', 0, 0, 'M2', 4, m.color, 'M2')
                    print(data)
                    sql = '''INSERT INTO "arrangement_result" ("machine_NO", "machine_ton", "mold_down_t", "plan_s_time", "plan_e_time", "plan_work_time", "Part_NO", "machine_CT", "UPH", "mold_edit", "mold_Serial", "mold_NO", "mold_position", "package_size", "product_name", "plan_number", "emergency", "mass_pro", "need", "same_mold_part_NO", "value", "total_value", "plastic_Part_NO", "mold_changeover_time", "plastic_color", "note", "Seq") VALUES (:1, :2, TO_DATE(:3,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:4,'YYYY-MM-DD HH24:MI:SS'), TO_DATE(:5,'YYYY-MM-DD HH24:MI:SS'), :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25, :26, ARRANGEMENT_SEQ.NEXTVAL)'''
                    cursor.execute(sql, data)
                    conn.commit()
        conn.close()

    def to_csv(self, name):
        week = '18'
        result_dic = {}
        tons_list = []
        machine_name_list = []
        start_time_list = []
        end_time_list = []
        part_number_list = []
        part_name_list = []
        amount_list = []
        planning_time_list = []
        for line in self.line_list:
            for m in line.machine_list:
                for o in m.order_list:
                    tons_list.append(m.tons)
                    machine_name_list.append(m.name)
                    start_time_list.append(o.start_time)
                    end_time_list.append(o.end_time)
                    part_number_list.append(o.part_number)
                    part_name_list.append(o.part_name)
                    amount_list.append(o.amount)
                    planning_time_list.append(o.planning_time)
        
        result_dic.update({'噸位':tons_list, '機台號':machine_name_list, '起始時間':start_time_list, '結束時間':end_time_list, \
                           '鴻海料號':part_number_list, '品名':part_name_list, '數量':amount_list, '生產時間':planning_time_list})
        result_df = pd.DataFrame(result_dic)
        result_df.to_csv('./' + name + '.csv', encoding='utf_8_sig', index=False)


# 機台實時狀態
class Real_machine_status(Machine):
    def __init__(self, name, tons, color, status, order_list, max_usable_time, remaining_time, ontime_order, m_start_time, m_end_time):
        super().__init__(name, tons, color, status, order_list, max_usable_time)
        self.remaining_time = remaining_time
        self.ontime_order = ontime_order
        self.m_start_time = m_start_time
        self.m_end_time = m_end_time

    def update_order_status(self, order_list, finished_amount_list):
        keep_end_time = None
        for i, o in enumerate(order_list):
            remaining_amount = o.amount - finished_amount_list[i]
            remaining_time_needed = round(remaining_amount/o.UPH, 2)
            remaining_hour_needed = int(str(remaining_time_needed).split('.')[0])
            remaining_minute_needed = (int(str(remaining_time_needed).split('.')[1])/100)*60
            real_end_time = datetime.datetime.now() + datetime.timedelta(hours=remaining_hour_needed, minutes=remaining_minute_needed)
            if keep_end_time:
                o.real_start_time = keep_end_time
            o.real_end_time = real_end_time
            o.remaining_amount = remaining_amount
        return
    
    def show_machine_information(self):
        print('machine name : ', self.name)
        print('tons : ', self.tons)
        print('color : ', self.color)
        if self.status == 1: 
            print('status : ', 'normal') 
        else: 
            print('status : ', 'abnormal')
        print('order : ', self.get_order_name_list())
        print('remaining time : ', self.remaining_time)
        return
   
    def get_delayed_order(self):
        result_list = []
        for o in self.order_list:
            if o.real_end_time > self.order_list[-1].end_time:
                result_list.append(o)
            else:
                continue
        return result_list

    


# 錯誤訊息
class Error_message():
    def __init__(self):
        pass
    
    def wrong_input_machine_name(self, machine):
        print('The machine name : ' + machine + ' is wrong. Please ensure to input the whole name. Ex: A01透明')
        return
