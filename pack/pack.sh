#!/bin/sh


PLUGIN_NAME="advancedfind"

ver_str=$(zenity --entry --title="Version" --text="Enter the version code : " --entry-text="")
if [ "${ver_str}" == "" ]; then
	exit
fi

tar -zcv -f ${PLUGIN_NAME}'-'${ver_str}.tar.gz ../src/*




