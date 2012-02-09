# -*- encoding:utf-8 -*-


# findadvance_ui.py
# v0.1.2
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
import os
import fnmatch
import subprocess
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
		self.ui = gtk.Builder()
		self.ui.add_from_file(gladefile)
		self.ui.connect_signals({ "on_findDialog_destroy" : self.on_findDialog_destroy_action,
							
							"on_findButton_clicked" : self.on_findButton_clicked_action,
							"on_replaceButton_clicked" : self.on_replaceButton_clicked_action,
							"on_findAllButton_clicked" : self.on_findAllButton_clicked_action,
							"on_replaceAllButton_clicked" : self.on_replaceAllButton_clicked_action,
							"on_closeButton_clicked" : self.on_closeButton_clicked_action,
							"on_selectPathButton_clicked" : self.on_selectPathButton_clicked_action,
							"on_selectPathDialogOkButton_clicked" : self.on_selectPathDialogOkButton_clicked_action,
							"on_selectPathDialogCancelButton_clicked" : self.on_selectPathDialogCancelButton_clicked_action,
							
							"on_matchWholeWordCheckbutton_toggled" : self.on_matchWholeWordCheckbutton_toggled_action,
							"on_matchCaseCheckbutton_toggled" : self.on_matchCaseCheckbutton_toggled_action,
							"on_wrapAroundCheckbutton_toggled" : self.on_wrapAroundCheckbutton_toggled_action,
							"on_followCurrentDocCheckbutton_toggled" : self.on_followCurrentDocCheckbutton_toggled_action,
							"on_includeSubfolderCheckbutton_toggled" : self.on_includeSubfolderCheckbutton_toggled_action,
							
							"on_forwardRadiobutton_toggled" : self.directionRadiobuttonGroup_action,
							"on_backwardRadiobutton_toggled" : self.directionRadiobuttonGroup_action,
							
							"on_currentFileRadiobutton_toggled" : self.scopeRadiobuttonGroup_action,
							"on_allFilesRadiobutton_toggled" : self.scopeRadiobuttonGroup_action,
							"on_allFilesInPathRadiobutton_toggled" : self.scopeRadiobuttonGroup_action })

		self.findDialog = self.ui.get_object("findDialog")
		self.findDialog.set_keep_above(True)

		self.findTextEntry = self.ui.get_object("findTextComboboxentry")
		#self.findTextListstore = self.ui.get_object("findTextListstore")
		#find_cell = gtk.CellRendererText()
		#self.findTextEntry.pack_start(find_cell, True)
		#self.findTextEntry.add_attribute(find_cell, 'text', 0)
		self.findTextEntry.set_text_column(0)
		try:
			for find_text in self._instance.find_list:
				self.findTextEntry.append_text(find_text)
		except:
			pass

		self.replaceTextEntry = self.ui.get_object("replaceTextComboboxentry")
		#self.replaceTextListstore = self.ui.get_object("replaceTextListstore")
		#replace_cell = gtk.CellRendererText()
		#self.replaceTextEntry.pack_start(replace_cell, True)
		#self.replaceTextEntry.add_attribute(replace_cell, 'text', 0)
		self.replaceTextEntry.set_text_column(0)
		try:
			for replace_text in self._instance.replace_list:
				self.replaceTextEntry.append_text(replace_text)
		except:
			pass
			
		self.filterComboboxentry = self.ui.get_object("filterComboboxentry")
		self.filterComboboxentry.set_text_column(0)
		self.filterComboboxentry.child.set_text("*")
		#self.filterComboboxentry.append_text("*")
		try:
			for file_filter in self._instance.filter_list:
				self.filterComboboxentry.append_text(file_filter)
		except:
			pass
			
		self.selectPathFilechooserdialog = self.ui.get_object("selectPathFilechooserdialog")
		
		self.pathComboboxentry = self.ui.get_object("pathComboboxentry")
		self.pathComboboxentry.set_text_column(0)
		self.pathComboboxentry.child.set_text(self.selectPathFilechooserdialog.get_filename())
		#self.pathComboboxentry.child.set_text(os.path.dirname(self._instance._window.get_active_document().get_uri_for_display()))
		try:
			for path in self._instance.path_list:
				self.pathComboboxentry.append_text(path)
		except:
			pass
		
		self.matchWholeWordCheckbutton = self.ui.get_object("matchWholeWordCheckbutton")
		self.matchCaseCheckbutton = self.ui.get_object("matchCaseCheckbutton")
		self.wrapAroundCheckbutton = self.ui.get_object("wrapAroundCheckbutton")
		self.followCurrentDocCheckbutton = self.ui.get_object("followCurrentDocCheckbutton")
		self.includeSubfolderCheckbutton = self.ui.get_object("includeSubfolderCheckbutton")

		self.forwardRadiobutton = self.ui.get_object("forwardRadiobutton")
		self.backwardRadiobutton = self.ui.get_object("backwardRadiobutton")
		if self._instance.forwardFlg == True:
			self.forwardRadiobutton.set_active(True)
		else:
			self.backwardRadiobutton.set_active(True)

		self.currentFileRadiobutton = self.ui.get_object("currentFileRadiobutton")
		self.allFilesRadiobutton = self.ui.get_object("allFilesRadiobutton")
		self.allFilesInPathRadiobutton = self.ui.get_object("allFilesInPathRadiobutton")
		if self._instance.scopeFlg == 0:
			self.currentFileRadiobutton.set_active(True)
		elif self._instance.scopeFlg == 1:
			self.allFilesRadiobutton.set_active(True)
		elif self._instance.scopeFlg == 2:
			self.allFilesInPathRadiobutton.set_active(True)

		self.findButton = self.ui.get_object("findButton")
		self.replaceButton = self.ui.get_object("replaceButton")
		self.findAllButton = self.ui.get_object("findAllButton")
		self.replaceAllButton = self.ui.get_object("replaceAllButton")
		self.closeButton = self.ui.get_object("closeButton")
		self.selectPathButton = self.ui.get_object("selectPathButton")

		self.findDialog.show()

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
		self.followCurrentDocCheckbutton.set_active(self.options['FOLLOW_CURRENT_DOC'])
		self.includeSubfolderCheckbutton.set_active(self.options['INCLUDE_SUBFOLDER'])

		if self.options['FOLLOW_CURRENT_DOC'] == True:
			self.pathComboboxentry.child.set_text(os.path.dirname(self._instance._window.get_active_document().get_uri_for_display()))

		#self._instance.scopeFlg = 0 #current document

	def on_findDialog_destroy_action(self, object):
		try:
			self.config_manager.update_config_file(self.config_manager.config_file, 'search_option', self.options)
			self._instance.find_dialog = None
		except:
			pass

	def main(self):
		gtk.main()

	def append_combobox_list(self):
		find_text = self.findTextEntry.get_active_text()
		replace_text = self.replaceTextEntry.get_active_text()
		file_filter = self.filterComboboxentry.get_active_text()
		path = self.pathComboboxentry.get_active_text()
		self._instance.current_pattern = find_text
		
		if find_text != "" and find_text not in self._instance.find_list:
			self._instance.find_list.append(find_text)
			self.findTextEntry.append_text(find_text)
			
		if replace_text != "" and replace_text not in self._instance.replace_list:
			self._instance.replace_list.append(replace_text)
			self.replaceTextEntry.append_text(replace_text)
			
		if file_filter != "" and file_filter not in self._instance.filter_list:
			self._instance.filter_list.append(file_filter)
			self.filterComboboxentry.append_text(file_filter)
			
		if path != "" and path not in self._instance.path_list:
			self._instance.path_list.append(path)
			self.pathComboboxentry.append_text(path)

	# button actions       
	def on_findButton_clicked_action(self, object):
		doc = self._instance._window.get_active_document()
		if not doc:
			return
		
		search_pattern = self.findTextEntry.get_active_text()
		self._instance.curretn_pattern = search_pattern
		if search_pattern == "":
			return
		
		self.append_combobox_list()
		self._instance.advanced_find_in_doc(doc, search_pattern, self.options, self._instance.forwardFlg)
		
	def on_replaceButton_clicked_action(self, object):
		doc = self._instance._window.get_active_document()
		if not doc:
			return
		
		search_pattern = self.findTextEntry.get_active_text()
		self._instance.curretn_pattern = search_pattern
		if search_pattern == "":
			return
		
		self.append_combobox_list()
		self._instance.advanced_find_in_doc(doc, search_pattern, self.options, self._instance.forwardFlg, True)

	def on_findAllButton_clicked_action(self, object):
		search_pattern = self.findTextEntry.get_active_text()
		if search_pattern == "":
			return
		
		self.append_combobox_list()
		
		it = self._instance._results_view.append_find_pattern(search_pattern)
		
		if self._instance.scopeFlg == 0: #current
			doc = self._instance._window.get_active_document()
			if not doc:
				return
			self._instance.advanced_find_all_in_doc(it, doc, search_pattern, self.options)
			self._instance._results_view.show_find_result()
			self._instance.show_bottom_panel()
		elif self._instance.scopeFlg == 1: #all opened
			docs = self._instance._window.get_documents()
			if not docs:
				return
			for doc in docs:
				self._instance.advanced_find_all_in_doc(it, doc, search_pattern, self.options)
			self._instance._results_view.show_find_result()
			self._instance.show_bottom_panel()
		elif self._instance.scopeFlg == 2: #files in directory
			dir_path = self.pathComboboxentry.get_active_text()
			file_pattern = self.filterComboboxentry.get_active_text()
			self._instance.find_all_in_dir(it, dir_path, file_pattern, search_pattern, self.options)

	def on_replaceAllButton_clicked_action(self, object):
		search_pattern = self.findTextEntry.get_active_text()
		if search_pattern == "":
			return
		
		self.append_combobox_list()

		it = self._instance._results_view.append_find_pattern(search_pattern, True, self.replaceTextEntry.child.get_text())
		
		if self._instance.scopeFlg == 0: #current
			doc = self._instance._window.get_active_document()
			if not doc:
				return
			self._instance.advanced_find_all_in_doc(it, doc, search_pattern, self.options, True)
			self._instance._results_view.show_find_result()
			self._instance.show_bottom_panel()
		elif self._instance.scopeFlg == 1: #all opened
			docs = self._instance._window.get_documents()
			if not docs:
				return
			for doc in docs:
				self._instance.advanced_find_all_in_doc(it, doc, search_pattern, self.options, True)
			self._instance._results_view.show_find_result()
			self._instance.show_bottom_panel()
		elif self._instance.scopeFlg == 2: #files in directory
			path = str(self._instance._results_view.findResultTreemodel.iter_n_children(None) - 1)
			it = self._instance._results_view.findResultTreemodel.get_iter(path)
			self._instance._results_view.findResultTreemodel.set_value(it, 2, "Replace in All Documents in Directory is not supported.")

	def on_closeButton_clicked_action(self, object):
		self.findDialog.destroy()
		
	def on_selectPathButton_clicked_action(self, object):
		self.selectPathFilechooserdialog.show()

	# select path file chooserr dialog actions
	def on_selectPathDialogOkButton_clicked_action(self, object):
		folder_path = self.selectPathFilechooserdialog.get_filename()
		self.selectPathFilechooserdialog.select_filename(folder_path)
		self.pathComboboxentry.child.set_text(folder_path)
		self.append_combobox_list()
		self.selectPathFilechooserdialog.hide()
		
	def on_selectPathDialogCancelButton_clicked_action(self, object):
		self.selectPathFilechooserdialog.hide()

	# options    
	def on_matchWholeWordCheckbutton_toggled_action(self, object):
		self.options['MATCH_WHOLE_WORD'] = object.get_active()

	def on_matchCaseCheckbutton_toggled_action(self, object):
		self.options['MATCH_CASE'] = object.get_active()

	def on_wrapAroundCheckbutton_toggled_action(self, object):
		self.options['WRAP_AROUND'] = object.get_active()
		
	def on_followCurrentDocCheckbutton_toggled_action(self, object):
		self.options['FOLLOW_CURRENT_DOC'] = object.get_active()
		if object.get_active() == True:
			self.pathComboboxentry.child.set_text(os.path.dirname(self._instance._window.get_active_document().get_uri_for_display()))
		else:
			self.pathComboboxentry.child.set_text(self.selectPathFilechooserdialog.get_filename())
			
	def on_includeSubfolderCheckbutton_toggled_action(self, object):
		self.options['INCLUDE_SUBFOLDER'] = object.get_active()


	# radiobutton
	def directionRadiobuttonGroup_action(self, object):
		self._instance.forwardFlg = self.forwardRadiobutton.get_active()

	def scopeRadiobuttonGroup_action(self, object):
		if self.currentFileRadiobutton.get_active() == True:
			self._instance.scopeFlg = 0
		elif self.allFilesRadiobutton.get_active() == True:
			self._instance.scopeFlg = 1
		elif self.allFilesInPathRadiobutton.get_active() == True:
			self._instance.scopeFlg = 2


if __name__ == "__main__":
	app = AdvancedFindUI(None)
	app.main()

