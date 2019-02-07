# coding = utf-8

import pandas as pd
import os
import glob

def warning(tolerence = 3):
    df = pd.DataFrame(columns=['count','sumclass','score'])
    filelst = os.listdir('./presence/student_data')
    filelst = list(filter(lambda x : x[-3:] == 'csv',filelst))
    sumclass = int(len(glob.glob('./presence/*.csv')))
    for file in filelst:
        tempdf = pd.read_csv('./presence/student_data/{}'.format(file))
        stu_id = file[:-4]
        count = tempdf.iloc[:,-1].sum()
        if sumclass - int(count) >= tolerence:
            df.loc[int(stu_id)] = {'count':count,'sumclass':sumclass,'score':0}
        else:
            df.loc[int(stu_id)] = {'count':count,'sumclass':sumclass,'score':count/sumclass*100}
    warn = df[df.sumclass - df.iloc[0] == 1]
    return df,list(warn.iloc[:,-1])

        
if __name__ == '__main__':
    print(warning())