#!/bin/bash
DIRLISTFILE=~/.dirlist
dirlist=()
dircnt=0
function LoadDirList()
{
	while read line
	do
		if [ "$line" == "" ]; then
			continue
		fi

		ind=0
		found=0
		while [ $ind -lt $dircnt ]
		do
			if [ "$line" == "${dirlist[$i]}" ]; then
				found=1
				break
			fi
			ind=`expr $ind + 1`
		done

		if [ $found -eq 1 ]; then
			continue
		fi

		if [ ! -d $line ]; then
			echo -e "!Error: Invalid Directory Item $line"
			continue
		fi
		dirlist[$dircnt]=$line				 
		dircnt=`expr $dircnt + 1`
	done < $DIRLISTFILE				
}
function ShowDirList()
{
	ind=0
	while [ $ind -lt $dircnt ]
	do
		echo -e "$ind `basename ${dirlist[$ind]}` --->  ${dirlist[$ind]} \n"
		ind=`expr $ind + 1`
	done	
}
function DumpDirList()
{
	TMPFILE=	mp/`date +%Y%m%d%H%M%S`
	ind=0
	while [ $ind -lt $dircnt ]
	do	
		if [ "AAA${dirlist[$ind]}" != "AAA" ]; then
			echo ${dirlist[$ind]} >> $TMPFILE
		fi
		ind=`expr $ind + 1`
	done	

	sort $TMPFILE > $DIRLISTFILE
	unlink $TMPFILE
}
function AddCurrentDir()
{
	curdir=`pwd`

	LoadDirList

	found=0
	ind=0
	while [ $ind -lt $dircnt ]
	do
		if [ "$curdir" == "${dirlist[$ind]}" ]; then
			found=1
			break
		fi
		ind=`expr $ind + 1`
	done

	if [ $found -eq 0 ]; then
		dirlist[$dircnt]=$curdir
		dircnt=`expr $dircnt + 1`
	fi
	DumpDirList
}
function SubCurrentDir()
{
	curdir=`pwd`
	LoadDirList
	ind=0
	while [ $ind -lt $dircnt ]
	do
		if [ $curdir == ${dirlist[$ind]} ]; then
			dirlist[$ind]=""
			break
		fi
		ind=`expr $ind + 1`
	done

	DumpDirList	
}
function SelectDirectory()
{
	echo -e "Please Select Item From Followings ... \n"
	LoadDirList 

	ShowDirList
	jump=""

	echo -n "select: "
	while read line
	do
		line=`echo $line | awk '{print $1}'`
		if [ "$line" == "" ]; then
			break
		fi
		ind=0
		found=0
		while [ $ind -lt $dircnt ]
		do
			if [ $line == $ind ]; then
				found=1
				break
			fi
			ind=`expr $ind + 1`
		done
		if [ $found -eq 0 ]; then
			echo -e "Invalid Input! "
			echo -n "select: "
			continue
		fi
		jump=${dirlist[$ind]}
		break
	done

	if [[ "$jump" != "" && -d $jump ]]; then
		cd $jump
	fi
}
function ShowHelp()
{
	echo "Usage:"
	echo -e "	z + : Add Current Directory To List"
	echo -e "	z - : Delete Currrent Directory From List"
	echo -e "	z   : Show or Select Directory"
	return 0
}
touch $DIRLISTFILE
if [ $# -eq 0 ];
then
	SelectDirectory
else
	case "$1" in
		"+")
			AddCurrentDir ;;
		"-")
			SubCurrentDir ;;
		"h")
			ShowHelp ;;
	esac
fi


