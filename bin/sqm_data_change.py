#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os
import sys
import json
import datetime

queryPrjCmd = "curl \"http://172.17.84.185:9090/api/projects/index?format=json\" 2>/dev/null"
product = {"oversea":["MSD3463", "MSD3563", "MSD6486", "MSD6488", "MSD6586", "_OVERSEA"], \
"common":["MSD3553_", "V56_", "_COMMON"], \
"smart":["MSD338", "MSD638", "MSD648_", "Hisi", "_SMART"]}

def excuteCmd(cmd):
	rc = os.popen(cmd, 'r')
	result = rc.read()
	rc.close()
	return result

class QueryProjects:
	"""get projects on SQM """
	def __init__(self):
		self.overseaPrjList = list()
		self.commonPrjList = list()
		self.smartPrjList = list()
		self.prjs = list()

		res = excuteCmd(queryPrjCmd)
		prjs = json.loads(res)
		for i in range(0, prjs.__len__()):
			prj = prjs[i]['k']
			self.prjs.append(prjs[i]['k'])
			for j in range(0, len(product["oversea"])) :
				if prj.__contains__(product["oversea"][j]) :
					self.overseaPrjList.append(prj)
					break
			for j in range(0, len(product["common"])) :
				if prj.__contains__(product["common"][j]) :
					self.commonPrjList.append(prj)
					break
			for j in range(0, len(product["smart"])) :
				if prj.__contains__(product["smart"][j]) :
					self.smartPrjList.append(prj)
					break

	def getOversea(self):
		return self.overseaPrjList

	def getCommon(self):
		return self.commonPrjList

	def getSmart(self):
		return self.smartPrjList

	def getPrjs(self):
		return self.prjs

class QueryMeasure:
	"""get measure result"""
	def __init__(self):
		self.sqmPrjs = QueryProjects()

	def getPrjMeasureByDate(self, prj, date):
		timelineCmd = "curl \"http://172.17.84.185:9090/api/timemachine/index?format=json&&resource=%s"\
		"&&metrics=violations,bugs,vulnerabilities,code_smells&&toDateTime=%s\" 2>/dev/null" % (prj, date)
		rc = excuteCmd(timelineCmd)
		measure_info = json.loads(rc)

		cellsLen = len(measure_info[0]['cells'])
		colLen = len(measure_info[0]['cols'])
		res = dict()

		if cellsLen <= 0:
			return res
		#print "%s Get from %s, cellsLen=%s colLen=%s" %(date, prj, cellsLen, colLen)
		cols = measure_info[0]['cols']
		cell = measure_info[0]['cells'][cellsLen-1]

		res['date'] = date
		for i in range(0, colLen):
			key = cols[i]['metric']
			val = cell['v'][i]
			res[key] = val

		return res

	def getPrjMeasureOrigin(self, prj):
		date = datetime.datetime.today().strftime("%Y-%m-%d")
		timelineCmd = "curl \"http://172.17.84.185:9090/api/timemachine/index?format=json&&resource=%s"\
		"&&metrics=violations,bugs,vulnerabilities,code_smells\" 2>/dev/null" % (prj)
		rc = excuteCmd(timelineCmd)
		measure_info = json.loads(rc)

		cellsLen = len(measure_info[0]['cells'])
		colLen = len(measure_info[0]['cols'])
		res = dict()

		if cellsLen <= 0:
			return res
		#print "%s Get from %s, cellsLen=%s colLen=%s" %(date, prj, cellsLen, colLen)
		cols = measure_info[0]['cols']
		cell = measure_info[0]['cells'][1]

		res['date'] = date
		for i in range(0, colLen):
			key = cols[i]['metric']
			val = cell['v'][i]
			res[key] = val

		return res

############################## main #############################
argc = len(sys.argv)
if argc != 3:
	print "%% Error, arguments error!"
	exit(1)
elif sys.argv[1] == "-h":
	print "Useage : sqm_data_change.py 2016-12-21  2017-01-20> result.csv"
	exit(0)
else:
	dateS = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d')
	dateE = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d')

##这两行解决编码问题    
reload(sys)
sys.setdefaultencoding('utf-8')

productPrjList = {}
queryMeasure = QueryMeasure()
queryProject = QueryProjects()

productPrjList['通用产品线'] = queryProject.getCommon()
productPrjList['智能产品线']= queryProject.getSmart()
productPrjList['海外产品线'] = queryProject.getOversea()

print "%s 至 %s 各项目静态指标变化" % (dateS.strftime("%Y-%m-%d"), dateE.strftime("%Y-%m-%d"))
print "产品线 | 项目名称 |  漏洞月初值 | 当前漏洞 | 漏洞增量 |  BUG月初值 | 当前BUG |  BUG增量 | 坏味道月初值 | 当前坏味道 | 坏味道增量 | SQI月初值 | 当前SQI | SQI增量" 
for productName,productPrjs in productPrjList.items():
	for i in range(0, len(productPrjs)):
		prjNew=""
		dataS = queryMeasure.getPrjMeasureByDate(productPrjs[i], dateS.strftime("%Y-%m-%d"))
		dataE = queryMeasure.getPrjMeasureByDate(productPrjs[i], dateE.strftime("%Y-%m-%d"))
		if dataE.__len__() == 0:
            #print "%s Error!" %(productPrjs[i])
			continue
		if dataS.__len__() == 0:
			dataS = queryMeasure.getPrjMeasureOrigin(productPrjs[i])
			prjNew="本月新增"

		vulDelta = dataE['vulnerabilities'] - dataS['vulnerabilities']
		bugDelta = dataE['bugs'] - dataS['bugs']
		smellDelta = dataE['code_smells'] - dataS['code_smells']
		sqiE = dataE['vulnerabilities']*2 + dataE['bugs'] + dataE['code_smells']*0.2
		sqiS = dataS['vulnerabilities']*2 + dataS['bugs'] + dataS['code_smells']*0.2
		sqiDelta = vulDelta*2 + bugDelta + smellDelta*0.2
		prjName = (productPrjs[i]).replace('_COMMON', '').replace('_SMART', '').replace('_OVERSEA', '').replace(' ', '')

		print "%s | %s | %d | %d | %d | %d | %d| %d | %d | %d | %d | %d | %d | %d" %(productName+prjNew, prjName, dataS['vulnerabilities'], dataE['vulnerabilities'], vulDelta, dataS['bugs'], dataE['bugs'], bugDelta, dataS['code_smells'], dataE['code_smells'], smellDelta, sqiS, sqiE, sqiDelta)





