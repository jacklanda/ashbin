#!/bin/bash
if [ $# -lt 1 ]; then
	echo "usage: sh process.sh inputfile "
	exit
fi
input_dir=$1
SEND_THREAD_NUM=36
tmp_fifofile="/tmp/$$.fifo"
mkfifo "$tmp_fifofile"
exec 6<>"$tmp_fifofile"
for ((i=0;i<$SEND_THREAD_NUM;i++))
do
	echo
done >&6
#for file in `ls ${input_dir}/*`
path=`readlink -f  ${input_dir}`
for file in `cat ${input_dir}`
do
	read -u6
{
	echo $file, $$
	python jiebaseg.py $file
	python2 preprocess.py ${file}.seg ${file}.seg.quanjiao
	iconv -c -f utf8 -t gbk ${file}.seg.quanjiao > ${file}.gbk
	rm ${file}.seg.quanjiao
	echo >&6
}&
done
wait
exec 6>&-
exit 0

#file=$1
#sed -i -e 's/。/\n/g' -e 's/！/\n/g' -e 's/？/\n/g' -e 's/｡/\n/g' -e 's/^\s\+//g' -e '/^\s*$/d' ${file}
#python cn_tn.py ${file} ${file}.norm


