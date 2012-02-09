# -*- encoding:utf-8 -*-


# findadvance_ui.py
# v0.0.3
#
# Copyright 2010 swatch
#
# This program is free software; you can redistribute it and/or modify
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



import sys
try:
	import pygtk
	pygtk.require("2.0")
except:
	pass
try:
	import gtk
	import gtk.glade
except:
	sys.exit(1)

import os.path
#import pango
import re
import config_manager

class AdvancedFindUI(object):
	def __init__(self, plugin):
		try:
			self._plugin = plugin
			self._instance = self._plugin.get_instance()
		except:
			pass

		gladefile = os.path.join(os.path.dirname(__file__),"FindDialog.glade")
		ui = gtk.Builder()
		ui.add_from_file(gladefile)
		ui.connect_signals({ "on_findDialog_destroy" : self.on_findDialog_destroy_action,
							
							"on_findButton_clicked" : self.on_findButton_clicked_action,
							"on_replaceButton_clicked" : self.on_replaceButton_clicked_action,
							"on_findAllButton_clicked" : self.on_findAllButton_clicked_action,
							"on_replaceAllButton_clicked" : self.on_replaceAllButton_clicked_action,
							"on_closeButton_clicked" : self.on_closeButton_clicked_action,

							"on_matchWholeWordCheckbutton_toggled" : self.on_matchWholeWordCheckbutton_toggled_action,
							"on_matchCaseCheckbutton_toggled" : self.on_matchCaseCheckbutton_toggled_action,
							"on_wrapAroundCheckbutton_toggled" : self.on_wrapAroundCheckbutton_toggled_action,

							"on_forwardRadiobutton_toggled" : self.directionRadiobuttonGroup_action,
							"on_backwardRadiobutton_toggled" : self.directionRadiobuttonGroup_action,

							"on_currentFileRadiobutton_toggled" : self.scopeRadiobuttonGroup_action,
							"on_allFilesRadiobutton_toggled" : self.scopeRadiobuttonGroup_action,
							"on_allFilesInPathRadiobutton_toggled" : self.scopeRadiobuttonGroup_action })

		self.findDialog = ui.get_object("findDialog")
		self.findDialog.set_keep_above(True)

		#self.findTextEntry = ui.get_object("findTextEntry")
		#self.replaceTextEntry = ui.get_object("replaceTextEntry")
		
		self.findTextEntry = ui.get_object("findTextComboboxentry")
		#self.findTextListstore = ui.get_object("findTextListstore")
		#find_cell = gtk.CellRendererText()
		#self.findTextEntry.pack_start(find_cell, True)
		#self.findTextEntry.add_attribute(find_cell, 'text', 0)
		self.findTextEntry.set_text_column(0)
		for find_text in self._instance.find_list:
			self.findTextEntry.append_text(find_text)

		self.replaceTextEntry = ui.get_object("replaceTextComboboxentry")
		#self.replaceTextListstore = ui.get_object("replaceTextListstore")
		#replace_cell = gtk.CellRendererText()
		#self.replaceTextEntry.pack_start(replace_cell, True)
		#self.replaceTextEntry.add_attribute(replace_cell, 'text', 0)
		self.replaceTextEntry.set_text_column(0)
		for replace_text in self._instance.replace_list:
			self.replaceTextEntry.append_text(replace_text)


		self.matchWholeWordCheckbutton = ui.get_object("matchWholeWordCheckbutton")
		self.matchCaseCheckbutton = ui.get_object("matchCaseCheckbutton")
		self.wrapAroundCheckbutton = ui.get_object("wrapAroundCheckbutton")

		self.forwardRadiobutton = ui.get_object("forwardRadiobutton")
		self.backwardRadiobutton = ui.get_object("backwardRadiobutton")

		self.currentFileRadiobutton = ui.get_object("currentFileRadiobutton")
		self.allFilesRadiobutton = ui.get_object("allFilesRadiobutton")

		self.findButton = ui.get_object("findButton")
		self.replaceButton = ui.get_object("replaceButton")
		self.findAllButton = ui.get_object("findAllButton")
		self.replaceAllButton = ui.get_object("replaceAllButton")
		self.closeButton = ui.get_object("closeButton")

		self.findDialog.show()

		#'''
		configfile = os.path.join(os.path.dirname(__file__), "config.xml")
		self.config_manager = config_manager.ConfigManager(configfile)
		self.options = self.config_manager.load_configure('search_option')
		for key in self.options.keys():
			if self.options[key] == 'True':
				self.options[key] = True
			elif self.options[key] == 'False':
				self.options[key] = False
		
		self.matchWholeWordCheckbutton.set_active(self.options['MATCH_WHOLE_WORD'])
		self.matchCaseCheckbutton.set_active(self.options['MATCH_CASE'])
		self.wrapAroundCheckbutton.set_active(self.options['WRAP_AROUND'])
		#'''

		self.forwardFlg = True
		self.scopeFlg = 0 #current document

	def on_findDialog_destroy_action(self, object):
		try:
			self.config_manager.update_config_file(self.config_manager.config_file, 'search_option', self.options)
			self._instance.find_dialog = None
		except:
			pass

	def main(self):
		gtk.main()


	# button actions       
	def on_findButton_clicked_action(self, object):
		doc = self._instance._window.get_active_document()
		if not doc:
			return
		
		pattern = self.findTextEntry.get_active_text()
		if pattern == "":
			return
			
		if pattern not in self._instance.find_list:
			self._instance.find_list.append(pattern)
			self.findTextEntry.append_text(pattern)
			
		self._instance.advanced_find_in_doc(doc, pattern, self.options, self.forwardFlg)
		
	def on_replaceButton_clicked_action(self, object):
		doc = self._instance._window.get_active_document()
		if not doc:
			return
		
		pattern = self.findTextEntry.get_active_text()
		if pattern == "":
			return
			
		replace_text = self.replaceTextEntry.get_active_text()
		if replace_text != "" and replace_text not in self._instance.replace_list:
			self._instance.replace_list.append(replace_text)
			self.replaceTextEntry.append_text(replace_text)
			
			
		self._instance.advanced_find_in_doc(doc, pattern, self.options, self.forwardFlg, True)

	def on_findAllButton_clicked_action(self, object):
		pattern = self.findTextEntry.get_active_text()
		if pattern == "":
			return
			
		if pattern not in self._instance.find_list:
			self._instance.find_list.append(pattern)
			self.findTextEntry.append_text(pattern)

		it = self._instance._results_view.append_find_pattern(pattern)
		
		if self.scopeFlg == 0: #current
			doc = self._instance._window.get_active_document()
			if not doc:
				return
			self._instance.advanced_find_all_in_doc(it, doc, pattern, self.options)
		elif self.scopeFlg == 1: #all opened
			docs = self._instance._window.get_documents()
			if not docs:
				return
			for i in range(0,len(docs)):
				self._instance.advanced_find_all_in_doc(it, docs[i], pattern, self.options)

	def on_replaceAllButton_clicked_action(self, object):
		pattern = self.findTextEntry.get_active_text()
		if pattern == "":
			return
			
		replace_text = self.replaceTextEntry.get_active_text()
		if replace_text != "" and replace_text not in self._instance.replace_list:
			self._instance.replace_list.append(replace_text)
			self.replaceTextEntry.append_text(replace_text)

		it = self._instance._results_view.append_find_pattern(pattern, True, self.replaceTextEntry.child.get_text())
		
		if self.scopeFlg == 0: #current
			doc = self._instance._window.get_active_document()
			if not doc:
				return
			self._instance.advanced_find_all_in_doc(it, doc, pattern, self.options, True)
		elif self.scopeFlg == 1: #all opened
			docs = self._instance._window.get_documents()
			if not docs:
				return
			for i in range(0,len(docs)):
				self._instance.advanced_find_all_in_doc(it, docs[i], pattern, self.options, True)

	def on_closeButton_clicked_action(self, object):
		self.findDialog.destroy()

	# options    
	def on_matchWholeWordCheckbutton_toggled_action(self, object):
		self.options['MATCH_WHOLE_WORD'] = object.get_active()

	def on_matchCaseCheckbutton_toggled_action(self, object):
		self.options['MATCH_CASE'] = object.get_active()

	def on_wrapAroundCheckbutton_toggled_action(self, object):
		self.options['WRAP_AROUND'] = object.get_active()


	# radiobutton
	def directionRadiobuttonGroup_action(self, object):
		self.forwardFlg = self.forwardRadiobutton.get_active()

	def scopeRadiobuttonGroup_action(self, object):
		if self.currentFileRadiobutton.get_active() == True:
			self.scopeFlg = 0
		elif self.allFilesRadiobutton.get_active() == True:
			self.scopeFlg = 1


if __name__ == "__main__":
	app = AdvancedFindUI(None)
	app.main()

