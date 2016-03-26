

# Install using script (Recommanded) #
  1. Close all gedit windows.
  1. Extract downloaded file and enter the folder.
  1. Run the install script
    * **bash install.sh**
    * **bash install\_all.sh** to install for all users. (v3.5.0 or earlier)
    * Do not run as root. The script will request proper privilege during installation.
  1. Restart gedit
  1. In gedit main menu, go to **Edit->Preferences**
  1. Go to **Plugins** tab
  1. Find **Advanced Find/Replace** in list and check it
  1. In main menu, **Search->Advanced Find / Replace** or using **Shift+Ctrl+F** shortcut to activate the find/replace dialog

# Install manually #
  1. Close all gedit windows.
  1. Extract downloaded file.
  1. Copy the files to specified folder
    * Install for current user
      * **~/.local/share/gedit/plugins** for Gnome3
      * **~/.gnome2/gedit/plugins** for Gnome2
    * Install for all users
      * **/usr/lib/gedit/plugins** for Gnome3
      * **/usr/lib/gedit-2/plugins** for Gnome2
    * **Solve the privilege issue if necessary.**
  1. Restart gedit
  1. In gedit main menu, go to **Edit->Preferences**
  1. Go to **Plugins** tab
  1. Find **Advanced Find/Replace** in list and check it
  1. In main menu, **Search->Advanced Find / Replace** or using **Shift+Ctrl+F** shortcut to activate the find/replace dialog