import random
import pandas as pd

def rand_sample(num):
    '''
    提供GUI使用的取样函数
    '''
    df = pd.read_excel('presence/id.xlsx')
    ser = list(df.ID)
    samplst = random.sample(ser,num)
    samplst = map(str, samplst)
    return ' '.join(samplst)

def load_y():
    '''
    加载ID
    '''
    df = pd.read_excel('presence/id.xlsx')
    ser = list(df.ID)
    ser = list(map(str,ser))
    return ser

if __name__ == '__main__':
    print(rand_sample(10))