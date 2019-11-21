import os
import tensorflow as tf
import argparse
import io
import numpy as np

size = 2383
basePath = "/Users/shanwang/Desktop/data/xia/use/"
big = "big/"
middle = "middle/"
small = "small/"
train = "train/"
test = "test/"

trainPath = basePath + train
testPath = basePath + test

pathList = []
labelList = []

paramsLen = 3968 * 2976

def getAllPath(path , label):
    for file in os.listdir(path):
        if not file.endswith(".jpg"):
            print(path + file)
            continue
        pathList.append(path + file)
        labelList.append(label)


def getAllPathLabel(path):
    for file in os.listdir(path):
        if not file.endswith(".jpeg"):
            print(path + file)
            continue
        pathList.append(path + file)
        labels = file.split('_')
        labelList.append(int(labels[0]))

def loadImg(path_queue):
    reader = tf.WholeFileReader()
    key , value = reader.read(path_queue)
    img = tf.image.convert_image_dtype(tf.image.decode_jpeg(value , channels=3) , dtype=tf.float32)
    img = tf.image.resize_images(img , size=(size,size))
    return img

def sliceReadImage(path_queue):
    file_contents = tf.read_file(path_queue[0])
    img = tf.image.convert_image_dtype(tf.image.decode_jpeg(file_contents , channels=3) , dtype=tf.float32)
    img = tf.image.resize_images(img , size=(size,size))
    return img



def init():
    parse = argparse.ArgumentParser()
    parse.add_argument('-t', '--trainPath', type=str, default='', help='train path')
    parse.add_argument('-l', '--logPath', type=str, default='', help='log path')
    parse.add_argument('-b', '--batchSize', type=int, default=50, help='train batch size')
    parse.add_argument('-m', '--maxSteps', type=int, default=30, help='train max step')
    parse.add_argument('-r', '--learningRate', type=float, default=0.01, help=' learning rate')
    args = parse.parse_args()
    return args


def weight_variable(shape):
    initial = tf.truncated_normal(shape , stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1 , shape=shape)
    return tf.Variable(initial)


def conv_layer(bottom ,w_conv, b_conv ,name):
    with tf.variable_scope(name) as scope:
        conv = tf.nn.conv2d(bottom , w_conv ,strides=[1,1,1,1] , padding='SAME')
        bias = tf.nn.bias_add(conv , b_conv)
        relu = tf.nn.relu(bias)
        return relu

def max_pool(bias, name):
    with tf.variable_scope(name) as scope:
        pool = tf.nn.max_pool(bias , ksize=[1,2,2,1],strides=[1,2,2,1] , padding='SAME')
        return pool

def fc_layer(bottom , resLen ,name):
    with tf.variable_scope(name) as scope:
        shape = bottom.get_shape().as_list()
        dim = 1
        for d in shape[1:]:
            dim*= d
        x = tf.reshape(bottom , [-1,dim])
        w = weight_variable([dim , resLen])
        b = bias_variable([resLen])
        fc = tf.nn.bias_add(tf.matmul(x,w), b)
        return fc

def drop_out(name):
    pass

def loss(logits, labels_placeholder):
    cross_entropy = -tf.reduce_sum(labels_placeholder*tf.math.log(logits))
    return cross_entropy

def training(loss):
    train_step = tf.compat.v1.train.GradientDescentOptimizer(0.01).minimize(loss,name='aaa')
    return train_step

def inference(img):
    print(img.get_shape().as_list())
    relu1_1 = conv_layer(img ,weight_variable([5,5,3,32]) ,bias_variable([32]), "conv1_1")
    relu1_2 = conv_layer(relu1_1 ,weight_variable([5,5,32,32]) ,bias_variable([32]),  "conv1_2")
    pool_1 = max_pool(relu1_2 , "pool_1")

    relu2_1 = conv_layer(pool_1 ,weight_variable([5,5,32,32]) ,bias_variable([32]),  "conv2_1")
    relu2_2 = conv_layer(relu2_1 , weight_variable([5,5,32,32]) ,bias_variable([32]), "conv2_2")
    pool_2 = max_pool(relu2_2 ,  "pool_2")

    relu3_1 = conv_layer(pool_2 , weight_variable([5,5,32,32]) ,bias_variable([32]), "conv3_1")
    relu3_2 = conv_layer(relu3_1 , weight_variable([5,5,32,32]) ,bias_variable([32]), "conv3_2")
    relu3_3 = conv_layer(relu3_2 , weight_variable([5,5,32,32]) ,bias_variable([32]), "conv3_3")
    pool_3 = max_pool(relu3_3 , "pool_3")

    relu4_1 = conv_layer(pool_3 ,weight_variable([5,5,32,32]) ,bias_variable([32]),  "conv4_1")
    relu4_2 = conv_layer(relu4_1 , weight_variable([5,5,32,32]) ,bias_variable([32]), "conv4_2")
    relu4_3 = conv_layer(relu4_2 , weight_variable([5,5,32,32]) ,bias_variable([32]), "conv4_3")
    pool_4 = max_pool(relu4_3 , "pool_4")

    relu5_1 = conv_layer(pool_4 , weight_variable([5,5,32,32]) ,bias_variable([32]), "conv5_1")
    relu5_2 = conv_layer(relu5_1 , weight_variable([5,5,32,32]) ,bias_variable([32]), "conv5_2")
    relu5_3 = conv_layer(relu5_2 , weight_variable([5,5,32,32]) ,bias_variable([32]), "conv5_3")
    pool_5 = max_pool(relu5_3 , "pool_5")

    fc6 = fc_layer(pool_5 ,4000, "fc_6")
    relu_6 = tf.nn.relu(fc6)
    relu_6 = tf.nn.dropout(relu_6 , 0.5)
    fc7 = fc_layer(relu_6 , 2000,"fc_7")
    relu_7 = tf.nn.relu(fc7)
    relu_7 = tf.nn.dropout(relu_7 , 0.5)
    fc8 = fc_layer(relu_7 ,3, "fc_8")
    resOp = tf.nn.softmax(fc8 , name="prob")
    return resOp

def getBatchTrain():

    getAllPathLabel(trainPath + 'qiege/')
    imgString = tf.convert_to_tensor(pathList , dtype=tf.string)
    labelString = tf.convert_to_tensor(labelList , dtype=tf.int32)

    imgQueue = tf.train.slice_input_producer([imgString , labelString],shuffle=True , num_epochs= 2)
    labelQueue = imgQueue[1]
    img = sliceReadImage(imgQueue)
    labels = tf.one_hot(labelQueue , 3)

    x , y_ = tf.train.batch([img , labels] , batch_size=30)
    return x , y_

def main():

    img , label = getBatchTrain()
    logits = inference(img)
    lossOp = loss(logits , label)
    trainOp = training(lossOp)

    localInit = tf.compat.v1.local_variables_initializer()
    globalInit = tf.compat.v1.global_variables_initializer()

    tf.summary.scalar("loss",lossOp)
    # for item in tf.trainable_variables():
    #     tf.summary.histogram(item.name , item)

    summary_op = tf.summary.merge_all()

    with tf.compat.v1.Session() as sess:
        sess.run(localInit)
        sess.run(globalInit)
        log_write = tf.summary.FileWriter("/Users/shanwang/Desktop/data/study/test/log" , sess.graph)
        coorid = tf.train.Coordinator()
        thread = tf.train.start_queue_runners(sess = sess , coord=coorid)
        try:
            while not coorid.should_stop():
                imgs , summary= sess.run([trainOp,summary_op])
                log_write.add_summary(summary)
                correct_prediction = tf.equal(tf.argmax(logits , 1) , tf.argmax(label , 1))
                accuracy = tf.reduce_mean(tf.cast(correct_prediction , tf.float32))
                print(sess.run(accuracy ))


        except tf.errors.OutOfRangeError:
            print("done")
        finally:
            coorid.request_stop()

        coorid.join(thread)




if __name__ == '__main__':
    args = init()
    main()
    # tf.compat.v1.app.run(main=main, argv=[sys.argv[0]] + unparsed)