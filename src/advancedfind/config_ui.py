# -*- encoding:utf-8 -*-


# config_ui.py is part of advancedfind-gedit.
#
#
# Copyright 2010-2012 swatch
#
# advancedfind-gedit is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#




from gi.repository import Gtk, Gedit, Gdk
import os.path
	
#from gettext import gettext as _



class ConfigUI(object):
	def __init__(self, plugin):
		#self._plugin = plugin
		self._instance, self._window = plugin.get_instance()
	
		#Set the Glade file
		gladefile = os.path.join(os.path.dirname(__file__),"config.glade")
		UI = Gtk.Builder()
		UI.set_translation_domain('advancedfind')
		UI.add_from_file(gladefile)
		self.configWindow = UI.get_object("configWindow")
		#self.configWindow.set_transient_for(self._window)
		
		self.fgColorbutton = UI.get_object("fgColorbutton")
		self.bgColorbutton = UI.get_object("bgColorbutton")
		self.fgColorbutton.set_color(Gdk.color_parse(self._instance.result_highlight['FOREGROUND_COLOR']))
		self.bgColorbutton.set_color(Gdk.color_parse(self._instance.result_highlight['BACKGROUND_COLOR']))
		
		self.useDefaultFontCheckbutton = UI.get_object("useDefaultFontCheckbutton")
		self.useDefaultFontCheckbutton.set_active(self._instance.result_gui_settings['USE_DEFAULT_FONT'])
		self.resultFontbutton = UI.get_object("resultFontbutton")
		if self._instance.result_gui_settings['USE_DEFAULT_FONT']:
			self.resultFontbutton.get_parent().set_sensitive(False)
		else:
			self.resultFontbutton.get_parent().set_sensitive(True)

		self.rootFollowFilebrowserCheckbutton = UI.get_object("rootFollowFilebrowserCheckbutton")
		self.rootFollowFilebrowserCheckbutton.set_active(self._instance.find_options['ROOT_FOLLOW_FILEBROWSER'])
		
		self.configWindow.show_all()

		signals = { "on_configWindow_destroy" : self.on_configWindow_destroy,
					"on_fgColorbutton_color_set" : self.on_fgColorbutton_color_set,
					"on_bgColorbutton_color_set" : self.on_bgColorbutton_color_set,
					"on_useDefaultFontCheckbutton_toggled" : self.on_useDefaultFontCheckbutton_toggled,
					"on_resultFontbutton_font_set" : self.on_resultFontbutton_font_set,
					"on_rootFollowFilebrowserCheckbutton_toggled" : self.on_rootFollowFilebrowserCheckbutton_toggled }
		
		UI.connect_signals(signals)
		
		
	def on_configWindow_destroy(self, widget):
		pass
		
	def on_fgColorbutton_color_set(self, widget):
		self._instance.result_highlight['FOREGROUND_COLOR'] = widget.get_color().to_string()
		
	def on_bgColorbutton_color_set(self, widget):
		self._instance.result_highlight['BACKGROUND_COLOR'] = widget.get_color().to_string()
		
	def on_useDefaultFontCheckbutton_toggled(self, object):
		self._instance.result_gui_settings['USE_DEFAULT_FONT'] = object.get_active()
		if object.get_active():
			self.resultFontbutton.get_parent().set_sensitive(False)
		else:
			self.resultFontbutton.get_parent().set_sensitive(True)
		
	def on_resultFontbutton_font_set(self, object):
		self._instance.result_gui_settings['RESULT_FONT'] = object.get_font_name()
		
	def on_rootFollowFilebrowserCheckbutton_toggled(self, widget):
		self._instance.find_options['ROOT_FOLLOW_FILEBROWSER'] = widget.get_active()
			


if __name__ == '__main__':
	dlg = ConfigUI(None)
	Gtk.main()
	
