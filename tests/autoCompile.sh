#!/bin/bash
set -x

if [ `id -u` -ne 0 ]; then
	echo "Must be run as root" >&2
	exit 1
fi

BRO_DIR=$HOME/src/capstone-code/bro-src/
PLUGIN_DIR=$BRO_DIR/../bro/
LOGFILE="`pwd`/compileTest.log"


rm -r /usr/local/bro/
pushd $BRO_DIR
	git fetch -a
	for ver in `git tag -l | grep -e 'v[0-9.]\{1,\}$'`; do
		printf "\n-----------\nCompiling Bro Version %s \n----------\n" "$ver" 2>&1 | tee -a $LOGFILE
		git checkout $ver
		rm -rf ./*
		git checkout HEAD .
		git submodule update --init --recursive
		./configure 2>&1 | tee -a $LOGFILE
		make 2>&1 | tee -a $LOGFILE
		make install 2>&1 | tee -a $LOGFILE
		pushd $PLUGIN_DIR
			make distclean
			./configure --bro-dist="$BRO_DIR" 2>&1 | tee -a $LOGFILE
			make 2>&1 | tee -a $LOGFILE
			make install 2>&1 | tee -a $LOGFILE
		popd
		rm -r /usr/local/bro/
	done

popd

chmod 555 $LOGFILE
