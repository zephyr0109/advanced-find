#!/bin/bash

# plugin name
PLUGIN_NAME="advancedfind"
APP_NAME="advancedfind"
# plugin install path for all user
PLUGIN_PATH_ALL=/usr/lib/gedit/plugins
# plugin install path for current user
PLUGIN_PATH_USER=~/.local/share/gedit/plugins
# plugin configuarion path for current user
CONFIG_PATH_USER=~/.local/share/gedit/plugins
# plugin locale path
LOCALE_PATH=/usr/share/locale

read -p "Install plugin for all user? Root privilege is necessary. (y/n) : " all_flg
if [ "${all_flg}" == "Y" ] || [ "${all_flg}" == "y" ]; then
	# gedit plugin directory
	PLUGIN_DEST=${PLUGIN_PATH_ALL}
	# create plugin folder
	sudo mkdir -p ${PLUGIN_DEST}
	# remove old plugin
	sudo rm -rf ${PLUGIN_DEST}/${PLUGIN_NAME}*
	# install the plugin
	sudo cp -rv ${PLUGIN_NAME}* ${PLUGIN_DEST}
	
	#CONFIG_DEST=${CONFIG_PATH_USER}
	#mkdir -p ${CONFIG_DEST}/${PLUGIN_NAME}
	#cp -rv ${PLUGIN_NAME}/config ${CONFIG_DEST}/${PLUGIN_NAME}
	
elif [ "${all_flg}" == "N" ] || [ "${all_flg}" == "n" ]; then
	# gedit plugin directory
	PLUGIN_DEST=${PLUGIN_PATH_USER}
	CONFIG_BACKUP_DEST=${PLUGIN_DEST}/"bak_"${PLUGIN_NAME}
	# create plugin folder
	mkdir -p ${PLUGIN_DEST}
	# backup config
	mkdir -p ${CONFIG_BACKUP_DEST}
	cp -rv ${PLUGIN_DEST}/${PLUGIN_NAME}/config ${CONFIG_BACKUP_DEST}
	# remove old plugin
	rm -rf ${PLUGIN_DEST}/${PLUGIN_NAME}*
	# install the plugin
	cp -rv ${PLUGIN_NAME}* ${PLUGIN_DEST}
	
	read -p "Keep old configuration?(y/n) : " cfg_flg
	if [ "${cfg_flg}" == "Y" ] || [ "${cfg_flg}" == "y" ]; then
		cp -rv ${CONFIG_BACKUP_DEST}/config ${PLUGIN_DEST}/${PLUGIN_NAME}
	fi
	rm -rf ${CONFIG_BACKUP_DEST}
	
else
	echo "Unknown choice. Exit without installing plugin."
	exit 0
fi

read -p "Install optional language support? Rroot privilege is necessary. (y/n) : " lang_flg
if [ "${lang_flg}" == "Y" ] || [ "${lang_flg}" == "y" ]; then
	LOCALE_DEST=${LOCALE_PATH}
	sudo cp -rv ${PLUGIN_NAME}/locale/* ${LOCALE_DEST}
elif [ "${lang_flg}" == "N" ] || [ "${lang_flg}" == "n" ]; then
	echo "Optional language support will not install."
else
	echo "Unknown choice. Optional language support will not install."
fi

echo "Installation completed."

