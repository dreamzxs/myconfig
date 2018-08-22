#!/bin/sh
################################################################################
# Copyright Statement: CVTE
# Copyright (C) 2016 Guangzhou Shiyuan Electronics Co.,Ltd. All rights reserved.
#      ____________        _______________   __________
#     / / ________ \      / / _____   ____| /|  _______|
#    / / /_______/\ \    / / /___/ | |___/ | | |______/
#   | | |        \ \ \  / / /    | | |     | | |_______
#   | | |         \ \ \/ / /     | | |     | |  _______|
#   | | |          \ \ \/ /      | | |     | | |______/
#    \ \ \______    \ \  /       | | |     | | |_______
#     \ \_______|    \ \/        | |_|     | |_________|
#      \/______/      \/         |/_/      |/_________/ 
################################################################################
# descript:
#######################
# author  : luojie
# date    : 2017-06-15
# note    : for package the upload_fw_32bit/upload_fw_64bit
################################################################################


CONST_SYS_BIT=$(getconf LONG_BIT)

#################################
UPLOAD_TOOL=/usr/local/bin/upload_fw_${CONST_SYS_BIT}bit
tempfile=/tmp/tempfile_upload_${RANDOM}.txt

# for old version
FW_SUFFIX=$1
FW_DIR=$2
#

RESULT_TEST=""
RESULT_REMARK=""

#################################

function dialog_select_test_level()
{
	dialog --title "< OCS自动上传脚本 >" \
	--menu "测试类型选择:" 14 40 7 \
	N "无测试类型" \
	A "测" \
	B "测" \
	C "测" \
	D "测" \
	E "测" \
	F "测" 2>$tempfile
	RESULT_TEST=$?
}

function dialog_input_remark()
{

	dialog --title "请输入测试备注" --clear "$@" \
	       --inputbox "注意只支持单行
	       " 10 80 2> $tempfile
	RESULT_REMARK=$?
}

function upload_ocs()
{
	test_type=$1
	remark=$2
    echo "PARAM:[$FW_SUFFIX  $FW_DIR  $test_type]"
    echo "REMARK:[$remark]"
	$UPLOAD_TOOL "$FW_SUFFIX" "$FW_DIR" "$test_type" "$remark"
}	


dialog_select_test_level
if [ "$RESULT_TEST" == "0" ];then
	l_dialog_type=`cat $tempfile`
	dialog_input_remark
	if [ "$RESULT_REMARK" == "0" ];then
		l_dialog_remark=`cat $tempfile`
		upload_ocs "$l_dialog_type" "$l_dialog_remark"
	else
		echo "Note:user cancelled!"
	fi
fi 

rm -f $tempfile

