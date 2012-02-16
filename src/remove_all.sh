#!/bin/sh


PLUGIN_NAME="advancedfind"

# gedit plugin directory
PLUGIN_DEST=/usr/lib/gedit/plugins/

# create it
#mkdir -p ${PLUGIN_DEST}

# remove old version
sudo rm -rf ${PLUGIN_DEST}/${PLUGIN_NAME}*

# install the plugin
#cp -rv ${PLUGIN_NAME}* ${PLUGIN_DEST}

LOCALE_DEST=/usr/share/locale

#sudo cp -rv ${PLUGIN_NAME}/locale/* ${LOCALE_DEST}

CONFIG_DEST=~/.local/share/gedit/plugins
rm -rf ${CONFIG_DEST}/${PLUGIN_NAME}



