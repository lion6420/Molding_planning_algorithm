import pandas as pd
import numpy as np
import os

plenty_chambers_dic = {
}


class Identification():
    def __init__(self):
        pass

    def to_same_length(self, s1, s2):
        if len(s1) == len(s2):
            return s1, s2
        elif len(s1) > len(s2):
            return self.to_same_length(s1[0:-1], s2)
        else:
            return self.to_same_length(s1, s2[0:-1])

    def same_mold(self, p1, p2):
        p1, p2 = self.to_same_length(p1, p2)
        p1_ = p1.split('-')
        p2_ = p2.split('-')

        if len(p1_) != len(p2_): # type 1 Ex: '1B41DKB20-01E' and '1B41DKB20P01E'
            count_diff = 0
            for i in range(len(p1)):
                if p1[i] != p2[i]:
                    count_diff+=1
                if count_diff >= 2:
                    return False
            return True
        elif len(p1_) == 3 and len(p2_) == 3: # type 2 Ex: '700-105500-01WA' and '700-105500-01PWA'
            if p1_[0] == p2_[0] and p1_[1] == p2_[1] and p1_[2][0:2] == p2_[2][0:2]: # Ex: '700' == '700' and '105500' == '105500'
                    return True
            else:
                return False
        else:
            return False
    
    def plenty_chambers(self):
        pass