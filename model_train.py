'''
author:Skymos Wu
version:0.5
'''
# 加载keras库
import keras
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense,Activation,Convolution2D,Dropout,MaxPooling2D,Flatten
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import TensorBoard
# 加载数据处理用库
from utils.load_data import load_data
import numpy as np
import os
from playsound import playsound

def construct_model(people,nb_filters1=32,nb_filters2=64,nb_pool=2,nb_conv=3):
    '''
    模型创建用函数，模型的构建参考Alexnet的结构,模型的构成如下：
    
    '''
    model = Sequential()
    model.add(Convolution2D(nb_filters1, (nb_conv, nb_conv),border_mode='valid',input_shape=(56,56,3),data_format='channels_last'))
    model.add(Activation('tanh'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))

    model.add(Convolution2D(nb_filters2, (nb_conv, nb_conv)))
    model.add(Activation('tanh'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(1000)) #Full connection
    model.add(Activation('tanh'))
    model.add(Dropout(0.5))
    model.add(Dense(people))
    model.add(Activation('softmax'))
    model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
    print('Model construction complete.')
    playsound('alert/nncomplete.mp3')
    return model

def load():
    '''
    加载数据和标准化数据用工具函数
    '''
    (x_train,y_train,classes) = load_data('face-data')
    x_train = x_train / 255
    y_use = list(np.arange(0,classes))
    tempst = sorted(list(set(y_train)))
    dct = dict(zip(tempst,y_use))
    y_fit = []
    for i in y_train:
        y_fit.append(dct[i])
    y_fit = np.array(y_fit)
    y_fit = np_utils.to_categorical(y_fit,num_classes=classes)
    return x_train,y_fit,classes,dct

if __name__ == '__main__':
    x_train,y_train,classes,dct = load()
    # 使用ImageDataGenerator生成噪声数据，提高模型的泛用性
    tb = TensorBoard(log_dir='./logs',write_graph=True,write_images=True)
    model = construct_model(classes)
    model.fit(x_train,y_train,epochs=2000,callbacks=[tb])
    playsound('alert/tc.mp3')
    # 保存模型
    model.save('face-model.h5')
    
