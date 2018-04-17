# coding=utf-8
import copy
import math
def DeNoiseGoss(dict_count_diff):

    lenth = len(dict_count_diff)
    u = float(sum(dict_count_diff))/lenth
    var2 = 0
    for i in range(lenth):
        var2 += (dict_count_diff[i] - u) ** 2
    var = float((float(var2)/lenth)) ** 0.5

    # dataRange = [u-var*3,u+var*3]
    kernel_size=8



    dict_count_return = list()
    #掐头去尾
    for i in range(lenth):
        if i < kernel_size//2 or i >= lenth-kernel_size//2:
            if  dict_count_diff[i] > u+var*3 or dict_count_diff[i] < u-var*3:
                dict_count_return.append(round(u+var*4))
            elif dict_count_diff[i] < u-var*3:
            	dict_count_return.append(round(u-var*4))
            else:
                dict_count_return.append(dict_count_diff[i])
                # dict_count_return[i] += 1 # 零点太多影响计算结果，故给每个值加一个1
        else:
            dict_count_return.append(dict_count_diff[i])
    dict_count_diff_new=copy.deepcopy(dict_count_return)
    #滑窗滤波
    for i in range(kernel_size//2 ,lenth-kernel_size//2):
        aver = 0.0
        for k in range(- kernel_size // 2,  kernel_size // 2):
            aver += dict_count_return[i + k]
        aver = aver/float(kernel_size+1)
        if dict_count_return[i] > u+var*4 or dict_count_return[i] < u-var*4:
            # new = sorted(dict_count_return[i - kernel_size // 2: i + kernel_size // 2 + 1])
            # dict_count_return[i] = int(sorted(dict_count_return[i - kernel_size // 2: i + kernel_size // 2 + 1])[kernel_size // 2])
            dict_count_diff_new[i]=aver


    return dict_count_diff_new

def exp_smooth(wave,a):
    temp=[]
    for i in range(len(wave)):
        if(i==0):
            b=float(sum(wave)/len(wave))
            temp.append(b)
        else:
            temp.append((1-a)*temp[i-1]+a*wave[i])
    return temp



def exp_smooth_double(wave,arfa):
    temp=[]
    y = wave
    info_data_id = [1]
    info_data_sales = [[] for i in range(len(info_data_id))]
    for i in range(len(info_data_id)):
        for j in range(len(y)):
            info_data_sales[i].append(y[j])

    ##二次指数平滑的初值为S2_1，用S2_1_new来储存每一组数据的一次平滑的数值
    S2_1 = []
    S2_2 = []
    for m in range(0, len(info_data_id)):
        S2_1_empty = []
        x = 0
        for n in range(0, 3):
            x = x + float(info_data_sales[m][n])
        x = x / 3
        S2_1_empty.append(x)
        S2_1.append(S2_1_empty)
        S2_2.append(S2_1_empty)
    # print(S2_2)
    a = [arfa]  ##这是用来存放阿尔法的数组
    info_MSE = []  ##计算均方误差来得到最优的a(阿尔法)

    ##下面是计算一次指数平滑的值
    S2_1_new1 = []
    for i in range(0, len(info_data_sales)):
        S2_1_new = [[]] * len(info_data_id)
        for j in range(0, len(info_data_sales[i])):
            if j == 0:
                S2_1_new[i].append(
                    float(a[i]) * float(info_data_sales[i][j]) + (1 - float(a[i])) * float(S2_1[i][j]))
            else:
                S2_1_new[i].append(float(a[i]) * float(info_data_sales[i][j]) + (1 - float(a[i])) * float(
                    S2_1_new[i][j - 1]))  ##计算一次指数的值
        S2_1_new1.append(S2_1_new[i])
    # print(S2_1_new1)
    # print(len(S2_1_new1[i]))

    ##下面是计算二次指数平滑的值
    S2_2_new1 = []
    info_MSE = []  ##计算均方误差来得到最优的a(阿尔法)
    for i in range(0, len(info_data_sales)):
        S2_2_new = [[]] * len(info_data_id)
        MSE = 0
        for j in range(0, len(info_data_sales[i])):
            if j == 0:
                S2_2_new[i].append(float(a[i]) * float(S2_1_new1[i][j]) + (1 - float(a[i])) * float(S2_2[i][j]))
            else:
                S2_2_new[i].append(
                    float(a[i]) * float(S2_1_new1[i][j]) + (1 - float(a[i])) * float(S2_2_new[i][j - 1]))  ##计算二次指数的值
            MSE = (int(S2_2_new[i][j]) - int(info_data_sales[i][j])) ** 2 + MSE
        MSE = (MSE ** (1 / 2)) / int(len(info_data_sales[i]))
        info_MSE.append(MSE)
        S2_2_new1.append(S2_2_new[i])
    # print(S2_2_new1)
    # print(len(S2_2_new1[i]))

    ##下面是计算At、Bt以及每个预估值Xt的值，直接计算预估值，不一一列举Xt的值了
    u = 1
    Xt = []
    for i in range(0, len(info_data_sales)):
        At = (float(S2_1_new1[i][len(S2_1_new1[i]) - 1]) * 2 - float(S2_2_new1[i][len(S2_2_new1[i]) - 1]))
        Bt = (float(a[i]) / (1 - float(a[i])) * (
        float(S2_1_new1[i][len(S2_1_new1[i]) - 1]) - float(S2_2_new1[i][len(S2_2_new1[i]) - 1])))
        Xt.append(At + Bt * int(u))
        print('第' + str(i + 1) + '组的二次平滑预估值为:' + str(Xt[i]) + '；均方误差为：' + str(info_MSE[i]))


    return S2_1_new1[0]