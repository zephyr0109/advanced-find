#!/bin/bash


# plugin name
PLUGIN_NAME="advancedfind"
# plugin install path for all user
PLUGIN_PATH_ALL=/usr/lib/gedit/plugins/
# plugin install path for current user
PLUGIN_PATH_USER=~/.local/share/gedit/plugins/
# plugin configuarion path for current user
CONFIG_PATH_USER=~/.local/share/gedit/plugins
# plugin locale path
LOCALE_PATH=/usr/share/locale


read -p "Are you sure you want to remove ${PLUGIN_NAME} completedly? Root privilege is necessary. (y/n) : " rm_flg

if [ "${rm_flg}" == "Y" ] || [ "${rm_flg}" == "y" ]; then
	# remove plugin
	echo "Remove plugin files..."
	rm -rf ${PLUGIN_PATH_USER}/${PLUGIN_NAME}*
	sudo rm -rf ${PLUGIN_PATH_ALL}/${PLUGIN_NAME}*

	echo "Remove locale files..."
	sudo rm ${LOCALE_PATH}/*/LC_MESSAGES/"${PLUGIN_NAME}.mo"

	echo "Remove configuration files..."
	rm -rf ${CONFIG_PATH_USER}/${PLUGIN_NAME}

	echo "Plugin is removed successfully."
else
	echo "Remove action is canceled."
fi


