import numpy as np

a = np.array([1,2,3,4,5,6,7] , ndmin=3 )
print(a)
print(type(a))
print(a.ndim)

b = np.array([1,2,34],dtype= complex)
print(b)
print(type(b))


dType = np.dtype([('age' , np.int8)])
c = np.array([(10,),(20,)],dtype=dType)
print(c)
print(type(c))
print(type(c[0]))
print(c['age'])


sType = np.dtype([('name','S20') , ('age','i8')])
d = np.array([('wangshan',90),('liuyue',800)] , dtype=sType)
print(d['name'])
print(d.data)
print(d.ndim)
print(d.flags)


e = np.empty([3,3,3,] , dtype=np.int8)
print(e)

f = np.zeros([2,2] , dtype= [('x' ,'i4'),('y','i4')])
print(f)


g = np.ones([2,2] , dtype=int)
print(g)

s = b'abcdefghijk'
h = np.frombuffer(s , dtype='S1')
print(h)


i = np.asarray([1,2,3,4,5,6,7], dtype=int)
print(i)


list = range(6)
it = iter(list)
j = np.fromiter(it , dtype=float)
print(j)

h = np.arange(1, 20)
print(h)

i = np.linspace(0 , 20 , 8 ,endpoint=True)
print(i)

j = np.logspace(1, 20 , 9 , base=9)
print(j)


a = np.array([22,87,5,43,56,73,55,54,11,20,51,5,79,31,27])
np.histogram(a,bins =  [0,20,40,60,80,100])
hist,bins = np.histogram(a,bins =  [0,20,40,60,80,100])
print (hist)
print (bins)