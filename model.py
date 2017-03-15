import theano.sandbox.cuda
theano.sandbox.cuda.use("gpu0")
import keras

from keras.models import Model, model_from_json
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import backend as K

from keras.layers import (
    Input,
    Activation,
    merge,
    Dense,
    Flatten,
    Dropout
)
from keras.layers.convolutional import (
    Convolution2D,
    MaxPooling2D,
)
from keras.layers.normalization import BatchNormalization

from keras.utils import np_utils, generic_utils
from controler import *
class model(object):
    def __init__(self):
        pass

    # (samples, rows, cols, channels)
    def bulid_model(self):
        x = Input(shape=(19, 19, 4), dtype='float32', name='x')
        x2 = Input(shape=(2,), dtype='float32', name='x2')
        conv1 = Convolution2D(nb_filter=64, nb_row=5, nb_col=5, activation='relu', input_shape=(19, 19, 4))(x)
        bn1 = BatchNormalization()(conv1)

        conv2 = Convolution2D(nb_filter=64, nb_row=3, nb_col=3, activation='relu')(bn1)
        bn2 = BatchNormalization()(conv2)

        conv3 = Convolution2D(nb_filter=64, nb_row=3, nb_col=3, activation='relu')(bn2)
        bn3 = BatchNormalization()(conv3)

        cnn_out = Flatten()(bn3)
        merge1 = merge([cnn_out, x2], mode='concat', concat_axis=1)

        out = Dense(output_dim=361, init="he_normal", activation="softmax", name='out')(merge1)
        self.model = Model(input=[x, x2], output=out)

    def train(self):
        checkpointer = ModelCheckpoint(filepath='./best.model',
                                       verbose=1,
                                       monitor='val_loss',
                                       save_best_only=True)
        earlystop = EarlyStopping(monitor='val_loss',
                                  patience=10,
                                  verbose=1,
                                  mode='auto')

        self.model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
        json_model = self.model.to_json()
        fjson = open('model.json', 'w')
        fjson.write(json_model)
        fjson.close()
        print 'model_json_saved!'
        train_x, train_x2, train_y = pre_x_y(path='kgs-19-2011/')
        valid_x, valid_x2, valid_y = pre_x_y(path='kgs-19-2017-01-new/')
        print 'train_data_len: ', len(train_x)
        print 'valid_data_len: ', len(valid_x)
        self.model.fit({'x': train_x, 'x2': train_x2}, {'out': train_y},
                  batch_size=32,
                  nb_epoch=100,
                  shuffle=True,
                  verbose=1,
                  callbacks=[checkpointer, earlystop],
                  validation_data=({'x': valid_x, 'x2': valid_x2}, {'out': valid_y}))

    def test(self):
        x, x2, y = pre_x_y(path='kgs-19-2017-01-new/')

        print('Loading model...')
        fp = open('model.json')
        model = model_from_json(fp.readline().strip())
        model.load_weights('best.model')
        fp.close()
        print('Compile...')
        model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
        pred = model.predict({'x': x, 'x2': x2}, batch_size=32, verbose=1)
        for pre in pred:
            print pre.argmax()


