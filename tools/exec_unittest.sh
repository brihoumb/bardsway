#!/bin/sh

move_tests() {
	echo "\033[1;34mMove unittest files ... \033[1;31m"
	cp ./unittest/*.py ./algorithm || echo "\033[m" && return 1
	return 0
}

remove_test() {
	echo "\033[1;34mRemove unittest files ... \033[m"
	find ./algorithm -name "*_unittest.py" -delete
	return 0
}

main() {
	if [ "$1" = "move" ]
	then
		move_tests
	elif [ "$1" = "remove" ]
	then
		remove_test
	else
		return 0
	fi
	return 0
}; main $1
