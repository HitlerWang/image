import tensorflow as tf
import os

def save_model_ckpt(ckpt_file_path):
    x = tf.placeholder(tf.int32, name='x')
    y = tf.placeholder(tf.int32, name='y')
    b = tf.Variable(1, name='b')
    xy = tf.multiply(x, y)
    op = tf.add(xy, b, name='op_to_store')

    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    path = os.path.dirname(os.path.abspath(ckpt_file_path))
    if os.path.isdir(path) is False:
        os.makedirs(path)

    tf.train.Saver().save(sess, ckpt_file_path)

    # test
    feed_dict = {x: 2, y: 3}
    print(sess.run(op, feed_dict))


def restore_model_ckpt(ckpt_file_path):
    sess = tf.Session()
    saver = tf.train.import_meta_graph('/Users/shanwang/Desktop/data/study/minist/test_model/model.meta') # 加载模型结构
    saver.restore(sess, tf.train.latest_checkpoint('/Users/shanwang/Desktop/data/study/minist/test_model')) # 只需要指定目录就可以恢复所有变量信息

    # 直接获取保存的变量
    print(sess.run('b:0'))

    # 获取placeholder变量
    input_x = sess.graph.get_tensor_by_name('x:0')
    input_y = sess.graph.get_tensor_by_name('y:0')
    # 获取需要进行计算的operator
    op = sess.graph.get_tensor_by_name('op_to_store:0')

    # 加入新的操作
    add_on_op = tf.multiply(op, 2)

    ret = sess.run(add_on_op, {input_x: 5, input_y: 5})
    print(ret)

restore_model_ckpt("/Users/shanwang/Desktop/data/study/minist/test_model/model")