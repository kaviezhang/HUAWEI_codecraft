# coding=utf-8
import copy
#矩阵转置
def trans(A):
    tx=[]
    for i in range(len(A[0])):
        tmp=[0]*len(A)
        tx.append(tmp)
    for i in range(len(A)):
        for j in range(len(A[0])):
            tx[j][i] = A[i][j]
    return tx

#矩阵相乘
def mulmat(A,B):
    res = [[0] * len(B[0]) for i in range(len(A))]
    # res=[[0] * len(B[0])]*len(A)
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                res[i][j] += A[i][k] * B[k][j]
    return res

#矩阵行列式
def det(m):
    if len(m) <= 0:
        return None
    if len(m) == 1:
        return m[0][0]
        #因此矩阵仅有一个元素的时候，在赋值操作时也要写成[[]]的二维矩阵形式
    else:
        s = 0
        for i in range(len(m)):
            n = [[row[a] for a in range(len(m)) if a != i] for row in m[1:]]
            if i % 2 == 0:
                s += m[0][i] * det(n)
            else:
                s -= m[0][i] * det(n)
    return s

#矩阵删除第r行，第c列
def delmat( A, r, c):
    result=[]
    for i in range(len(A)):
        temp=[]
        for j in range(len(A[0])):
            if i!=r and j!=c:
                temp.append(A[i][j])
        if i != r:
            result.append(temp)
    return result

#矩阵的伴随矩阵
def adjoint(A):
    temp=[[]]
    res=[[]]
    res = [[0] * len(A[0]) for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            tmp=A
            tmp = delmat(tmp,i,j)
            res[i][j]=(1 if (i+j)%2==0 else -1) * det(tmp)
    return res

#矩阵的逆
def inv(A):
    res=adjoint(A)
    dets=det(A)
    if dets==0:
        print 'no inv'
    for i in range(len(res)):
        for j in range(len(res[0])):
            res[i][j]/=dets
    return res

#合并两个行相同的矩阵
def conrows(X,Y):
    res=copy.deepcopy(X)
    for i in range(len(Y)):
        for j in range(len(Y[0])):
            res[i].append(Y[i][j])
    return res

#合并两个列相同的矩阵
def concols(X,Y):
    res=copy.deepcopy(X)
    for i in range(len(Y)):
        row=[]
        for j in range(len(Y[0])):
            row.append(Y[i][j])
        res.append(row)
    return res
