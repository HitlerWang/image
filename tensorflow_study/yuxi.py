import tensorflow as tf

# x = tf.Variable(3, tf.int16)
# y = tf.Variable(5, tf.int16)
# z = tf.add(x, y)
# init = tf.global_variables_initializer()
# with tf.Session() as sess:
#     sess.run(init)
#     print(sess.run(z))



# x = tf.constant([[3.,3.]])
# y = tf.constant([[2.],[2.]])
# product = tf.matmul(x , y)
# with tf.Session() as sess:
#     result = sess.run(product)
#     print(result)


sess = tf.InteractiveSession()

x = tf.Variable([1.0,2.0])
y = tf.constant([3.0,3.0])
x.initializer.run()

sub = tf.sub(x,y)
print(sub.eval())