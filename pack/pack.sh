#!/bin/sh


PLUGIN_NAME="advanced_find"

#ver_code=$(zenity --entry --title="Version" --text="Enter the version code : " --entry-text="")
#if [ "${ver_code}" == "" ]; then
	#exit
#fi

read -p "Enter the plugin version code : " ver_code

PACK_NAME=${PLUGIN_NAME}'-'${ver_code}

# create temp folder for plugin
mkdir ${PACK_NAME}
# copy plugin files to temp folder
cp -r ../src/*	${PACK_NAME}
# create plugin package
tar -zcv -f ${PACK_NAME}.tar.gz ${PACK_NAME}/*
# remove temp files
rm -rf ${PACK_NAME}/*
# remove temp folder
rmdir ${PACK_NAME}

