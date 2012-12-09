#!/bin/bash


PLUGIN_NAME="advanced_find"
MODULE="advancedfind"

#ver_code=$(zenity --entry --title="Version" --text="Enter the version code : " --entry-text="")
#if [ "${ver_code}" == "" ]; then
	#exit
#fi

# show current version code
grep -E "Version\s*=.+$" ../src/${MODULE}.plugin

# enter plugin version code
read -p "Enter the plugin version code : " ver_code

# update plugin description
sed -r -i "s/Version *=.+$/Version=${ver_code}/g" ../src/${MODULE}.plugin
#cat ../src/${MODULE}.plugin


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

