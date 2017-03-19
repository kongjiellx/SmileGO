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
<<<<<<< HEAD
    pred = model.predict({'x': np.reshape(x, (1, 19 ,19 ,12))}, batch_size=1, verbose=2)
=======
    pred = model.predict({'x': np.reshape(x, (1, 19, 19, 12))}, batch_size=1, verbose=2)
>>>>>>> a6dc7bd1d6b12a09f744649ed31d653028ff2e0a
    # print(time_pred)
    # point = np.random.choice(361, 1, p=pred[0])
    # point = (point[0] / 19 + 1, point[0] % 19 + 1)
    pred = np.argmax(pred)
    point = (pred / 19 + 1, pred % 19 + 1)
    print point
    return point

def random_point():
    point = np.random.randint(0, 360)
    return (point / 19 + 1, point % 19 + 1)

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


