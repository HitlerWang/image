
import tensorflow as tf
path_list=['/Users/shanwang/Desktop/data/xia/use/train/small/IMG_20191012_132502.jpg','/Users/shanwang/Desktop/data/xia/use/train/small/IMG_20191012_132524.jpg','/Users/shanwang/Desktop/data/xia/use/train/small/IMG_20191012_132545.jpg']
img_path=tf.convert_to_tensor(path_list,dtype=tf.string)#将list转化张量tensor

image=tf.train.string_input_producer(img_path,num_epochs=1)#放入文件名队列中，epoch是1

def load_img(path_queue):
    #创建一个队列读取器，然后解码成数组,与slice的不同之处，重要！！！！！！！！！
    reader=tf.WholeFileReader()
    key,value=reader.read(path_queue)

    img=tf.image.convert_image_dtype(tf.image.decode_png(value,channels=3),tf.float32)#将图片decode成3通道的数组
    img=tf.image.resize_images(img,size=(224,224))
    return img

img=load_img(image)

print(type(img))
print(img.shape)
#可以看出string进行处理的时候只处理了图片本身，对标签并没有处理。将图片放入内存队列，因为abtch_size=1,所以一次放入一张供读取。但是系统还是“停滞”状态。
image_batch=tf.train.batch([img],batch_size=1)

with tf.Session() as sess:
    tf.local_variables_initializer().run()
    tf.global_variables_initializer().run()
    coord=tf.train.Coordinator()
    #tf.train.start_queue_runners()函数才会启动填充队列的线程，系统不再“停滞”，此后计算单元就可以拿到数据并进行计算
    thread=tf.train.start_queue_runners(sess=sess,coord=coord)
    try:
        while not coord.should_stop():
            imgs=sess.run(image_batch)
            print(imgs.shape)
    #当文件队列读到末尾的时候，抛出异常
    except tf.errors.OutOfRangeError:
        print('done')
    finally:
        coord.request_stop()#将读取文件的线程关闭
    coord.join(thread)#将读取文件的线程加入到主线程中（虽然说已经关闭过）


with tf.Session() as sess:
    tf.local_variables_initializer().run()
    tf.global_variables_initializer().run()
    coord = tf.train.Coordinator()
    thread = tf.train.start_queue_runners(sess = sess , coord= coord)
    try:
        while not coord.should_stop():
            imgs = sess.run(image_batch)
            print(imgs.shape)
    except tf.errors.OutOfRangeError:
        print("done")
    finally:
        coord.request_stop()
    coord.join(thread)

