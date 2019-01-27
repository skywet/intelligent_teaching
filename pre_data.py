import pandas as pd
import matplotlib.pyplot as plt
import os


def data_process():
    dirs = os.listdir('presence/')
    people = len(pd.read_excel('presence/id.xlsx').ID)
    for file in dirs:
        if 'id' not in file and 'plot' not in file:
            loc = 'presence/'+file
            present = len(pd.read_csv(loc).name)
            absent = people - present
            fig = plt.figure()
            ax1 = fig.add_subplot(111)
            ax1.set_title(file[:-4])
            labels = {'presence':str(present),'absent':str(absent)}
            explode = [0,0.5]
            ax1.pie([present,absent],labels=labels,colors=['#ee0000','#66ccff'],explode=explode,shadow=True)
            plt.savefig('presence/plot/{}.jpg'.format(file[:-4]))
        

if __name__ == '__main__':
    data_process()