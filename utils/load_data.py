'''
author:Skymos Wu
reference:
version:0.4
'''
import os
import cv2
import numpy as np

def load_x(loc):
    '''
    加载图像数据用的工具函数
    '''
    dirs = os.listdir(loc)
    os.chdir(loc)
    x = []
    for subdir in dirs:
        os.chdir(subdir)
        for imgfile in os.listdir():
            img = cv2.imread(imgfile)
            img = cv2.resize(img,(56,56))
            x.append(img)
        os.chdir('../')
    os.chdir('../')
    return np.array(x)

def load_y(loc):
    '''
    加载标签数据使用的工具函数
    '''
    os.chdir(loc)
    y = []
    for subdir in os.listdir():
        os.chdir(subdir)
        indv = len(os.listdir())
        y.extend([subdir]*indv)
        os.chdir('../')
    os.chdir('../')
    return np.array(y)

def load_data(loc):
    '''
    加载整合数据使用的工具函数
    '''
    x = load_x(loc)
    y = load_y(loc)
    p = np.random.permutation(range(len(x)))
    x,y = x[p],y[p]
    print('Data loaded, shape of x is {}, shape of y is {}.'.format(x.shape,y.shape))
    return x,y,len(os.listdir(loc))

if __name__ == '__main__':
    print(load_y('face-data'))
