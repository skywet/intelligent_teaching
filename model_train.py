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
from load_data import load_data
import numpy as np
import os
from playsound import playsound

def construct_model(people):
    '''
    模型创建用函数，模型的构建参考Alexnet的结构,模型的构成如下：
    
    '''
    model = Sequential()
    model.add(Convolution2D(32,(2,2),strides=1,padding='same',input_shape=(56,56,3),data_format='channels_last'))
    model.add(MaxPooling2D(pool_size=2,strides=2,padding='same'))
    model.add(Dropout(0.01))
    model.add(Convolution2D(64, 5, strides=1, padding='same', data_format='channels_first'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(2, 2, 'same', data_format='channels_first'))
    model.add(Dropout(0.1))
    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Dropout(0.2))
    model.add(Activation('relu'))
    model.add(Dense(people))
    model.add(Dropout(0.01))
    model.add(Activation('softmax'))
    opt = keras.optimizers.adam(lr=0.0001)
    model.compile(optimizer=opt,loss='categorical_crossentropy',metrics=['accuracy'])
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
    datagen = ImageDataGenerator(
        featurewise_center=False,
        samplewise_center=False,
        featurewise_std_normalization=False,
        samplewise_std_normalization=False,
        zca_whitening=False,
        rotation_range=180,
        width_shift_range=1, 
        height_shift_range=1,
        horizontal_flip=True,
        vertical_flip=True)
    datagen.fit(x_train)
    tb = TensorBoard(log_dir='./logs',write_graph=True,write_images=True)
    model = construct_model(classes)
    model.fit_generator(generator=datagen.flow(x_train,y_train,batch_size=1),steps_per_epoch=1,epochs=100,callbacks=[tb])
    playsound('alert/tc.mp3')
    # 保存模型
    model.save('face-model.h5')
    