#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
OPT=$DIR/opt$VS_CODE_INSTANCE
mkdir -p $OPT
cd $DIR/..
. $DIR/conf.sh


if [ "$1" == "build" ]; then

	cd $(head -n 1 $OPT/exampleFolder)
	west build -d build_$(head -n 1 $OPT/exampleBoard) -b $(head -n 1 $OPT/exampleBoard)

elif [ "$1" == "rebuild" ]; then

	cd $(head -n 1 $OPT/exampleFolder)
	west build -d build_$(head -n 1 $OPT/exampleBoard) -b $(head -n 1 $OPT/exampleBoard) -t clean
	west build -d build_$(head -n 1 $OPT/exampleBoard) -b $(head -n 1 $OPT/exampleBoard)

elif [ "$1" == "purge" ]; then

	cd $(head -n 1 $OPT/exampleFolder)
	rm -Rf build_$(head -n 1 $OPT/exampleBoard)
	west build -d build_$(head -n 1 $OPT/exampleBoard) -b $(head -n 1 $OPT/exampleBoard)

elif [ "$1" == "menuconfig" ]; then

	cd $(head -n 1 $OPT/exampleFolder)
	west build -d build_$(head -n 1 $OPT/exampleBoard) -b $(head -n 1 $OPT/exampleBoard) -t menuconfig

elif [ "$1" == "flash" ]; then

	cd $(head -n 1 $OPT/exampleFolder)
	west flash -d build_$(head -n 1 $OPT/exampleBoard)

elif [ "$1" == "checkpatch" ]; then

	cd $2
	git diff $3 | $ZEPHYR_BASE/scripts/checkpatch.pl -
	echo $3 > /tmp/-build-vscode-checkpatch-tmp.txt
	cat $OPT/checkpatchBase >> /tmp/-build-vscode-checkpatch-tmp.txt
	cat /tmp/-build-vscode-checkpatch-tmp.txt | head -20 | awk '!seen[$0]++' > $OPT/checkpatchBase

elif [ "$1" == "mru" ]; then

	cat $OPT/$2
	echo $3

elif [ "$1" == "mruSet" ]; then # $2 - list name, $3 - MRU max count, $4 - value or custom text, $5 value if previous was custom text

	case "$4" in  
	*\ * )
		VALUE=$5
	;;
	*)
		VALUE=$4
	;;
	esac

	if [ "$VALUE" == "[[input]]" ]; then
		printf "Enter a new value: "
		IFS= read VALUE
	fi

	echo $VALUE > /tmp/-build-vscode-mru-tmp.txt
	cat $OPT/$2 >> /tmp/-build-vscode-mru-tmp.txt
	cat /tmp/-build-vscode-mru-tmp.txt | head -$3 | awk '!seen[$0]++' > $OPT/$2

	echo Current MRU list:
	cat $OPT/$2
	echo
	echo \"$2\" changed to:
	echo $VALUE

else

	echo "Unknown command"

fi
