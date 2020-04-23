#!/bin/bash

if [ "$1" == "empty" ]; then exit; fi

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR/..

OPT=$DIR/opt$VS_CODE_INSTANCE
mkdir -p $OPT
touch $OPT/checkpatchBase
touch $OPT/exampleBoard
touch $OPT/exampleFolder

if [[ ! -e $(head -n 1 $OPT/exampleFolder)/Makefile ]]; then
	WEST=west
	MAKE="$DIR/build.sh empty"
else
	WEST="$DIR/build.sh empty"
	MAKE="make --jobs=$(nproc)"
fi

if [ "$1" == "build" ]; then

	cd $(head -n 1 $OPT/exampleFolder)
	$WEST build -d build_$(head -n 1 $OPT/exampleBoard) -b $(head -n 1 $OPT/exampleBoard)
	$MAKE all

elif [ "$1" == "rebuild" ]; then

	cd $(head -n 1 $OPT/exampleFolder)
	$WEST build -d build_$(head -n 1 $OPT/exampleBoard) -b $(head -n 1 $OPT/exampleBoard) -t clean
	$WEST build -d build_$(head -n 1 $OPT/exampleBoard) -b $(head -n 1 $OPT/exampleBoard)
	$MAKE clean
	$MAKE all

elif [ "$1" == "purge" ]; then

	cd $(head -n 1 $OPT/exampleFolder)
	rm -Rf build_$(head -n 1 $OPT/exampleBoard)
	$WEST build -d build_$(head -n 1 $OPT/exampleBoard) -b $(head -n 1 $OPT/exampleBoard)
	$MAKE clean
	$MAKE all

elif [ "$1" == "menuconfig" ]; then

	cd $(head -n 1 $OPT/exampleFolder)
	$WEST build -d build_$(head -n 1 $OPT/exampleBoard) -b $(head -n 1 $OPT/exampleBoard) -t menuconfig

elif [ "$1" == "flash" ]; then

	cd $(head -n 1 $OPT/exampleFolder)
	$WEST flash -d build_$(head -n 1 $OPT/exampleBoard)
	$MAKE flash

elif [ "$1" == "checkpatch" ]; then

	cd $2
	git diff $3 | $ZEPHYR_BASE/scripts/checkpatch.pl -
	echo $3 > /tmp/-build-vscode-checkpatch-tmp.txt
	cat $OPT/checkpatchBase >> /tmp/-build-vscode-checkpatch-tmp.txt
	cat /tmp/-build-vscode-checkpatch-tmp.txt | head -20 | awk '!seen[$0]++' > $OPT/checkpatchBase

elif [ "$1" == "mru" ]; then

	head -n 1 $OPT/$2 > /tmp/-build-vscode-mru-tmp.txt
	for DIR in $OPT/../opt*/ ; do
		head -n 1 $DIR$2 >> /tmp/-build-vscode-mru-tmp.txt
	done
	cat $OPT/$2 >> /tmp/-build-vscode-mru-tmp.txt
	for DIR in $OPT/../opt*/ ; do
		cat $DIR$2 >> /tmp/-build-vscode-mru-tmp.txt
	done
	cat /tmp/-build-vscode-mru-tmp.txt | awk '!seen[$0]++' > $OPT/$2
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

elif [ "$1" == "instance" ]; then

	case "$2" in  
	*\ * )
		printf "Enter a new title: "
		IFS= read TITLE
		echo $TITLE > /tmp/-build-vscode-mru-tmp.txt
		cat $OPT/../opt/instanceTitles >> /tmp/-build-vscode-mru-tmp.txt
		cat /tmp/-build-vscode-mru-tmp.txt | head -$3 | awk '!seen[$0]++' > $OPT/../opt/instanceTitles
	;;
	*)
		TITLE=$2
	;;
	esac

	for NUMBER in 1 2 3 4 5 6 7 8 9 10; do
		echo Checking instance slot $NUMBER
		mkdir -p ~/vscode_instances/$NUMBER
		set +e
		code -s --user-data-dir ~/vscode_instances/$NUMBER | grep "Please run it again" > /dev/null
		RESULT=$?
		set -e
		if [ "$RESULT" == "0" ]; then
			echo "Free slot $NUMBER"
			break
		fi
	done
	echo Starting instance $NUMBER
	cp ~/.config/Code/User/settings.json ~/vscode_instances/$NUMBER/User/settings.json
	set +e
	grep "window.title" ~/vscode_instances/$NUMBER/User/settings.json > /dev/null
	if [ "$?" != "0" ]; then
		echo "WARNING !!!!"
		echo "Set window.title setting in main VS Code instance and restart all instances to correctly show window title!!!"
		echo "Go to File - Preferences - Settings, search for window.title and add anything after \${dirty}"
	fi
	set -e
	sed -i -E -e "s/(\\\$\{dirty\})([^\\\$]*?)(\\\$\{separator\})?/\1$TITLE\$\{separator\}/g" ~/vscode_instances/$NUMBER/User/settings.json
	VS_CODE_INSTANCE=$NUMBER code --user-data-dir ~/vscode_instances/$NUMBER

elif [ "$1" == "serials" ]; then

	set +e
	echo > /tmp/-build-vscode-mru-tmp.txt
	dmesg | grep -o -E 'tty[a-zA-Z_0-9]+' | while read -r PORT ; do
		echo $PORT >> /tmp/-build-vscode-mru-tmp.txt
	done
	cat /tmp/-build-vscode-mru-tmp.txt | sort | awk '!seen[$0]++' > /tmp/-build-vscode-mru-tmp2.txt
	SERIAL_PATTERN='[0]*([1-9][0-9]+)'
	cat /tmp/-build-vscode-mru-tmp2.txt | while read -r PORT ; do
		if [ "$PORT" == "" ]; then continue; fi
		SER=`/bin/udevadm info --name=/dev/$PORT | grep -o -E 'ID_SERIAL_SHORT\s*=\s*[0-9]*'`
		[[ $SER =~ $SERIAL_PATTERN ]]
		SER=${BASH_REMATCH[1]}
		if [ "$SER" != "" ]; then SER=" - $SER"; fi
		echo $PORT$SER
	done

elif [ "$1" == "term" ]; then

	echo terminal $2
	minicom -b 115200 -D /dev/$2 -c on

elif [ "$1" == "comments" ]; then

	if [ "$2" == "off" ]; then
		sed -i -E -e "s/\"(editor\.tokenColorCustomizations)\"/\"---\1\"/g" $DIR/settings.json
	elif [ "$2" == "on" ]; then
		sed -i -E -e "s/\"---(editor\.tokenColorCustomizations)\"/\"\1\"/g" $DIR/settings.json
	fi

else

	echo "Unknown command"

fi
