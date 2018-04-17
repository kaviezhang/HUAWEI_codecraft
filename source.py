# coding=utf-8
import copy

#自协方差AutoCov[k] = E((x[i] - u)(x[i - k] - u))
#自相关系数AutoCov[k] = AutoCov[k] / AutoCov[0]
def getAutoCov(data):
    n=len(data)
    mean=0.0
    for i in range(n):
        mean+=data[i]
    mean/=n
    prodata=[]
    for i in range(n):
        prodata.append(data[i]-mean)
    AutoCov=[0]*n
    for j in range(n):
        for i in range(n-j):
            AutoCov[j]+=prodata[i]*prodata[i+j]
        AutoCov[j]/=n-j
    return AutoCov
def getAutoCor(data):
    AutoCor=[]
    AutoCov=getAutoCov(data)
    for k in range(len(data)-1):
        AutoCor.append(AutoCov[k+1]/AutoCov[0])
    return AutoCor

# 得到偏相关系数BiasCor[k,k]
#  BiasCor[0,0] = AutoCor[0]
#  BiasCor[k,k] = (AutoCor[k-1] - sum[j:0...k-1]{AutoCor[k-j]*BiasCor[j,k-1]}) / (1 - sum[j:0...k-1]AutoCor[j]*BiasCor[j,k-1])
#  BiasCor[j,k] = BiasCor[j,k-1] - BiasCor[k,k]*BiasCor[k-j,k-1] j = 0...k
def getBiasCor(AutoCor):
    BiasCor=[]
    for i in range(len(AutoCor)):
        tmp=[0]*len(AutoCor)
        BiasCor.append(tmp)
    BiasCor[0][0]=AutoCor[0]
    for k in range(1,len(AutoCor)):
        BiasCor[k][k]=AutoCor[k]
        t1=0
        t2=0
        for j in range(k):
            t1 = AutoCor[k-j]*BiasCor[j][k - 1]
            t2 = AutoCor[j] * BiasCor[j][k - 1]
            BiasCor[j][k] = BiasCor[j][k - 1] - BiasCor[k][k] * BiasCor[k - j][k - 1]
        BiasCor[k][k] = (BiasCor[k][k]-t1)/t2
        for j in range(k):
            BiasCor[k][j] = BiasCor[j][k] = BiasCor[j][k-1] - BiasCor[k][k] * BiasCor[k-j][k-1]
    res=[]
    for k in range(len(AutoCor)):
        res.append(BiasCor[k][k])
    return res