# coding=utf-8
import datetime
import Put_flavors_SA
# import ARMA_Interface
import AR_Interface
import copy
from DeNoise import *


# import matplotlib.pyplot as plt
def addtwodimdict(thedict, key_a, key_b):
    if key_a in thedict:
        thedict[key_a].update({key_b: 0})
    else:
        thedict.update({key_a: {key_b: 0}})


def sortedDictValues(adict):
    keys = adict.keys()
    keys.sort()
    return map(adict.get, keys)


def predict_vm(ecs_lines, input_lines):
    # Do your work from here#
    result = []
    if ecs_lines is None:
        print
        'ecs information is none'
        return result
    if input_lines is None:
        print
        'input file information is none'
        return result

    ##----------dict context load-------##
    dict_train_data = dict()
    dict_date = {}
    for i in range(len(ecs_lines)):
        date_build = ecs_lines[i].split('\t')[2].split(' ')[0]
        dict_date[date_build] = 0

    date_train_start = datetime.datetime.strptime(sorted(dict_date.keys())[0], '%Y-%m-%d')
    date_train_end = datetime.datetime.strptime(date_build, '%Y-%m-%d')
    delta = date_train_end - date_train_start

    dict_date = {}
    for i in range(delta.days + 1):
        n_date = date_train_start + datetime.timedelta(days=i)
        n_day = n_date.strftime('%Y-%m-%d')
        dict_date.update({n_day: 0})
        # dict_date[n_day]=0
    date_test_end = input_lines[len(input_lines) - 1].split(' ')[0]
    date_test_start = input_lines[len(input_lines) - 2].split(' ')[0]
    date_train_start = date_train_start.strftime('%Y-%m-%d')
    date_train_end = n_day
    # day_test2train = datetime.datetime.strptime(date_test_end, '%Y-%m-%d') - datetime.datetime.strptime(date_test_start,
    day_test2train = datetime.datetime.strptime(date_test_end, '%Y-%m-%d') - datetime.datetime.strptime(date_test_start,
                                                                                                        '%Y-%m-%d')
    iter_num = day_test2train.days // 2
    # iter_num = 7
    ndays_train_end = delta.days // iter_num
    ndays_train_end_ = delta.days
    # check the num is completed,and all the flavor's name has been arranged
    # cpu input saved by dict_input_cpu
    # ram input saved by GB transformed by 1024MB
    dict_input_cpu = {}
    dict_input_ram = {}
    cpu_device = input_lines[0].split(' ')[0]
    ram_device = input_lines[0].split(' ')[1]
    num_flavor_class = int(input_lines[2])
    for i in range(num_flavor_class):
        dict_input_cpu[input_lines[3 + i].split(' ')[0]] = int(input_lines[3 + i].split(' ')[1])
        dict_input_ram[input_lines[3 + i].split(' ')[0]] = int(input_lines[3 + i].split(' ')[2]) // 1024

    ##
    for i in dict_input_cpu.keys():
        flavor_name = i
        for j in dict_date.keys():
            addtwodimdict(dict_train_data, flavor_name, j)

    for i in range(len(ecs_lines)):
        flavor_name = ecs_lines[i].split('\t')[1]
        for j in dict_date.keys():
            addtwodimdict(dict_train_data, flavor_name, j)
            # dict_train_data.update({flavor_name:{date_build:0}})
    print
    '2dimloadcomplete'
    del dict_date  # free dict_date
    for i in range(len(ecs_lines)):
        flavor_name = ecs_lines[i].split('\t')[1]
        date_build = ecs_lines[i].split('\t')[2].split(' ')[0]
        dict_train_data[flavor_name][date_build] += 1

    print
    'The number of requests for the interval date recording server---saved in a 2 dim dict'
    ##-----------------------------##
    target = input_lines[len(input_lines) - 4]

    dict_count_ = dict()
    for i in dict_train_data.keys():
        if i in dict_input_cpu.keys():
            dict_count_[i] = sortedDictValues(dict_train_data[i])
            # ---------------------------------------------------------- #
            #     drop_out_num = int(0.5 * ndays_train_end_)
            #     dict_count_day_temp = dict()
            #     # for j in dict_count_day_
            #     for j in dict_count_.keys():
            #         dict_count_day_temp[j]=sorted(list(dict_count_[j]),reverse = True)
            #         for i in range(drop_out_num):
            #             temp=dict_count_day_temp[j][i]
            #             for k in range(ndays_train_end_):
            #                 if(dict_count_[j][k]==temp):
            #                     dict_count_[j][k]=sum(dict_count_[j])/ndays_train_end
            # print("sum=",sum(dict_count_[j]))
            # print("flavor",j,"= ",dict_count_[j][k])

    dict_count_denoise = dict()
    for j in dict_count_.keys():
        # temp = []
        # temp.extend(DeNoiseGoss(dict_count_[j]))
        dict_count_denoise[j] = DeNoiseGoss(dict_count_[j])

    # 每天的数量累加 在平滑前预处理
    dict_count_preday = copy.deepcopy(dict_count_denoise)
    for i in dict_input_cpu.keys():
        for j in range(len(dict_count_preday[i]) - 1):
            dict_count_preday[i][j + 1] += dict_count_preday[i][j]

    # 把每天的数量累加 进入ep里进行平滑预处理
    dict_count_exp_predaysmooth = dict()
    for j in dict_count_preday.keys():
        # dict_count_exp_smooth[j]=exp_smooth(dict_count_[j],0.3)
        dict_count_exp_predaysmooth[j] = exp_smooth_double(dict_count_preday[j], 0.36)

    # 每天的数量累加平滑后，再进行差分，得到的就是每天的平滑量
    for i in dict_count_exp_predaysmooth.keys():
        for j in range(len(dict_count_exp_predaysmooth[i])):
            if j == 0:
                dict_count_preday[i][j] = dict_count_exp_predaysmooth[i][j] - 0
            else:
                dict_count_preday[i][j] = dict_count_exp_predaysmooth[i][j] - dict_count_exp_predaysmooth[i][j - 1]


                # dict_count_exp_smooth=dict()
                # for j in dict_count_.keys():
                #     # dict_count_exp_smooth[j]=exp_smooth(dict_count_[j],0.3)
                #     dict_count_exp_smooth[j]=exp_smooth_double(dict_count_[j],0.3)
                #


                # plt.figure()
                # plt.plot(dict_count_[j],"r")
                # plt.plot(dict_count_exp_smooth[j],"b")
                # plt.show()
    # 统计每周申请总数
    # num_weeks = delta.days // 7
    dict_count = dict()
    for i in dict_count_exp_predaysmooth.keys():
        dict_count[i] = [0 for k in range(ndays_train_end)]
        for j in range(ndays_train_end):
            dict_count[i][ndays_train_end - j - 1] = sum(
                dict_count_preday[i][delta.days - (j + 1) * iter_num:delta.days - j * iter_num])
            # ---------------------------------------------------------- #
    # 每周增加的各类服务器申请数
    dict_count_day_ = copy.deepcopy(dict_count)
    # dict_count_day = dict()
    # for i in dict_count_day_.keys():
    #     dict_count_day[i] = kalman(dict_count_day_[i])
    # dict_count_day[i] = dict_count_day_[i]
    # for i in dict_input_cpu.keys():
    #     if i in dict_train_data.keys():
    #         dict_count[i]=sortedDictValues(dict_train_data[i])
    # ---------------------------------------------------------- #
    #     drop_out_num = int(0.1 * ndays_train_end)
    # dict_count_day_temp=dict()
    # # for j in dict_count_day_.keys():
    #     dict_count_day_temp[j]=sorted(list(dict_count_day_[j]),reverse = True)
    #     for i in range(drop_out_num):
    #         temp=dict_count_day_temp[j][i]
    #         for k in range(ndays_train_end):
    #             if(dict_count_day_[j][k]==temp):
    #                 dict_count_day_[j][k]=sum(dict_count_day_[j])/ndays_train_end
    # dict_count_day_[j][k] = 0
    # 每周的数量累加
    for i in dict_input_cpu.keys():
        for j in range(len(dict_count[i]) - 1):
            dict_count[i][j + 1] += dict_count[i][j]

    target = target[0:3]  # 优化目标CPU或者是MEM

    # 申请的CPU总数 无应用，废弃
    # list_count_all=[0]*(delta.days//iter_num+1)
    # for j in range(delta.days//iter_num+1):
    #     for i in dict_count.keys():
    #         list_count_all[j]+=dict_count[i][j]*dict_input_cpu[i]

    ##预测时间总长
    # day_test2train = datetime.datetime.strptime(date_test_end, '%Y-%m-%d')-datetime.datetime.strptime(date_test_start, '%Y-%m-%d')
    # ndays_predict_end = day_test2train.days
    # --------------------------------------------------------- #
    ndays_predict_end = delta.days // iter_num + day_test2train.days // iter_num
    ndays_least = day_test2train.days % iter_num

    # predict count all flavors cpu 计算总数。。。可省略
    # count_predict_all=AR_Interface.Autoregressive(list_count_all,ndays_predict_end,ndays_train_end)
    # count_predict_all=ARMA_Interface.ARMA_predict(list_count_all,ndays_predict_end,ndays_train_end)

    # predict all kinds of nums of flavors
    count_predict = {}
    data_flavor = {}

    # for i in dict_count.keys():
    #     count_predict[i]=int(dict_count[i][ndays_train_end-1]/float(ndays_train_end)*(ndays_predict_end-ndays_train_end)+1)

    # 按每天的申请数预测
    # for i in dict_count.keys():
    #     count_predict[i]=ARMA_Interface.ARMA_predict(dict_count_day[i],ndays_predict_end,ndays_train_end)



    # 按每天的申请数差分预测

    dict_count_diff = copy.deepcopy(dict_count_day_)
    for i in dict_count_day_.keys():
        for j in range(ndays_train_end):
            if j == 0:
                dict_count_diff[i][j] = dict_count_day_[i][j] - 0
            else:
                dict_count_diff[i][j] = dict_count_day_[i][j] - dict_count_day_[i][j - 1]
    for i in dict_count_diff.keys():
        # count_predict[i]=ARMA_Interface.ARMA_predict(dict_count_diff[i],ndays_predict_end,ndays_train_end)
        # count_predict[i] = AR_Interface.Autoregressive(dict_count_day[i], dict_count[i],ndays_predict_end, ndays_train_end)
        count_predict[i] = AR_Interface.Autoregressive(dict_count_diff[i], dict_count_day_[i], ndays_predict_end,
                                                       ndays_train_end, ndays_least) \
            # +int(ndays_least*sum(dict_count_day_[i])/(len(dict_count_day_[i])))+1
        # print("count_predict[",i,"]=",count_predict[i])
    # #按每天的申请数累加预测
    # for i in dict_count.keys():
    #     # count_predict[i]=ARMA_Interface.ARMA_predict(dict_count[i],ndays_predict_end,ndays_train_end)
    #     count_predict[i]=AR_Interface.Autoregressive(dict_count[i],ndays_predict_end,ndays_train_end)



    # check the num of predict is or not right or suitable
    num_cpu = 0
    num_flavor_predict = 0
    for i in dict_count.keys():
        num_cpu += count_predict[i] * dict_input_cpu[i]
        num_flavor_predict += count_predict[i]

    # distribute the device
    allot_device = Put_flavors_SA.distribute_SA(count_predict, dict_input_cpu, dict_input_ram, int(cpu_device),
                                                int(ram_device), target)

    num_device = len(allot_device)
    distu = []
    temp = []
    for i in range(len(allot_device)):
        distu.append('')
        distu[i] = {}
        for j in allot_device[i].load:
            distu[i].update({j: 0})
    for i in range(len(allot_device)):
        for j in allot_device[i].load:
            distu[i][j] += 1

    # save the result as a list
    result = []
    result.append(num_flavor_predict)
    for i in count_predict.keys():
        string_out = i + ' ' + str(count_predict[i])
        result.append(string_out)
    result.append('')
    result.append(num_device)
    for i in range(num_device):
        string_out = str(i + 1)
        for j in distu[i].keys():
            string_out = string_out + ' ' + j + ' ' + str(distu[i][j])
        result.append(string_out)

    return result


