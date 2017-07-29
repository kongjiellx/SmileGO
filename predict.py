from keras.preprocessing import sequence
from keras.models import Sequential, model_from_json
from keras import backend as K
from keras.utils import np_utils
import cPickle as cp
import numpy as np
import math
import json

def predict(model, x):
    # print('Predicting...')
    pred = model.predict({'x': np.reshape(x, (1, 19 ,19 ,12))}, batch_size=1, verbose=2)

    # print(time_pred)
    pred = np.random.choice(361, 1, p=pred[0])
    pred = pred[0]
    # point = (point[0] / 19, point[0] % 19)
    # pred = np.argmax(pred)
    point = (pred / 19, pred % 19)
    # print point
    return point

def random_point():
    point = np.random.randint(0, 360)
    return (point / 19, point % 19)

def load_model():
    ### load model
    print('Loading model...')
    fp = open('model.json')
    model = model_from_json(fp.readline().strip())
    model.load_weights('best.model')
    fp.close()

    print('Compile...')
    model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
    return model


