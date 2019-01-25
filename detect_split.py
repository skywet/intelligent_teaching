'''
author:Skymos Wu
reference:python-opencv official documentation,opencv official doc
version:0.2
'''
import numpy as numpy
import cv2
import os

def init_cascader():
    global face_cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def detect(img):
    '''
    使用opencv自带的人脸分拣器提取人脸位置数据，资料存储于haarcascade_frontalface_default.xml中
    '''
    init_cascader()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.1,1)
    region = []
    for (x,y,width,height) in faces:
        region.append((x,y,x+width,y+height))
    return region

def split(img,reg):
    '''
    把人脸部分提取出来并单独切分减少运算量
    '''
    a,b,c,d = reg[0]
    splited = img[b:d,a:c]
    return splited

if __name__ == '__main__':
    init_cascader()
    source = r'face-data'
    dirs = os.listdir(source)
    # 对目录下所有文件进行切分操作，无法识别出面部的图片删除
    for d in dirs:
        for file in os.listdir(source+'\\'+d):
            os.chdir(source+'\\'+d)
            try:
                img = cv2.imread(file)
                reg = detect(img)
                face = split(img,reg)
                cv2.imwrite(file,face)
            except:
                os.remove(file)
            finally:
                os.chdir('../../')