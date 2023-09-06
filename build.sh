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

if [ "$1" == "checkpatch" ]; then

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
	echo "[[empty]]"
	echo "$3"

elif [ "$1" == "mruSet" ]; then # $2 - list name, $3 - MRU max count, $4 - value or custom text, $5 value if previous was custom text

	case "$4" in  
	+\ \ \ * )
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
	if [ "$VALUE" == "[[empty]]" ]; then
		VALUE=
	fi

	echo $VALUE > /tmp/-build-vscode-mru-tmp.txt
	cat $OPT/$2 >> /tmp/-build-vscode-mru-tmp.txt
	cat /tmp/-build-vscode-mru-tmp.txt | head -$3 | awk '!seen[$0]++' > $OPT/$2

	echo Current MRU list:
	cat $OPT/$2
	echo
	echo \"$2\" changed to:
	echo $VALUE

elif [ "$1" == "comments" ]; then

	if [ "$2" == "off" ]; then
		sed -i -E -e "s/\"(editor\.tokenColorCustomizations)\"/\"---\1\"/g" $DIR/settings.json
	elif [ "$2" == "on" ]; then
		sed -i -E -e "s/\"---(editor\.tokenColorCustomizations)\"/\"\1\"/g" $DIR/settings.json
	fi

elif [ "$1" == "nrf_rpc_gen" ]; then

	echo node nrf_rpc_generator/main.js --clang-path=/home/doki/work/apps/clang \"$2\"
	#node nrf_rpc_generator/main.js --dump-ast --clang-path=/home/doki/work/apps/clang /dk/ncs/nrf/subsys/bluetooth/rpc/client/bt_rpc_gatt_cli.c
	node nrf_rpc_generator/main.js --clang-path=/home/doki/work/apps/clang "$2"

elif [ "$1" == "nrf_rpc_gen_prev" ]; then

	tmp_dir=`mktemp -d /tmp/XXXXXXXXXX`
	cp "$2" $tmp_dir/OLD.c
	echo node nrf_rpc_generator/main.js --clang-path=/home/doki/work/apps/clang \"$2\"
	node nrf_rpc_generator/main.js --clang-path=/home/doki/work/apps/clang "$2"
	cp "$2" $tmp_dir/NEW.c
	node nrf_rpc_generator/strip.js $tmp_dir
	if cmp -s $tmp_dir/OLD.c $tmp_dir/NEW.c; then
		echo There are no changes > $tmp_dir/OLD.c
		echo There are no changes > $tmp_dir/NEW.c
	fi
	if [ -z ${VS_CODE_INSTANCE+x} ]; then
		code -r -d $tmp_dir/OLD.c $tmp_dir/NEW.c
	else
		code --user-data-dir ~/vscode_instances/$NUMBER -r -d $tmp_dir/OLD.c $tmp_dir/NEW.c
	fi

elif [ "$1" == "docs" ]; then

	cd $DIR/../nrf/doc

	if [ "$2" == "+" ]; then
		rm -Rf build_doc || true
		kb_per_job=$((3 * 1024 * 1024))
		cpu_count=`nproc`
		mem_kb=`grep MemAvailable /proc/meminfo | awk '{print $2}'`
		max_jobs=$((kb <= kb_per_job ? 1 : kb / kb_per_job))
		max_jobs=$((cpu_count < max_jobs ? cpu_count : max_jobs))
		cmake -DSPHINXOPTS_DEFAULT="-j $max_jobs" -GNinja -S. -Bbuild_doc
	fi

	cd build_doc

	shopt -s globstar
	case "$2" in
	nrf/**) T=nrf-all;;
	zephyr/**) T=zephyr-all;;
	nrfxlib/**) T=nrfxlib-all;;
	modules/hal/nordic/nrfx/**) T=nrfx-all;;
	-) T=;;
	+) T=;;
	*) echo Cannot detect module based on file path!
		exit 1
		;;
	esac

	if [ -z "$T" ]
	then
		echo Building everything...
		ninja
	else
		echo Building target $T to refresh file $2
		ninja -t commands $T > /tmp/build_commands.txt
		echo "#!/bin/bash" > /tmp/build_commands.sh
		tail -n 1 /tmp/build_commands.txt >> /tmp/build_commands.sh
		chmod 755 /tmp/build_commands.sh
		/tmp/build_commands.sh
	fi

elif [ "$1" == "docs_server" ]; then

	python3 $DIR/docs_server/serv.py 8178 $DIR/../nrf/doc/build_doc/html

else

	echo "Unknown command"

fi
