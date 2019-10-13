#########################################################################
# File Name: chinese_/usr/bin/iconv.sh
# Author: ma6174
# mail: ma6174@163.com
# Created Time: 2017年03月14日 18:10:45
#########################################################################
#!/bin/bash

cat /dev/null > /tmp/use_en
test_file=$1
for a in $(/usr/bin/iconv --list)
do
    head -n 5 $test_file | /usr/bin/iconv -f $a -t UTF-8 > /dev/null 2>&1
    if [ $? -eq 0 ] 
    then
        #echo "ok:$a" |tee -a /tmp/use_en
        head -n 5 $test_file | /usr/bin/iconv -f $a -t UTF-8 |sed "s/^/ok $a: /"|tee -a /tmp/use_en
    fi
done
