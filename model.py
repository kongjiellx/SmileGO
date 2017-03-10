import theano.sandbox.cuda
theano.sandbox.cuda.use("gpu1")
import keras

from keras.models import Model
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
import controler
class model(object):
    def __init__(self):
        pass

    # (samples, rows, cols, channels)
    def bulid_model(self):
        x = Input(shape=(19, 19, 3), dtype='float32', name='x')
        x2 = Input(shape=(2,), dtype='float32', name='x2')
        conv1 = Convolution2D(nb_filter=256, nb_row=5, nb_col=5, activation='relu', input_shape=(19, 19, 3))(x)
        bn1 = BatchNormalization()(conv1)
        pool1 = MaxPooling2D(pool_size=(2, 2), strides=(1, 1))(bn1)

        conv2 = Convolution2D(nb_filter=128, nb_row=3, nb_col=3, activation='relu')(pool1)
        bn2 = BatchNormalization()(conv2)
        pool2 = MaxPooling2D(pool_size=(2, 2), strides=(1, 1))(bn2)

        conv3 = Convolution2D(nb_filter=128, nb_row=3, nb_col=3, activation='relu')(pool2)
        bn3 = BatchNormalization()(conv3)
        pool3 = MaxPooling2D(pool_size=(2, 2), strides=(1, 1))(bn3)

        conv4 = Convolution2D(nb_filter=128, nb_row=3, nb_col=3, activation='relu')(pool3)
        bn4 = BatchNormalization()(conv4)
        pool4 = MaxPooling2D(pool_size=(2, 2), strides=(1, 1))(bn4)

        conv5 = Convolution2D(nb_filter=128, nb_row=3, nb_col=3, activation='relu')(pool4)
        bn5 = BatchNormalization()(conv5)
        pool5 = MaxPooling2D(pool_size=(3, 3), strides=(1, 1))(bn5)

        cnn_out = Flatten()(pool5)
        merge1 = merge([cnn_out, x2], mode='concat', concat_axis=1)

        out = Dense(output_dim=361, init="he_normal", activation="softmax", name='out')(merge1)
        self.model = Model(input=[x, x2], output=out)

    def train(self):
        ctrl = controler.controler()
        train_x, train_x2, train_y = ctrl.pre_x_y()

        self.model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
        self.model.fit({'x': train_x, 'x2': train_x2}, {'out': train_y},
                  batch_size=32,
                  nb_epoch=10,
                  shuffle=True,
                  verbose=1)


