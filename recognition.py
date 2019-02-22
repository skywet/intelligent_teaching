import keras
from keras.models import load_model
import cv2
from detect_split import detect,init_cascader
from model_train import load
import numpy as np
import pandas as pd
from time import strftime
import os

def draw_rec(img,a,b,c,d):
    '''
    在图片上绘制长方形使用的函数
    '''
    cv2.rectangle(img, (a - 50, b - 50), (c + 50, d + 50),(0,0,238), 2)

# 加载模型
model = load_model('face-model.h5')
font = cv2.FONT_HERSHEY_SIMPLEX
cam = cv2.VideoCapture(0)
# 加载独热编码解码字典
dct = load()[-1]
dct_b = {}
for key,value in dct.items():
    dct_b[value] = key
# 读取姓名学号数据
df = pd.read_excel('presence\id.xlsx')
df.index = df.ID
df.drop('ID',axis=1,inplace=True)
ser = df.name
# 创建出勤率记录文件
presence_df = pd.DataFrame(columns=['name','time'])
filename = 'presence\{}.csv'.format(strftime('%Y%m%d_%H%M'))
presence_df.to_csv(filename)

while True:
    # 启动摄像头进行读取
    _,img = cam.read()
    init_cascader()
    try:
        a,b,c,d = face_reg = detect(img)[0]
        if face_reg != ():
            face = img[b:d,a:c]
            mask = cv2.resize(face,(56,56))
            mask = mask.reshape(1,56,56,3).astype('float32')/255
            label = model.predict(mask)
            sid = dct_b[np.argmax(label)]
            time = strftime('%Y-%m-%d %H:%M:%S')
            draw_rec(img,a,b,c,d)
            cv2.putText(img, str(sid), (a, d), font, 0.55, (255, 204, 102), 1)
            if int(sid) not in presence_df.index:
                presence_df.loc[int(sid)] = {'name':ser[int(sid)], 'time':time}
                name = ser[int(sid)]
                presence_df.to_csv(filename)
    except IndexError:
        print('No face detected!')
    finally:
        cv2.imshow('Press "Q" to exit', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
print(presence_df)


