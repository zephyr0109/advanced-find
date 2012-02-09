# -*- encoding:utf-8 -*-


# findadvance.py
# v0.0.2
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



from gettext import gettext as _

import gtk
import gedit
import os.path
import re

from advancedfind_ui import AdvancedFindUI
from find_result import FindResultView

#import lang



# Menu item example, insert a new item in the Edit menu
ui_str = """<ui>
	<menubar name="MenuBar">
		<menu name="SearchMenu" action="Search">
			<placeholder name="SearchOps_2">
				<menuitem name="advanced_find" action="advanced_find"/>
			</placeholder>
		</menu>
	</menubar>
</ui>
"""


class AdvancedFindWindowHelper:
	def __init__(self, plugin, window):
		self._window = window
		self._plugin = plugin
		self.find_dialog = None

		self._results_view = FindResultView(window)
		self._window.get_bottom_panel().add_item(self._results_view, "Advanced Find", "gtk-find")

		# Insert menu items
		self._insert_menu()

	def deactivate(self):
		# Remove any installed menu items
		self._remove_menu()

		self._window = None
		self._plugin = None
		self.find_dialog = None
	
	def _insert_menu(self):
		# Get the GtkUIManager
		manager = self._window.get_ui_manager()

		# Create a new action group
		self._action_group = gtk.ActionGroup("FindAdvanceActions")
		self._action_group.add_actions( [("advanced_find", None, _("Advanced Find / Replace"), "<ctrl><shift>F", _("Advanced Find / Replace"), self.advanced_find_active)]) 

		# Insert the action group
		manager.insert_action_group(self._action_group, -1)

		# Merge the UI
		self._ui_id = manager.add_ui_from_string(ui_str)

	def _remove_menu(self):
		# Get the GtkUIManager
		manager = self._window.get_ui_manager()

		# Remove the ui
		manager.remove_ui(self._ui_id)

		# Remove the action group
		manager.remove_action_group(self._action_group)

		# Make sure the manager updates
		manager.ensure_update()

	def update_ui(self):
		self._action_group.set_sensitive(self._window.get_active_document() != None)
		
	def show_message_dialog(self, text):
		dlg = gtk.MessageDialog(self._window, 
								gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
								gtk.MESSAGE_INFO,
								gtk.BUTTONS_CLOSE,
								_(text))
		dlg.run()
		dlg.hide()
		
	def advanced_find_active(self, action):
		doc = self._window.get_active_document()
		if not doc:
			return
		
		try:
			start, end = doc.get_selection_bounds()
			search_text = unicode(doc.get_text(start,end))
		except:
			search_text = ""

		if self.find_dialog == None:
			self.find_dialog = AdvancedFindUI(self._plugin)
			self.find_dialog.findDialog.set_keep_above(True)
			
		if search_text != "":
			self.find_dialog.findTextEntry.set_text(search_text)
		
		uri = doc.get_uri_for_display()
		self.find_dialog.pathEntry.set_text(os.path.dirname(uri))

	def create_regex(self, pattern, options):
		if options['MATCH_WHOLE_WORD'] == True:
			pattern = "\\b%s\\b" % pattern
			
		if options['MATCH_CASE'] == True:
			regex = re.compile(unicode(pattern, "utf-8"))
		else:
			regex = re.compile(unicode(pattern, "utf-8"), re.IGNORECASE)

		return regex
		
	def advanced_find_in_doc(self, doc, pattern, options, forward_flg = True, replace_flg = False):
		if pattern == "":
			return
			
		try:
			selection_start, selection_end = doc.get_selection_bounds()
			if forward_flg == True:
				doc.place_cursor(selection_end)
			else:
				doc.place_cursor(selection_start)
		except:
			pass
		
		regex = self.create_regex(pattern, options)
		
		view = self._window.get_active_view()
		if forward_flg == True:
			find_start = doc.get_iter_at_mark(doc.get_insert())
			next_flg = view.forward_display_line(find_start)

			while next_flg == True:
				line_start = doc.get_iter_at_mark(doc.get_insert())
				line = doc.get_text(find_start, line_start)
				match = regex.search(line)
				if match:
					result_start = doc.get_iter_at_offset(line_start.get_offset() + match.start())
					result_end = doc.get_iter_at_offset(line_start.get_offset() + match.end())
					doc.select_range(result_start, result_end)
					view.scroll_to_cursor()
					if replace_flg == True:
						replace_text = unicode(self.find_dialog.replaceTextEntry.get_text(), 'utf-8')
						doc.delete_selection(False, False)
						doc.insert_at_cursor(replace_text)
						replace_end = doc.get_iter_at_mark(doc.get_insert())
						replace_start = doc.get_iter_at_offset(replace_end.get_offset() - len(replace_text))
						doc.select_range(replace_start, replace_end)
						view.scroll_to_cursor()
						
					return
				else:
					doc.place_cursor(doc.get_iter_at_offset(line_start.get_offset() + len(line)))
					find_start = doc.get_iter_at_mark(doc.get_insert())
					next_flg = view.forward_display_line(find_start)
			
			if options['WRAP_AROUND'] == True:
				find_start = doc.get_start_iter()
				doc.place_cursor(find_start)
				self.advanced_find_in_doc(doc, pattern, options, forward_flg, replace_flg)
			#self.show_message_dialog("End of file.")
		#'''
		else:
			find_end = doc.get_iter_at_mark(doc.get_insert())
			previous_flg = view.backward_display_line(find_end)

			while previous_flg == True:
				line_start = doc.get_iter_at_mark(doc.get_insert())
				line = doc.get_text(line_start, find_end)
				result = regex.findall(line)
				if result:
					match_pos = 0
					for idx in range(0, len(result)):
						match = regex.search(line[match_pos:])
						result_start = doc.get_iter_at_offset(find_end.get_offset() + match.start() + match_pos)
						result_end = doc.get_iter_at_offset(find_end.get_offset() + match.end() + match_pos)
						match_pos += match.end()
					doc.select_range(result_start, result_end)
					view.scroll_to_cursor()

					if replace_flg == True:
						replace_text = unicode(self.find_dialog.replaceTextEntry.get_text(), 'utf-8')
						doc.delete_selection(False, False)
						doc.insert_at_cursor(replace_text)
						replace_end = doc.get_iter_at_mark(doc.get_insert())
						replace_start = doc.get_iter_at_offset(replace_end.get_offset() - len(replace_text))
						doc.select_range(replace_start, replace_end)
						view.scroll_to_cursor()
						
					return
				else:
					doc.place_cursor(doc.get_iter_at_offset(line_start.get_offset() - len(line)))
					find_end = doc.get_iter_at_mark(doc.get_insert())
					previous_flg = view.backward_display_line(find_end)

			if options['WRAP_AROUND'] == True:
				find_end = doc.get_end_iter()
				doc.place_cursor(find_end)
				self.advanced_find_in_doc(doc, pattern, options, forward_flg, replace_flg)
			#self.show_message_dialog("End of file.")
		#'''
				

	def advanced_find_all_in_doc(self, parent_it, doc, pattern, options, replace_flg = False):
		if pattern == "":
			return
		
		regex = self.create_regex(pattern, options)

		start, end = doc.get_bounds()
		text = unicode(doc.get_text(start, end), 'utf-8')
		lines = text.splitlines()
		m = re.search('(\n|\r|\r\n)', text)
		eol = m.group(0)
		
		tree_it = None
		new_lines = list('')

		for i in range(len(lines)):
			result = regex.findall(lines[i])
			line_start = doc.get_iter_at_line(i)
				
			if result:
				if not tree_it:
					uri = doc.get_uri_for_display()
					tree_it = self._results_view.append_find_result_filename(parent_it, doc.get_short_name_for_display(), uri)
				tab = gedit.tab_get_from_document(doc)
				match_pos = 0
				line_list = list(lines[i])
				for cnt in range(0,len(result)):
					match = regex.search(lines[i][match_pos:])
					result_it_start = doc.get_iter_at_offset(line_start.get_offset() + match.start() + match_pos)
					result_it_end = doc.get_iter_at_offset(line_start.get_offset() + match.end() + match_pos)
					line_list[match.start()+match_pos:match.end()+match_pos] = unicode(self.find_dialog.replaceTextEntry.get_text(), 'utf-8')

					if replace_flg == True:
						self._results_view.append_find_result(tree_it, str(i+1), lines[i].strip(), tab, None, None)
					else:
						self._results_view.append_find_result(tree_it, str(i+1), lines[i].strip(), tab, result_it_start, result_it_end)
					match_pos += match.end()

				new_lines.append("".join(line_list) + eol)

			else:
				new_lines.append(lines[i] + eol)
				
		if replace_flg == True:
			#print "".join(new_lines)
			doc.set_text("".join(new_lines))

				
		self._results_view.show_find_result()
		
		# display bottom panel if not displayed
		panel = self._window.get_bottom_panel()
		if panel.get_property("visible") == False:
			panel.set_property("visible", True)
		panel.activate_item(self._results_view)


