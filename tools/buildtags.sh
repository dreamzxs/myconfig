#/bin/sh
string=`pwd -P`
ctags=${string//\//_}.tags
ctagsstring="/home/zhengxiasong/tags/lookuptags/"$ctags
echo "Now is building ctags"
start=$(date +%s)  
ctags -R --tag-relative -f $ctagsstring


echo "Now is building cscope tags"

cscope_tags=${string//\//_}.cscope_file
cscope_string="/home/zhengxiasong/tags/lookuptags/"$cscope_tags

find `pwd` -type f -iname "*.c" -o -type f -iname "*.h" -o -type f -iname "*.cpp" -o -type f -iname "*.java" -o -type f -iname "*.sh"  > cscope.files
cscope -bq -i cscope.files -f $cscope_string

echo "Now is building filenametags"

end=$(date +%s) 
time=$(( $end - $start )) 
echo Total time:$time


echo "finish"
