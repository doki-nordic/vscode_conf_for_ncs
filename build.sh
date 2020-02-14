#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR/..
. $DIR/conf.sh

if [ "$1" == "build" ]; then

	cd $EXAMPLE_DIR
	west build -d build_$EXAMPLE_BOARD -b $EXAMPLE_BOARD

elif [ "$1" == "rebuild" ]; then

	cd $EXAMPLE_DIR
	west build -d build_$EXAMPLE_BOARD -b $EXAMPLE_BOARD -t clean
	west build -d build_$EXAMPLE_BOARD -b $EXAMPLE_BOARD

elif [ "$1" == "purge" ]; then

	cd $EXAMPLE_DIR
	rm -Rf build_$EXAMPLE_BOARD
	west build -d build_$EXAMPLE_BOARD -b $EXAMPLE_BOARD

elif [ "$1" == "menuconfig" ]; then

	cd $EXAMPLE_DIR
	west build -d build_$EXAMPLE_BOARD -b $EXAMPLE_BOARD -t menuconfig

elif [ "$1" == "flash" ]; then

	cd $EXAMPLE_DIR
	west flash -d build_$EXAMPLE_BOARD

elif [ "$1" == "checkpatch" ]; then

	cd $2
	git diff $3 | $ZEPHYR_BASE/scripts/checkpatch.pl -
	echo $3 > /tmp/-build-vscode-checkpatch-tmp.txt
	cat $DIR/opt/checkpatchBase >> /tmp/-build-vscode-checkpatch-tmp.txt
	cat /tmp/-build-vscode-checkpatch-tmp.txt | head -10 | awk '!seen[$0]++' > $DIR/opt/checkpatchBase

elif [ "$1" == "getExampleDir" ]; then

	echo $EXAMPLE_DIR

elif [ "$1" == "getExampleBoard" ]; then

	echo $EXAMPLE_BOARD

elif [ "$1" == "getCheckpatchBase" ]; then

	cat $DIR/opt/checkpatchBase
	echo HEAD

else

	echo "Unknown command"

fi
