#/bin/sh
string=`pwd`
string=${string//\//_}.filenametags
string="/home/zhengxiasong/tags/lookuptags/"$string
echo -e "!_TAG_FILE_SORTED\t2\t/2=foldcase/"   > $string
find . -not -regex '.*\.\(png\|gif\|apk\|db\)'  ! -path "*svn*" -type f -printf "%f\t%p\t1\n" |sort -f >> $string

pwd=`pwd`
sed -i  "s+\.\/+$pwd\/+g" $string

