
import tensorflow as tf
import numpy as np
import tensorflow_study.input_data as id

paramsLen = 3968 * 2976

imgsPath = ['/Users/shanwang/Desktop/data/xia/use/train/small/IMG_20191012_132502.jpg','/Users/shanwang/Desktop/data/xia/use/train/small/IMG_20191012_132524.jpg','/Users/shanwang/Desktop/data/xia/use/train/small/IMG_20191012_132545.jpg']
imgString = tf.convert_to_tensor(imgsPath , dtype=tf.string)
imgQueue = tf.train.string_input_producer(imgString , num_epochs= 2)


def loadImg(path_queue):
    reader = tf.WholeFileReader()
    key , value = reader.read(path_queue)
    img = tf.image.convert_image_dtype(tf.image.decode_jpeg(value , channels=1) , dtype=tf.float32)
    img = tf.image.resize_images(img , size=(paramsLen,1))
    img = tf.reshape(img , (-1,paramsLen))
    return img[0]
img = loadImg(imgQueue)

x = tf.train.batch([img] , batch_size=1)


# x =  tf.compat.v1.placeholder(tf.float32 , [None , paramsLen] , name='input')

W = tf.Variable(tf.zeros([paramsLen,3]))
c = tf.Variable(tf.zeros([3]))
y = tf.nn.softmax(tf.matmul(x,W) + c , name='output')


y_ = tf.compat.v1.placeholder(tf.float32 , [None , 3])
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
            imgs = sess.run(train_step , feed_dict={  y_: np.array([[0,1,0]],dtype= np.float32)})


    except tf.errors.OutOfRangeError:
        print("done")
    finally:
        coorid.request_stop()

    coorid.join(thread)