import tensorflow as tf
import controler

class model(object):
    def __init__(self):
        pass

    def weight_variable(self, shape):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)

    def bias_variable(self, shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)

    def bulid_model(self):
        x = tf.placeholder(tf.float32, name='x')
        x2 = tf.placeholder(tf.float32, name='x2')
        y = tf.placeholder(tf.float32, name='y')

        conv1_input = tf.reshape(x, (-1, 19, 19, 1))
        W_conv1 = self.weight_variable(shape=(5, 5, 1, 32))
        b_conv1 = self.bias_variable(shape=(32,))
        conv1_out = tf.nn.conv2d(conv1_input, W_conv1, strides=(1, 1, 1, 1), padding='VALID') + b_conv1
        pool1_out = tf.nn.relu(tf.nn.max_pool(conv1_out, ksize=(1, 2, 2, 1), strides=(1, 1, 1, 1), padding='VALID'))

        W_conv2 = self.weight_variable(shape=(3, 3, 32, 64))
        b_conv2 = self.bias_variable(shape=(64,))
        conv2_out = tf.nn.conv2d(pool1_out, W_conv2, strides=(1, 1, 1, 1), padding='VALID') + b_conv2
        pool2_out = tf.nn.relu(tf.nn.max_pool(conv2_out, ksize=(1, 2, 2, 1), strides=(1, 1, 1, 1), padding='VALID'))

        W_conv3 = self.weight_variable(shape=(3, 3, 64, 128))
        b_conv3 = self.bias_variable(shape=(128,))
        conv3_out = tf.nn.conv2d(pool2_out, W_conv3, strides=(1, 1, 1, 1), padding='VALID') + b_conv3
        pool3_out = tf.nn.relu(tf.nn.max_pool(conv3_out, ksize=(1, 9, 9, 1), strides=(1, 1, 1, 1), padding='VALID'))

        cnn_out = tf.reshape(pool3_out, shape=(-1, 128))
        merge = tf.concat([cnn_out, tf.expand_dims(x2, 1)], axis=1)

        W_fc1 = self.weight_variable((128 + 1, 128))
        b_fc1 = self.bias_variable((128,))
        hidden = tf.matmul(merge, W_fc1) + b_fc1

        W_fc2 = self.weight_variable((128, 361))
        b_fc2 = self.bias_variable((361,))
        out = tf.nn.softmax(tf.matmul(hidden, W_fc2) + b_fc2)

        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=out))
        train_step = tf.train.AdadeltaOptimizer().minimize(cross_entropy)
        correct_prediction = tf.equal(tf.arg_max(out, dimension=1), tf.arg_max(y, dimension=1))
        acc = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        sess = tf.Session()
        sess.run(tf.global_variables_initializer())

        ctrl= controler.controler()
        ctrl.pre_x_y()
        for i in range(20000):
            batch = ctrl.get_batch(32)
            if i % 100 == 0:
                train_accuracy = acc.eval(session=sess, feed_dict={
                    x: batch[0], x2: batch[1], y: batch[2]})
                print("step %d, training accuracy %g" % (i, train_accuracy))
            train_step.run(session=sess, feed_dict={x: batch[0], x2: batch[1], y: batch[2]})


