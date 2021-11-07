#!/bin/sh

start_checking() {
    pycodestyle --show-source $1
}

start_checking_all() {
    find -name "*.py" -exec pycodestyle --show-source {} \;
}

count() {
    find -name "*.py" -exec pycodestyle --count --format='' {} \;
}

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo -e "\033[1;31mYou need to give me the name of the files you want to check, nothing for all or count to count the amount of error.\033[m"
    exit 1
fi

if [ -z "$*" ]; then
	start_checking_all
elif [ "$1" = "count" ]; then
    res=0
    dt=$(date '+%Y_%m_%d_%H_%M_%S')
    filename="output_${dt}.txt"

    count 2> /tmp/${filename} 1> /dev/null
    while read line
    do
	res=$(($line + $res))
    done < /tmp/${filename}
    echo "TOTAL: $res"
#    if ! [ "$res" -eq 0 ]; then
#	exit 1
#    fi
else
    for arg in "$@"; do
	if [ "$arg" != "$0" ]; then
	    start_checking "$arg"
	fi
    done
fi
