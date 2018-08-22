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
#######################
# filename: extractDataC.py
# author  : chenming
# date    : 2015-04-29
# version : V1.0
# note    :
# =====================
# auther  : chenming
# date    : 2015-0713
# modify  :
# version : V1.1
# note    :
#
################################################################################

import sys
import os
import re
import subprocess

CONST_VER = "V1.1"
def fun_printmark(keyStr="", str=""):
    theline=sys._getframe().f_back.f_lineno
    thefile=sys._getframe().f_back.f_code.co_filename
    #thefunc=sys._getframe().f_code.co_name
    print(theline,os.path.basename(thefile),"==",keyStr,"==")
    print(str)

    return

class pushGits2NewPath:
    '''
    '''
    def __init__(self, codedir, remotedir, en_showlog=True, en_pushenable=False, en_remotebranch=False, en_pushforce=False, en_localstruct=False, filtergitlist=[]):
        '''
        '''
        self.codedir    = codedir
        self.remotedir  = remotedir

        self.en_showlog    = en_showlog
        self.en_pushenable = en_pushenable
        self.en_pushforce  = en_pushforce
        self.en_remotebranch = en_remotebranch
        self.en_localstruct = en_localstruct
        self.filtergitlist  = filtergitlist

        self.repofile   = os.path.join(self.codedir, "zzrepoinfo.txt")

        self.Logfile = os.path.join(self.codedir, "xxpushLog.txt")
        self.LogStr  = ""

        fun_printmark("INFO", "code path")
        print("local  code dir:", self.codedir)
        print("remote code dir:", self.remotedir)

        #num:{lpath:xx, rpath:xx, lbranch:xx, rbranch:xx}
        self.prjdict = {'num':0, 'data':{}}

        return

    def fun_addLogstr(self, thestr):
        self.LogStr += thestr + "\n"
        return

    def fun_updateLogToFile(self):

        with open(self.Logfile, 'w', encoding='utf-8') as fw:
            fw.write(self.LogStr)

        return

    def fun_filter_git(self, name):
        fun_ret = 0

        for idx in range( len(self.filtergitlist) ) :
            if (name == self.filtergitlist[idx]):
                fun_ret = 1
                break

        return fun_ret

    def setp2_getRepoinfoFile(self):
        fun_ret = 0

        os.chdir(self.codedir)
        try:
            subprocess.call("repo info > " + self.repofile ,shell=True)
        except:
            fun_printmark("ERR", "repo info failed")
            fun_ret = 1
            return fun_ret
        self.codedir = os.path.abspath(".")

        if not os.path.isfile(self.repofile):
            fun_printmark("ERR", "not find repoinfo file: " + self.repofile)
            return 1

        with open(self.repofile, "r") as fr:
            rpath = ""
            lpath = ""
            rbranch = ""

            step = 0
            for line in fr:

                ret = re.search(r'^Project:\s+(.*)', line)
                if ret :
                    rpath = ret.group(1)
                    lpath = ""
                    rbranch = ""
                    step = 1
                # find remote path

                ret = re.search(r'^Mount path:\s+(.*)', line)
                if ret:
                    if step == 1:
                        lpath = ret.group(1)
                        step  = 2
                    else:
                        step  = 0
                        lpath = ""
                # find local path

                ret = re.search(r'^Current revision:\s+(.*)', line)
                if ret:
                    if step == 2:
                        rbranch = ret.group(1)
                        step  = 3
                    else:
                        step  = 0
                        lpath = ""
                # find remote branch

                if (rpath != "") and (lpath != "") and (rbranch != ""):

                    lpath = lpath.replace(self.codedir + "/" , "")
                    # print("lpath:", lpath)
                    # print("rpath:", rpath)

                    if (self.fun_filter_git(lpath) == 0 ):
                        # num:{lpath:xx, rpath:xx, lbranch:xx, rbranch:xx}
                        # lpath/rpath 相对路径
                        num = self.prjdict['num'] + 1
                        keyname = str(num)
                        self.prjdict['data'].update({keyname:{}})

                        self.prjdict['data'][keyname].update({'lpath':lpath})
                        self.prjdict['data'][keyname].update({'rpath':rpath})

                        self.prjdict['data'][keyname].update({'rbranch':rbranch})
                        self.prjdict['data'][keyname].update({'lbranch':""})
                        self.prjdict.update({'num':num})
                    else:
                        print("==filter==:", lpath)

                    # clean last time
                    rpath = ""
                    lpath = ""
                    rbranch = ""
                    step  = 0
            # end for
        # end open file

        # print(self.prjdict['data'])
        return fun_ret

    def step3_pushAllProject(self):
        '''
        #num:{lpath:xx, rpath:xx, lbranch:xx, rbranch:xx}
        '''
        fun_ret = 0

        fun_printmark("INFO", self.prjdict['num'])

        cutdict = self.prjdict['data']

        for prj in cutdict:
            lpath = os.path.join(self.codedir, cutdict[prj]['lpath'])
            os.chdir(lpath)

            try:
                tmpstr = 'git branch | grep "^* " | cut -c3-'
                lbranch = subprocess.check_output(tmpstr ,shell=True).decode('utf-8')
                lbranch = lbranch.strip()
            except:
                fun_printmark("ERR", "git failed: " + lpath)
                fun_ret = 1
                tmpstr = "gitfailed:" + lpath
                self.fun_addLogstr(tmpstr)
                continue

            ret = re.search(r"\W+", lbranch)
            if ret:
                continue

            cutdict[prj].update({'lbranch':lbranch})

            tmpstr = "gitsuccess:" + lpath
            self.fun_addLogstr(tmpstr)


            # print(cutdict[prj]['rpath'])
            # print(cutdict[prj]['lpath'])
            # print(cutdict[prj]['rbranch'])
            # print(cutdict[prj]['lbranch'])

        # end find local branch

        # start push project
        pushcnt = 0
        prjcnt  = 0

        manifest = ""
        for prj in cutdict:

            # try:
            #     tmpstr = 'git remote -v show ' + cutdict[prj]['rpath']
            #     lbranch = subprocess.check_output(tmpstr ,shell=True).decode('utf-8')
            #     lbranch = lbranch.strip()
            # except:
            #     fun_printmark("ERR", "git failed: " + lpath)
            #     fun_ret = 1
            #     tmpstr = "gitfailed:" + lpath
            #     self.fun_addLogstr(tmpstr)
            #     continue
            # self.en_showlog = en_showlog
            # self.en_pushgit = en_pushgit
            # self.en_remotebranch = en_remotebranch

            lpathpart2 = cutdict[prj]['lpath']
            lpath   = os.path.join(self.codedir, lpathpart2)
            lbranch = cutdict[prj]['lbranch']

            if (self.en_localstruct):
                rpathpart2 = cutdict[prj]['lpath']
            else:
                rpathpart2 = cutdict[prj]['rpath']

            rpath = os.path.join(self.remotedir, rpathpart2)

            if self.en_remotebranch:
                rbranch = cutdict[prj]['rbranch']
            else:
                rbranch = lbranch

            if self.en_pushforce:
                tmpstr = 'git push ' + rpath + " " + lbranch +":"+rbranch + " -f"
            else:
                tmpstr = 'git push ' + rpath + " " + lbranch +":"+rbranch

            #<project name="sdk_v1/3.1.10_Madison_TVOS" path="kernel"/>
            manifest += '    <project name="'
            manifest += rpathpart2 + '" '
            manifest += 'path="'
            manifest += lpathpart2 + '" />\n'

            if self.en_showlog:
                print(tmpstr)

            self.fun_addLogstr("pushgit:" + tmpstr)
            prjcnt = prjcnt + 1

            if self.en_pushenable:
                os.chdir(lpath)
                try:
                    subprocess.check_output(tmpstr ,shell=True).decode('utf-8')
                except:
                    fun_printmark("ERR", "git push failed: " + lpath)
                    tmpstr = "pushfailed:" + cutdict[prj]['lpath']
                    self.fun_addLogstr(tmpstr)
                    fun_ret = 1
                    continue
            # end push one git
            pushcnt = pushcnt + 1
            # end

        # end for push all project

        # fun_printmark("INFO", "project cnt info")
        # print("prjcnt : ", prjcnt)
        # print("pushcnt: ", pushcnt)
        # print(self.en_pushenable)

        return fun_ret

    def Run(self):
        '''
        '''
        fun_ret = 0

        while(1):

            if self.setp2_getRepoinfoFile() > 0:
                fun_ret = 1
                break

            if self.step3_pushAllProject() > 0:
                fun_ret = 1
                break

            self.fun_updateLogToFile()
            break
        # end while

        return fun_ret

def showHelp():
    # usage: git [--version] [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
    #        [-p|--paginate|--no-pager] [--no-replace-objects] [--bare]
    #        [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
    #        [-c name=value] [--help]
    #        <command> [<args>]

    print("help:")
    print("version: ", CONST_VER)
    print("-s: ", "show log")
    print("-p: ", "push branch to remote")
    print("-f: ", "force push branch, must set -p")
    print("-l: ", "use local folder structure for remote")
    print("-r: ", "user remote branch name for new remote branch name")
    print("-x string1 string2 : ", "filter one git repository")
    return

if __name__ == '__main__':
    '''
    codedir
    remotedir
    -s showlog       --> TRUE: 不显示log, 默认显示
    -p push          --> TRUE: 执行push命令
    -l local         --> TRUE: 按本地相对目录结构创建远程仓库. 默认使用远程相对目录结构
    -f force         --> TRUE: 小心使用.   push local:remote -f .使用 -f参数
    -r remotebranch  --> TRUE: 使用原始的远程仓库名作为新的远程仓库分支名
    -x 过滤  --> 仓库名 : 跳过某些仓库
    '''
    if(len(sys.argv) > 1):
        if ( sys.argv[1].upper() == "HELP" or sys.argv[1].upper() == "-H"):
            showHelp()
            exit(0)

    if(len(sys.argv) < 3):
        print("perameter error")
        showHelp()
        exit(1)

    codedir    = sys.argv[1]
    remotedir  = sys.argv[2]
    if not os.path.isdir(codedir):
        print("local code path not exist!!")
        exit(1)

    try:
        option = sys.argv[3]
    except:
        option = ""

    en_showlog      = True
    en_pushbranch   = False
    en_forcepush    = False
    en_localstruct  = False
    en_remotebranch = False
    filtergitlist   = []

    alloptions = []
    if (option != "" ):
        tmpstr = option.strip()
        idx    = option.find('-',0)
        if idx != -1:
            tmpstr = tmpstr[idx:]
        else:
            tmpstr = ""

        alloptions = tmpstr.split('-')
        # print(alloptions)
    # end get options

    
    # analyse options
    for item in alloptions:
        tmpstr = item.strip()
        try:
            opt = tmpstr[0]
        except:
            opt = ""

        if opt == "" :
            continue
        elif opt == 's':
            # show log
            en_showlog = True
        elif opt == "p":
            # push branch to remote
            en_pushbranch = True
        elif opt == 'l':
            # use local folder structure for remote
            # otherwise usr remote folder structure
            en_localstruct = True
        elif opt == 'f':
            # force push
            en_forcepush = True
        elif opt == 'r':
            # user remote branch name
            en_remotebranch = True
        elif opt == 'x':
            # name = tmpstr[1:].strip()
            itemlists = tmpstr[1:].split(" ")
            for idx in range ( len (itemlists)):
                name = itemlists[idx].strip()
                if name != "":
                    filtergitlist.append(name)
    # print("====", filtergitlist)
    # end analyse options

    if (False == en_pushbranch):
        en_forcepush   = False

    fun_ret = 0
    obj = pushGits2NewPath(codedir,remotedir, en_showlog, en_pushbranch, en_remotebranch, en_forcepush, en_localstruct, filtergitlist)

    while (1):

        if(obj.Run() > 0):
            fun_ret = 1
            break
        ####
        break
    # end while

    if fun_ret > 0:
        exit(1)

    exit(0)


