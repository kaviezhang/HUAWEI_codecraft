# coding=utf-8
from mat_op import *
from source import *
import random
# import matplotlib.pyplot as plt
import math
global y
global x

x = []
y = []

def formatData(data,p):
    global x
    global y
    x=[]
    y=[]
    #tmpy=[]
    for i in range(p,len(data)):
        y.append(data[i])
        tmp=[]
        for j in range(i-p,i):
            tmp.append(data[j])
        x.append(tmp)
    #y.append(tmpy)
    #y=trans(y)
    return 0

def LeastSquares(data,p):
    formatData(data,p)
    a=[[]]
    tx=[[]]
    invx=[[]]
    tmp=[[]]
    tx=trans(x)
    test=mulmat(tx,x) #test
    invx=inv(mulmat(tx,x))
    print 'inv'
    a = mulmat(mulmat(invx, tx), y)
    a = trans(a)
    print 'midmidmid'
    return a[0]

def getBias(data,a,n,p):
    sum=0.0
    calPN=data[0:p]
    for i in range(p,len(data)):
        s=0.0
        t=len(calPN)
        for j in range(p):
            s += a[j] * calPN[t - j - 1]
        calPN.append(s)
    for i in range(p,len(calPN)):
        sum += (data[i] - calPN[i])
    return sum / (n-p)

def calP_N(data,a,p):
    n=len(data)
    calPN=data[0:p]
    for i in range(p,len(data)):
        s=0.0
        t=len(calPN)
        for j in range(p):
            s += a[j] * calPN[t - j - 1]
        calPN.append(s)

    var=[]
    for i in range(p,len(calPN)):
        var.append(data[i]-calPN[i])
    Avar = getAutoCor(var) #得到的自相关系数
    Bvar = getBiasCor(Avar) #得到偏相关系数
    print '自相关系数:'
    for k in range(len(Avar)):
        print(Avar[k])
    # 检验是否有 68.3% 的 点 落 在 纵 坐 标ρ = ± 1 / n 内
    # 约 有 95.4% 的 点 落 在 纵 坐 标 ρ = ± 2 / n 内
    k1 = 0
    k2 = 0
    p1 = 1.0 / len(Avar)
    p2 = 2.0 / len(Avar)
    for k in range(len(Avar)):
        if Avar[k] >= -p1 and Avar[k] <= p1:
            k1+=1
        if Avar[k] >= -p2 and Avar[k] <= p2:
            k2+=1
    print 'ρ = ± 1 / n：'+str(k1*1.0 / len(Avar))
    print 'ρ = ± 2 / n：'+str(k2*1.0 / len(Avar))
    return 0
#
# def predict(data,weight,k,p):#predict(data, BGD_Train.finalweight, i+1, p)
#     res=0.0
#     for i in range(len(data),k):
#         s=0.0
#         t=len(data)
#         for j in range(p):
#             s += weight[j] * data[t - j - 1]
#         data.append(s)
#     return data[k-1]
def predict(predic_data,weight,begin,p,predict_end,k):#predict(data, BGD_Train.finalweight, i+1, p)
    temp=0.0
    for i in range(begin,predict_end):
        s=0.0
        #t=len(predic_data)
        for j in range(p):
            s += math.exp((p-j)**2/(-2*k**2))*weight[j] * predic_data[i - p + j]
            #print("begin - p + j=",i - p + j)
            #print("s=", s)
        predic_data.append(math.ceil(s))

    return predic_data
class BGD:
    def __init__(self,data,p,learning_rate,iteration,k):
        self.weight=[]
        self.loss=0.0
        self.learning_rate=learning_rate
        self.data=data
        self.p=p
        self.iteration=iteration
        self.finalloss=10000000
        self.finalweight=[]
        self.k=k
        self.Gra_diff_part=[]

        for p_idex in range(self.p):
            #self.weight.append(random.uniform(0,1))
            self.weight.append(0.5)
        for p_idex in range(self.p):
            self.finalweight.append(0.0)
        for p_idex in range(self.p):
            self.Gra_diff_part.append(0.0)
    def train(self):
        reg_term=0.5
        formatData(self.data, self.p)
        self.finalloss = 10000000
        for iter_num in range(self.iteration):
            self.loss = 0.0
            for p_idex in range(self.p):
                self.Gra_diff_part[p_idex]=0.0
            for lp in range(len(self.data)-self.p):
                #print("lp=",lp-self.p)
                diff=0.0
                sum=0.0
                for p_index in range(self.p):
                    #print("p_index=",p_index)
                    #sum=sum+math.exp(-1*(self.p-p_index)**2/2*self.k**2)*self.weight[p_index]*(lp+p_index)
                    sum = sum + math.exp( (self.p - p_index)/ (-2 * self.k ** 2)) * self.weight[p_index] * x[lp][p_index]
                #diff=abs(sum-y[lp])
                diff =sum-y[lp]
                for i in range(self.p):
                    self.Gra_diff_part[i]=self.Gra_diff_part[i]+diff*x[lp][i]+reg_term*2*self.weight[i]
            for p_ind in range(self.p):
                #print("weight_before=",self.weight[p_ind])
                self.weight[p_ind]=self.weight[p_ind]-self.learning_rate*self.Gra_diff_part[p_ind]#gengxintidu
                #print("weight_end=",self.weight[p_ind])
            sec_norm=0
            for p_ind in range(self.p):
                sec_norm=sec_norm+self.weight[p_ind]**2
            for lp_index in range(len(self.data)-self.p):
                new_sum=0.0
                for p_inde in range(self.p):
                    temp=math.exp((self.p-p_inde)/(-2*self.k**2))*self.weight[p_inde]*x[lp_index][p_inde]
                    new_sum=new_sum+temp
                    #print("new_sum=",new_sum)
                    #print("(y[lp_index-self.p]-new_sum)**2/2=",(y[lp_index-self.p]-new_sum)**2/2)
                self.loss=self.loss+(new_sum-y[lp_index])**2/2+reg_term*sec_norm
            print("loss=",self.loss)
            if(self.finalloss>self.loss):
                self.finalloss=self.loss
                for p_i in range(self.p):
                    self.finalweight[p_i]=self.weight[p_i]

            #print("iter=",iter_num,"self.finalloss=",self.finalloss)
def Autoregressive(xx,dict_count_day,ndays_predict_end,ndays_train_end,least_day):
    global result_pred
    result_pred=0
    # xx = [871.5,897.1,904.3,919.2,935.0,950.0,965.0,981.0,1028.0,1047.0,1061.0,1075.0,
    #           1086.0,1094.0,1102.0,1112.0,1125.0,1251.1,1259.4,1240.0,1245.6,1257.2,1363.6,
    #         1385.1,1423.2,1456.4,1492.7,1538.0,1601.0,1676.0,1771.0,1860.0,1961.9,2018.6,2069.3]
    size=len(xx)
    print xx
    learning_rate=0.00005
    iteration=3000
    k=3.42
    p=int(size*0.5)#原则上p可以选择[16-N],但是由于p大于18时，计算会超过精度，又考虑到模型尽可能简单，参数尽可能少，选择p=[15,16,17]
    # #这里分别用excel纪录了图像描述
    data=[]
    for i in range(size):
        data.append(float(xx[i]+abs(random.gauss(0,0.1))))
    # 计算
    # Calculate_p(data)
    BGD_Train=BGD(xx,p,learning_rate,iteration,k)
    BGD_Train.train()
    for i in range (p):
        print("weight=",BGD_Train.weight[i])
    # a=LeastSquares(data,p)
    #
    # print '参数a个数:  '+str(len(a))
    # for i in range(len(a)):
    #     print 'a['+str(i)+']='+str(a[i])
    # calP_N(data, a, p)

    pre_num=[]
    for i in range(size):
        pre_num.append(xx[i])
    predict(pre_num, BGD_Train.finalweight, size, p, ndays_predict_end,k)

    # for i in range(len(data)+ndays_predict_end-ndays_train_end):
    #     result=predict(data, BGD_Train.finalweight, i+1, p)
    #     pre_num.append(result)
    print pre_num
    final_predict = []

    # for i in range(size):
    #     # final_predict.append(sum(xx[0:i]))
    #     final_predict.append(xx[i])
    # # first_num = dict_count_day[size - 1] + pre_num[size - 1]
    # first_num = pre_num[size - 1]
    # if (first_num < 0):
    #     final_predict.append(0)
    # else:
    #     final_predict.append(first_num)
    # print("first_num=", first_num)
    # for final_idx in range(ndays_predict_end - ndays_train_end - 1):
    #     fina_temp = final_idx + size
    #     if (final_predict[fina_temp] + pre_num[fina_temp] < 0):
    #         final_predict.append(0)
    #     else:
    #         final_predict.append(final_predict[fina_temp] + pre_num[fina_temp])
    #final_predict = []
    # plt.figure()
    # plt.plot(xx)
    # plt.plot(pre_num, 'r--')
    # plt.show()
    # print 'end'

    # result_pred=predict(data, BGD_Train.finalweight, ndays_predict_end, p) -predict(data, BGD_Train.weight, ndays_train_end, p)
    # print 'num of predict = '+ str(result_pred)
    # if result_pred<0:
        # result_pred=0
    # return int(result_pred)


    for i in range(size):
        final_predict.append(dict_count_day[i])
    first_num = dict_count_day[size - 1] + pre_num[size]
    # print("dict_count_day[p - 1]=",dict_count_day[size - 1])
    # print("pre_num[p - 1]=",pre_num[size - 1])
    if (first_num < 0):
        final_predict.append(0)
    else:
        final_predict.append(first_num)
    print("first_num=", first_num)
    for final_idx in range(ndays_predict_end - ndays_train_end-1):
        fina_temp = final_idx + size
        if (final_predict[fina_temp] + pre_num[fina_temp+1] < 0):
            final_predict.append(0)
        else:
            final_predict.append(final_predict[fina_temp] + pre_num[fina_temp+1])

    # plt.figure()
    # plt.plot(xx)
    # plt.plot(pre_num, 'r--')
    # plt.show()
    # final_sum=final_predict[ndays_predict_end-1]-final_predict[ndays_train_end-1]
    final_sum=0

    for i in range(ndays_predict_end-ndays_train_end):
        final_sum=final_sum+final_predict[i+size]
    final_sum=final_sum+least_day*final_sum/(ndays_predict_end-ndays_train_end)
    # plt.figure()
    # plt.plot(pre_num,'b')
    # plt.plot(xx,'g--')
    # plt.figure()
    #
    # plt.plot(final_predict,'r')
    # plt.plot(dict_count_day, 'b--')
    # plt.show()

    print 'end'

    # result_pred=predict(data, a, ndays_predict_end, p) -predict(data, a, ndays_train_end, p)
    # print 'num of predict = '+ str(result_pred)
    # if result_pred<0:
    #     result_pred=0
    return int(final_sum)