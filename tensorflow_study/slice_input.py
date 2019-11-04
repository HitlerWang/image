'''
created on January 5 13:08 2018

@author:lhy
'''
import tensorflow as tf

path_list=['/Users/shanwang/Desktop/data/xia/use/train/small/IMG_20191012_132502.jpg','/Users/shanwang/Desktop/data/xia/use/train/small/IMG_20191012_132524.jpg','/Users/shanwang/Desktop/data/xia/use/train/small/IMG_20191012_132545.jpg']

#加入了标签，在使用的时候可以直接对应标签取出数据
label=[0,1,2]
#转换成张量tensor类型
img_path=tf.convert_to_tensor(path_list,dtype=tf.string)
label=tf.convert_to_tensor(label,dtype=tf.int32)

#返回了一个包含路径和标签的列表，并将文件名和对应的标签放入文件名对列中，等待系统调用
image=tf.train.slice_input_producer([img_path,label],shuffle=True,num_epochs=1)#shuffle=Flase表示不打乱，当为True的时候打乱顺序放入文件名队列
labels=image[1]

def load_image(path_queue):
    #读取文件，这点与string_input_producer不一样！！！！！
    file_contents=tf.read_file(path_queue[0])
    img=tf.image.convert_image_dtype(tf.image.decode_png(file_contents,channels=3),tf.float32)

    img=tf.image.resize_images(img,size=(228,228))
    return img

img=load_image(image)
print(img.shape)
#设置one_hot编码，并将labels规定为3种，在前向传播的时候默认会将结果的shape变为batch_size*3,从而达到分类的情况，这一步在使用标签的时候很重要
labels=tf.one_hot(labels,3)
img_batch,label_batch=tf.train.batch([img,labels],batch_size=1)

with tf.Session() as sess:
    #initializer for num_epochs
    tf.local_variables_initializer().run()
    coord=tf.train.Coordinator()
    thread=tf.train.start_queue_runners(sess=sess,coord=coord)
    try:
        while not coord.should_stop():
            imgs,label=sess.run([img_batch,label_batch])
            print(imgs.shape)
            print(label)
    except tf.errors.OutOfRangeError:
        print('Done')
    finally:
        coord.request_stop()
    coord.join(thread)