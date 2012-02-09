#!/bin/sh


# gedit plugin directory
DEST=~/.gnome2/gedit/plugins/

# create it
mkdir -p ${DEST}

# remove previous verision and currect version of plugin
rm -rf ${DEST}/advancedfind*

# install currect verion of plugin
cp -rv advancedfind* ${DEST}
