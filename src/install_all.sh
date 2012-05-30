#!/bin/sh


PLUGIN_NAME="advancedfind"

# gedit plugin directory
PLUGIN_DEST=/usr/lib/gedit/plugins/

# create it
sudo mkdir -p ${PLUGIN_DEST}

# remove old version
sudo rm -rf ${PLUGIN_DEST}/${PLUGIN_NAME}*

# install the plugin
sudo cp -rv ${PLUGIN_NAME}* ${PLUGIN_DEST}

LOCALE_DEST=/usr/share/locale

sudo cp -rv ${PLUGIN_NAME}/locale/* ${LOCALE_DEST}

CONFIG_DEST=~/.local/share/gedit/plugins
mkdir -p ${CONFIG_DEST}/${PLUGIN_NAME}
cp -rv ${PLUGIN_NAME}/config ${CONFIG_DEST}/${PLUGIN_NAME}

