#!/usr/bin/python3
################################################################################
# Copyright Statement: CVTE
# Copyright (C) 2013 Guangzhou Shiyuan Electronics Co.,Ltd. All rights reserved.
#      ____________        _______________  ___________
#     / / ________ \      / / _____   ____|| |  _______|
#    / / /      \ \ \    / / /   | | |     | | |
#   | | |        \ \ \  / / /    | | |     | | |_______
#   | | |         \ \ \/ / /     | | |     | |  _______|
#   | | |          \ \ \/ /      | | |     | | |
#    \ \ \______    \ \  /       | | |     | | |_______
#     \_\_______|    \_\/        |_|_|     |_|_________|
# 
################################################################################
# descript:  
# 运行方法:  python3 zzcpsordersum CPS提取出xls文件  输出文件(csv)
#            python3 zzcpsordersum CPS提取出xls文件
#######################
# filename: zzcpsordersum.py
# author  : chenming
# date    : 2016-009-21
# version : V1.0.0
# note    :
# =====================
# auther  :
# date    :
# modify  :
# version :
# note    :
#
################################################################################

import sys
import os
import re
import xlrd
from operator import itemgetter
from datetime import datetime
from xlrd import xldate_as_tuple
# import xlwt

PRT_NONE       = 0
PRT_EMERG      = 1
PRT_ALERT      = 2
PRT_CRIT       = 3
PRT_ERR        = 4
PRT_WARNING    = 5
PRT_NOTICE     = 6
PRT_INFO       = 7
PRT_DEBUG      = 8

g_print_level = PRT_ERR

def fun_printmark(keyStr="", str="", level=-1):
    l_level = PRT_NONE
    if  level < PRT_NONE:
        l_level = PRT_WARNING
    else:
        l_level = level
    # end set print level

    if l_level <= g_print_level:
        theline=sys._getframe().f_back.f_lineno
        thefile=sys._getframe().f_back.f_code.co_filename
        #thefunc=sys._getframe().f_code.co_name

        level_str=""
        if l_level == PRT_DEBUG:
            level_str = " dbg"
        elif l_level == PRT_INFO:
            level_str = "info"
        elif l_level == PRT_INFO:
            level_str = "noti"
        elif l_level == PRT_INFO:
            level_str = "warn"
        elif l_level == PRT_INFO:
            level_str = "erro"
        elif l_level == PRT_INFO:
            level_str = "crit"
        elif l_level == PRT_INFO:
            level_str = "aler"
        elif l_level == PRT_INFO:
            level_str = "emer"
        # end level_str
        print("==",os.path.basename(thefile),keyStr,"==")
        print(theline, level_str+":" ,str)

    return

def fun_Data2String(data, thelen=0):
    thestr=""

    if( isinstance(data, str) ):
        thestr = data.strip()
    elif( isinstance(data, float) ):
        thestr = str(int(data))
    elif( isinstance(data, int) ):
        thestr = str(data)
    else:
        thestr = ""

    while(1):
        tmp = len(thestr)
        if( tmp >= thelen):
            break

        tmp = thelen - tmp
        while(tmp):
            thestr = thestr + " "
            tmp = tmp - 1

        break
    # end while
    return thestr

def fun_xlsIsTrueFalse(data):
    strtmp = data

    if ("OCSXML_TRUE" == data):
        strtmp = "TRUE"
    elif("OCSXML_FALSE" == data):
        strtmp = "FALSE"
    elif( isinstance(data, int) ):
        if (1 == data):
            strtmp = "TRUE"
        elif(0 == data):
            strtmp = "FALSE"

    return strtmp


SMARTLIST =  \
{
    'MS628':"MSD628_1G",
    'MS628M':"MSD628_512M",
    'MS638':"MSD638",
    'MS338E':"MSD638",
    'MS338':"MSD338",
    'HV310':"HISIV310",
    'HV510':"HISIV510",
    'HV320':"HISIV320",
    'HV530':"HISIV530",
    'HV510':"HISIV510"
}

SMARTTIME = 45
NOOSTIME  = 5
# NOOSLIST = \
# [
#     'V56',
#     'VST59S',
#     'VST59',
#     'VST29',
#     'V56C',
# ]

class OcsList:
    '''
    '''

    def __init__(self, fin_excelfile, fout_csvfile):
        '''
        '''
        self.excelfile = fin_excelfile

        # Y/N/X, 宏定义/空, 路径
        self.csvfile = fout_csvfile

        ##bak  --> 原始数据
        ##data --> 处理后的
        self.datadict = {'bak':{}, 'data':{'smart':{}, 'noos':{}}}
        self.datadict['bak'].update({'board':{}, 'sum':{'CNT':0, 'platform':{}} })
        self.datadict['data']['smart'].update({'board':{}, 'sum':{'CNT':0, 'platform':{}} })
        self.datadict['data']['noos'].update({'board':{}, 'sum':{'CNT':0, 'platform':{}} })

        self.starttime = ""
        self.endtime   = ""
        return

    def step1_LoadExcel(self):
        '''
        从第7行开始读数据
        第一列: 配置生效列. 配置后该行才生成ocs_list.csv
        第二列: OCS属性标记列. 方便更新对比最新发布的OCS_XLS文件
        第三列: OCS属性序号列. 方便更新对比最新发布的OCS_XLS文件
        第四列: 属性名称列. OCS属性名, SW_END标识非OCS标准的自定义数据
        '''

        fun_ret = 0

        try:
            xls = xlrd.open_workbook(self.excelfile, encoding_override="GBK")
            sh = xls.sheet_by_index(0)
        except Exception as e:
            fun_printmark("ERR", e, PRT_ERR)

        # print(sh.nrows) # 行
        # print(sh.ncols) # 列

        maxrows = sh.nrows
        maxcols = sh.ncols
        # 从第8行开始, 索引值从0开始

        try:

            starttime = sh.cell_value(0, 1)
            endtime   = sh.cell_value(0, 2)
            if (starttime == "" or endtime == ""):
                fun_printmark("ERR", "时间未设置", PRT_ERR)
                print("==ERR: XLS文件cell(0, 1), cell(0,2) 必须为时间格式. 如2016/09/20")
                print("==ERR: starttime ", starttime)
                print("==ERR: endtime   ", endtime)
                return 1

            if( not isinstance(starttime, float) or not isinstance(endtime, float)):
                fun_printmark("ERR", "时间格式错误", PRT_ERR)
                print("==ERR: XLS文件cell(0, 1), cell(0,2) 必须为时间格式. 如2016/09/20")
                print("==ERR: starttime ", starttime)
                print("==ERR: endtime   ", endtime)
                return 1

            starttime = datetime(*xldate_as_tuple(starttime,0) )
            endtime   = datetime(*xldate_as_tuple(endtime,0) )
        except:
            fun_printmark("ERR", e, PRT_ERR)
            print("==ERR: XLS文件cell(0, 1), cell(0,2) 必须为时间格式. 如2016/09/20")
            return 1
        ## 

        self.starttime = starttime.strftime("%Y-%m-%d")
        self.endtime   = endtime.strftime("%Y-%m-%d")
        print("==INFO: ",self.starttime, self.endtime)

        if self.csvfile == "NONE":
            tmp_str = "cpstotal_" + str(self.starttime) + "_" + str(self.endtime) + ".csv"
            basepath= os.path.dirname(self.excelfile)
            self.csvfile = os.path.join(basepath, tmp_str.replace("-", ""))

        row_start = 1

        col_board   = 1
        col_count   = 2
        col_ratio   = 3

        sum_cnt = 0
        for row in range(row_start, maxrows):

            board     = fun_Data2String(sh.cell_value(row, col_board))
            count     = fun_Data2String(sh.cell_value(row, col_count))
            ratio     = sh.cell_value(row, col_ratio)

            ## 跳过汇总行
            if "总计" == board:
                continue

            if board.startswith('TP.'):
                platform  = board.split('.')[1]
            elif board.startswith('T.'):
                platform  = board.split('.')[1]
            elif board.startswith('MP.'):
                platform  = board.split('.')[1]
            elif board.startswith('A.'):
                platform  = board.split('.')[1]
            else:
                platform  = board.split('.')[0]

            try:


                self.datadict['bak']['board'].update({board:{'NAME':board, 'CNT':count, 'RATIO':ratio, 'platform':platform}})
                sum_cnt   = sum_cnt + int(count, 10)
                if not platform in self.datadict['bak']['sum']['platform']:
                    tmp_cnt = 0
                else:
                    tmp_cnt = self.datadict['bak']['sum']['platform'][platform]

                tmp_cnt = tmp_cnt + int(count, 10)
                self.datadict['bak']['sum']['platform'].update({platform:tmp_cnt})
            except:
                fun_printmark("ERR", e, PRT_ERR)
                print("==ERR: not identify board name   ", board)
                fun_ret = fun_ret + 1
                continue
            # print(self.datadict['bak']['board'][board])

        ## end for
        self.datadict['bak']['sum'].update({'CNT':sum_cnt})
        print("==INFO: ",self.datadict['bak']['sum'])
        

        ## 板型分类
        smartdict = self.datadict['data']['smart']
        noosdict  = self.datadict['data']['noos']
        for board in self.datadict['bak']['board']:
            theplat = self.datadict['bak']['board'][board]['platform']
            if theplat in SMARTLIST:
                smartdict['board'].update({board:self.datadict['bak']['board'][board]})
            else:
                noosdict['board'].update({board:self.datadict['bak']['board'][board]})
        ## end

        sum_cnt = 0
        datadict = smartdict

        for board in datadict['board']:
            thecnt  = int(datadict['board'][board]['CNT'], 10)
            sum_cnt = sum_cnt + thecnt
            platform = datadict['board'][board]['platform']
            if not platform in datadict['sum']['platform']:
                tmp_cnt = thecnt
                datadict['sum']['platform'].update({platform:0})
            else:
                tmp_cnt = datadict['sum']['platform'][platform] + thecnt

            # print(platform, datadict['sum']['platform'][platform], thecnt, tmp_cnt)
            datadict['sum']['platform'].update({platform:tmp_cnt})
        ##
        datadict['sum'].update({'CNT':sum_cnt})
        # print(datadict['sum'])

        sum_cnt = 0
        datadict = noosdict
        for board in datadict['board']:
            thecnt  = int(datadict['board'][board]['CNT'], 10)
            sum_cnt = sum_cnt + thecnt
            platform = datadict['board'][board]['platform']
            if not platform in datadict['sum']['platform']:
                tmp_cnt = thecnt
            else:
                tmp_cnt = datadict['sum']['platform'][platform] + thecnt
            datadict['sum']['platform'].update({platform:tmp_cnt})
        ##
        datadict['sum'].update({'CNT':sum_cnt})
        ## 输出数据

        return fun_ret

    def step2_OutCVS(self):
        '''
        '''
        fun_ret = 0

        alldict   = self.datadict['bak']
        smartdict = self.datadict['data']['smart']
        noosdict  = self.datadict['data']['noos']
        smartcnt  = smartdict['sum']['CNT']
        nooscnt   = noosdict['sum']['CNT']
        allcnt    = alldict['sum']['CNT']
        with open(self.csvfile,"w", encoding='utf-8') as fw:

            ## 智能机平台
            datadict = self.datadict['data']['smart']
            line = '====,' + str(self.starttime) + "," + str(self.endtime) + "," + "====,\n"
            line += '智能机平台,数量,总占比,分类占比,\n'

            for item in sorted( zip(datadict['sum']['platform'].values(), datadict['sum']['platform'].keys()), reverse=True ):
                platform = item[1]
                cur_cnt  = item[0]
                line += platform +','
                line += str(cur_cnt) + ','
                line += str( cur_cnt / allcnt * 100) + '%,'
                line += str( cur_cnt / smartcnt * 100) + '%,'
                line += '\n'
            fw.write(line)
            ##
            line  = '总计,'
            line += str(smartcnt) + ','
            line += str( smartcnt / allcnt * 100) + '%,'

            cur_cnt = smartcnt * SMARTTIME / 60
            line += str(cur_cnt) + '小时##' +  str(SMARTTIME) + "分/个,"
            line += '\n'
            fw.write(line)

            ## 传统机平台
            datadict = self.datadict['data']['noos']
            line = '====,=====,====,====,\n'
            line += '传统机平台,数量,总占比,分类占比,\n'

            for item in sorted( zip(datadict['sum']['platform'].values(), datadict['sum']['platform'].keys()) ,reverse=True):
                platform = item[1]
                cur_cnt  = item[0]
                line += platform +','
                line += str(cur_cnt) + ','
                line += str( cur_cnt / allcnt * 100)  + '%,'
                line += str( cur_cnt / nooscnt * 100) + '%,'
                line += '\n'
            fw.write(line)
            ##
            line  = '总计,'
            line += str(nooscnt) + ','
            line += str( nooscnt / allcnt * 100) + '%,'
            cur_cnt = nooscnt * NOOSTIME / 60
            line += str(cur_cnt) + '小时##' +  str(NOOSTIME) + "分/个,"
            line += '\n'
            fw.write(line)

            ## 智能机板型
            datadict = self.datadict['data']['smart']
            line = '====,=====,====,====,\n'
            line += '智能机板型,数量,总占比,分类占比\n'

            tmpdict = {}
            for board in datadict['board']:
                tmpdict.update({board:int(datadict['board'][board]['CNT'], 10)})

            for item in sorted( zip(tmpdict.values(), tmpdict.keys()), reverse=True ):
                board   = item[1]
                cur_cnt = item[0]
                line += board +','
                line += str(cur_cnt) + ','
                line += str( cur_cnt / allcnt * 100) + '%,'
                line += str( cur_cnt / smartcnt * 100) + '%,'


                ###
                line += '\n'
            fw.write(line)
            ###

            ## 传统机板型
            datadict = self.datadict['data']['noos']
            line = '====,=====,====,====,\n'
            line += '传统机板型,数量,总占比,分类占比,\n'
      
            tmpdict = {}
            for board in datadict['board']:
                tmpdict.update({board:int(datadict['board'][board]['CNT'], 10)})

            for item in sorted( zip(tmpdict.values(), tmpdict.keys()), reverse=True ):
                board   = item[1]
                cur_cnt = item[0]
                line += board +','
                line += str(cur_cnt) + ','
                line += str( cur_cnt / allcnt * 100) + '%,'
                line += str( cur_cnt / nooscnt * 100) + '%,'
                ###
                line += '\n'
            fw.write(line)
            ###

            ## 总表
            datadict = self.datadict['bak']
            line = '====,=====,====,====,\n'
            line += '所有板型,数量,总占比,,\n'

            tmpdict = {}
            for board in datadict['board']:
                tmpdict.update({board:int(datadict['board'][board]['CNT'], 10)})

            for item in sorted( zip(tmpdict.values(), tmpdict.keys()), reverse=True ):
                board   = item[1]
                cur_cnt = item[0]
                line += board +','
                line += str(cur_cnt) + ','
                line += str( cur_cnt / allcnt * 100) + '%,'

                ###
                line += '\n'
            fw.write(line)
            ###
            line  = '总计,'
            line += str(allcnt) + ','
            line += '100%,\n'
            fw.write(line)

            ## 

        # end write with

        return fun_ret

    def Run(self):
        '''
        '''
        fun_ret = 0
        while(1):
            #
            if self.step1_LoadExcel() != 0:
                fun_ret = 1
                break

            if self.step2_OutCVS() != 0:
                fun_ret = 1
                break

            break

        return fun_ret

if __name__ == '__main__':
    '''
    argv[1] --> input excel file
    argv[2] --> out csv file
    '''

    if(len(sys.argv) < 2):
        fun_printmark("ERR", "Parameters: in_excelfile, out_csvfile", PRT_ERR)
        exit(1)

    excelfile = os.path.abspath(sys.argv[1])
    if(len(sys.argv) >= 3):
        csvfile   = os.path.abspath(sys.argv[2])
    else:
        csvfile   = "NONE"

    if ( not os.path.isfile(excelfile) ):
        fun_printmark("ERR", "excel file not exist: " + excelfile, PRT_ERR)
        exit(1)

    obj = OcsList(excelfile, csvfile)
    ret = obj.Run()
    if ret != 0:
        fun_printmark("ERR", "Run failed : " + excelfile, PRT_ERR)
        exit(1)

    exit(0)



