import keras
from keras.models import load_model
import cv2
from detect_split import detect,init_cascader
from model_train import load
import numpy as np
import pandas as pd
from time import strftime
from aip import AipSpeech
from playsound import playsound
import os

def draw_rec(img,a,b,c,d):
    '''
    在图片上绘制长方形使用的函数
    '''
    cv2.rectangle(img, (a - 50, b - 50), (c + 50, d + 50),(0,0,238), 2)

def tts(st):
    '''
    调用百度语音合成接口为应用提供语音提示
    '''
    APP_ID = '15366913'
    API_KEY = 'VF7Tri9k6Gyqkw8t5s7zAAGr'
    SECRET_KEY = 'LyjBHhpHpevoXqQy3FOmsrGCg7Mt8jKI'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result  = client.synthesis(st, 'zh', 1, {
    'vol': 5,
    })
    if not isinstance(result,dict):
        with open('audio.mp3','wb') as f:
            f.write(result)
    playsound('audio.mp3')
    os.remove('audio.mp3')
    return 0

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
presence_df = pd.DataFrame(columns=['sid','name','time'])
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
            draw_rec(img,a,b,c,d)
            cv2.putText(img, str(sid), (a, d), font, 0.55, (255, 204, 102), 1)
            if sid not in presence_df.sid:
                presence_df.loc[-1] = [sid,ser[int(sid)],strftime('%Y-%m-%d %H:%M:%S')]
                name = ser[int(sid)]
                presence_df.to_csv(filename)
    except:
        print('Something wrong!')
    finally:
        cv2.imshow('Press "Q" to exit', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
print(presence_df)


