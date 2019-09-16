import tensorflow as tf
import numpy as np
import tensorflow_study.input_data as id


mnist = id.read_data_sets('/Users/shanwang/Desktop/data/study/minist/' , one_hot= True)

# tr_x , tr_y = mnist.train.next_batch(100)
# print(tr_y[0])
# oo = tr_x[0].reshape(-1,28)
# for item in oo:
#     for lin in item:
#         print('%.2f'%lin,end='')
#     print('')


x =  tf.compat.v1.placeholder(tf.float32 , [None , 784])

W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))
y = tf.nn.softmax(tf.matmul(x,W) + b)


y_ = tf.compat.v1.placeholder(tf.float32 , [None , 10])
cross_entropy = -tf.reduce_sum(y_*tf.math.log(y))

train_step = tf.compat.v1.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

init = tf.compat.v1.global_variables_initializer()

with tf.compat.v1.Session() as sess:
    sess.run(init)
    for i in range(1000):
        batch_xs , batch_ys = mnist.train.next_batch(100)
        sess.run(train_step , feed_dict={x:batch_xs , y_:batch_ys})


        correct_prediction = tf.equal(tf.argmax(y , 1) , tf.argmax(y_ , 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction , tf.float32))
        print(sess.run(accuracy , feed_dict={x:mnist.test.images , y_:mnist.test.labels}))