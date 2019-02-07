import pandas as pd
import os
import re
from warning_module import warning

class WeightInvalidError(Exception):
    def __init__(self):
        super().__init__(self)
        self.errorinfo='Weight Invalid'
    def __str__(self):
        return self.errorinfo

def calc(tolerence = 3):
    totalfac = 0
    scoredf = pd.read_excel('grade.xlsx')
    midweight = int(re.findall('(\d+)',scoredf.columns[0])[0])/100
    finalweight = int(re.findall('(\d+)',scoredf.columns[0])[0])/100
    if midweight + finalweight >= 100:
        raise WeightInvalidError
    else:
        usualweight = 1 - midweight - finalweight
    presencedf = warning(tolerence)[0]
    presencedf.index = list(map(int,presencedf.index))
    scoredf['平时分'] = presencedf.score
    scoredf['final'] = scoredf.iloc[:,0]*midweight+scoredf.iloc[:,1]*finalweight+scoredf.iloc[:,2]*usualweight
    scoredf.to_excel('grade.xlsx',index=False)


if __name__ == '__main__':
    calc()