from keras.preprocessing import sequence
from keras.models import Sequential, model_from_json
from keras import backend as K
from keras.utils import np_utils
import cPickle as cp
import numpy as np
import math
import json

def predict(model, x, x2):
    # print('Predicting...')
    pred = model.predict({'x': x, 'x2': x2}, batch_size=1,verbose=2)
    # print(time_pred)
    point = np.random.choice(361, 1, p=pred[0])
    point = (point[0] / 19 + 1, point[0] % 19 + 1)
    print point
    return point



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

