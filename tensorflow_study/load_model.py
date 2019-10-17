import tensorflow as tf
from tensorflow.python.framework import graph_io
from tensorflow.python.framework.graph_util import convert_variables_to_constants
import numpy as np

saver = tf.train.import_meta_graph("/Users/shanwang/Desktop/data/study/minist/tf_model/model.meta")
graph = tf.get_default_graph()

sess = tf.Session()
sess.run(tf.global_variables_initializer())
saver.restore(sess , tf.train.latest_checkpoint('/Users/shanwang/Desktop/data/study/minist/tf_model'))

graph = sess.graph
with graph.as_default():
    output_names = ["output"]
    input_graph_def = graph.as_graph_def()
    frozen_graph = convert_variables_to_constants(sess , input_graph_def , output_names)
graph_io.write_graph(frozen_graph , '/Users/shanwang/Desktop/data/study/minist/pb_model' , 'pb_model' , as_text=False)



