__author__ = 'chuzui'

a1 = 2
a2 = 4
t1 = [7,9,3,4,8,4]
t2 = [8,5,6,4,5,7]
e1 = [2,3,1,3,4,3]
e2 = [2,1,2,2,1,2]

a3 = 3
a4 = 2

f1=[]
f2=[]

l1=[]
l2=[]

f1.append(a1+t1[0])
f2.append(a1+t2[0])

for i in range(1,len(t1)):
    if f1[i-1] < f2[i-1]+e2[i-1]:
        f1.append(f1[i-1] + t1[i])
        l1.append(1)
    else:
        f1.append(f2[i-1]+e2[i-1] + t1[i])
        l1.append(2)

    if f2[i-1] < f1[i-1]+e1[i-1]:
        f2.append(f2[i-1] + t2[i])
        l2.append(2)
    else:
        f2.append(f1[i-1]+e1[i-1] + t2[i])
        l2.append(1)

print f1
print f2
print l1
print l2