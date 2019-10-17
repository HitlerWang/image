import tensorflow as tf
import numpy as np
import tensorflow_study.input_data as id
# mnist = id.read_data_sets('/Users/shanwang/Desktop/data/study/minist/' , one_hot= True)

# sess = tf.Session()
# saver = tf.train.import_meta_graph("/Users/shanwang/Desktop/data/study/minist/tf_model/model.meta")
# saver.restore(sess , tf.train.latest_checkpoint("/Users/shanwang/Desktop/data/study/minist/tf_model"))
#
# batch_xs , batch_ys = mnist.test.next_batch(10)
#
# # print(sess.run('input:0'))
# input_x = sess.graph.get_tensor_by_name('input:0')
#
# print(input_x)




outputGraph = tf.GraphDef()

with open("/Users/shanwang/Desktop/data/study/minist/pb_model/pb_model" , "rb") as f:
    outputGraph.ParseFromString(f.read())
    tensors = tf.import_graph_def(outputGraph , name="")

sess = tf.Session()
sess.run(tf.global_variables_initializer())
graph = tf.get_default_graph()

input = graph.get_tensor_by_name("input:0")
output = graph.get_tensor_by_name("output:0")

mnist = id.read_data_sets('/Users/shanwang/Desktop/data/study/minist/' , one_hot= True)
batch_xs , batch_ys = mnist.test.next_batch(10)
print(type(batch_xs))
output = sess.run(output , feed_dict={input:batch_xs})

print(output)