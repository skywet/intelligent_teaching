import pandas as pd
import matplotlib.pyplot as plt
import os
from time import strptime
import matplotlib.pyplot as plt


def data_process():
    '''
    用于处理获得的出勤数据
    '''
    dirs = os.listdir('../presence/')
    people = len(pd.read_excel('../presence/id.xlsx').ID)
    for file in dirs:
        if 'id' not in file and 'plot' not in file:
            loc = '../presence/'+file
            present = len(pd.read_csv(loc).name)
            absent = people - present
            fig = plt.figure()
            ax1 = fig.add_subplot(111)
            ax1.set_title(file[:-4])
            labels = {'../presence':str(present),'absent':str(absent)}
            explode = [0,0.5]
            ax1.pie([present,absent],labels=labels,colors=['#ee0000','#66ccff'],explode=explode,shadow=True)
            plt.savefig('../presence/plot/{}.jpg'.format(file[:-4]))
        
def catergorize_file(lst):
    '''
    将得到的数据按日期分类
    '''
    newlst = []
    histlst = []
    for item in lst:
        if item[-4:] == '.csv':
            date = item[:8]
            histlst.append(date)
    histlst = list(set(histlst))
    for item in lst:
        sublst = []
        for subitem in histlst:
            if item[:8] == subitem and item[-4:] == '.csv':
                sublst.append(item)
        if sublst != []:
            newlst.append(sublst)
    return histlst,newlst

def student_../presence_process(ID):
    '''
    生成csv/画图
    '''
    dirs = os.listdir('../presence/')
    dir_date, dir_c = catergorize_file(dirs)
    student_../presence_df = pd.DataFrame(columns=['count'])
    for filelst in dir_c:
        count = 0
        for file in filelst:
            dct = pd.read_csv('../presence/{}'.format(file)).to_dict().values()
            if {0:ID} in dct:
                count += 1
        student_../presence_df.loc[file[:8]] = count
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus']=False
    student_../presence_df.plot(kind='bar')
    student_../presence_df.to_csv('../presence/student_data/{}.csv'.format(ID))
    plt.xlabel('日期')
    plt.title('{}的出勤率-日期报告'.format(ID))
    plt.savefig('../presence/student_plot/{}.png'.format(ID))
    plt.close('all')
            
def process_that():
    peopleser = pd.read_excel('../presence/id.xlsx').ID
    for ID in peopleser:
        student_../presence_process(ID)

def process_whole_class():
    peopleser = pd.read_excel('../presence/id.xlsx').ID
    dir_date, dir_c = catergorize_file(os.listdir('../presence/'))
    df = pd.DataFrame(columns=['freq'])
    for filelst in dir_c:
        count = 0
        for file in filelst:
            dct = pd.read_csv('../presence/{}'.format(file))
            count += dct.shape[0]
        df.loc[file[:8]] = count
    df.to_csv('../presence/whole_class/whole-class.csv')


if __name__ == '__main__':
    process_whole_class()