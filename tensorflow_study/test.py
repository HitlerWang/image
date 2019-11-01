import tensorflow as tf

v1 = tf.constant([1,2,3])
v2 = tf.constant([3,4,5])

v_add = tf.add(v1 ,v2)
with tf.Session() as sess:
    print(sess.run(v_add))
