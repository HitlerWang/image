import os
import tensorflow as tf
import numpy as np
import tensorflow_study.input_data as id


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


def loadImg(path_queue):
    reader = tf.WholeFileReader()
    key , value = reader.read(path_queue)
    img = tf.image.convert_image_dtype(tf.image.decode_jpeg(value , channels=1) , dtype=tf.float32)
    img = tf.image.resize_images(img , size=(paramsLen,1))
    img = tf.reshape(img , (-1,paramsLen))
    return img[0]

def sliceReadImage(path_queue):
    file_contents = tf.read_file(path_queue[0])
    img = tf.image.convert_image_dtype(tf.image.decode_jpeg(file_contents , channels=1) , dtype=tf.float32)
    img = tf.image.resize_images(img , size=(paramsLen,1))
    img = tf.reshape(img , (-1,paramsLen))
    return img[0]


getAllPath(trainPath + big , 1)
getAllPath(trainPath + middle , 2)
getAllPath(trainPath + small , 3)

imgString = tf.convert_to_tensor(pathList , dtype=tf.string)
labelString = tf.convert_to_tensor(labelList , dtype=tf.int32)

imgQueue = tf.train.slice_input_producer([imgString , labelString],shuffle=True , num_epochs= 2)
labelQueue = imgQueue[1]

img = sliceReadImage(imgQueue)



labels = tf.one_hot(labelQueue , 3)

x , y_ = tf.train.batch([img , labels] , batch_size=10)

# x = tf.train.batch([img] , batch_size=100)


# x =  tf.compat.v1.placeholder(tf.float32 , [None , paramsLen] , name='input')

W = tf.Variable(tf.zeros([paramsLen,3]))
c = tf.Variable(tf.zeros([3]))
y = tf.nn.softmax(tf.matmul(x,W) + c , name='output')


# y_ = tf.compat.v1.placeholder(tf.float32 , [None , 3])
cross_entropy = -tf.reduce_sum(y_*tf.math.log(y))

train_step = tf.compat.v1.train.GradientDescentOptimizer(0.01).minimize(cross_entropy,name='aaa')

localInit = tf.compat.v1.local_variables_initializer()
globalInit = tf.compat.v1.global_variables_initializer()

with tf.compat.v1.Session() as sess:
    sess.run(localInit)
    sess.run(globalInit)
    coorid = tf.train.Coordinator()
    thread = tf.train.start_queue_runners(sess = sess , coord=coorid)
    try:
        while not coorid.should_stop():
            imgs = sess.run(train_step)

            correct_prediction = tf.equal(tf.argmax(y , 1) , tf.argmax(y_ , 1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction , tf.float32))
            print(sess.run(accuracy ))


    except tf.errors.OutOfRangeError:
        print("done")
    finally:
        coorid.request_stop()

    coorid.join(thread)