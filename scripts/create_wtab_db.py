#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
	A script to create the wtab_app database and table which waxtablet uses for configuration settings.  Written for Linux.  Modify as needed
	for your platform/OS.
"""
import sys

sys.path.append("../waxtablet") 	# path to the source code files for waxtablet.  Modify as needed.  It just needs sqlmin and sqlmg to import

import sqlmin
import sqlmg



def create_app_db_and_table(sg):

	sg.create_db()

	sys.stdout.write("\n\tcreate_db result: " + sg.result)
	sys.stdout.write("\n\tcreate_db status: " + sg.status)

	sg.new_table("settings").add_table_column("settings_key", "text").add_table_column("settings_val", "text").create_table()

	sys.stdout.write("\n\tcreate_table result: " + sg.result + "\n")
	sys.stdout.write("\n\tcreate_table status: " + sg.status + "\n")

def sr(sm, msg):
	
	sys.stdout.write(msg)
	sys.stdout.write("\n\tResult/Status: " + sm.result + " -- " + sm.status)
	

def populate_wtab_app_db(sm):

		row_list = [("path_to_html_templates", ""), ("path_to_entry_databases", ""), ("path_to_input_html_file", ""), ("path_to_output_html_file", ""),\
					 ("current_entry_database", ""), ("basic_input_html_file_template",\
					 "\r\n<!-- BEGIN ENTRY -->\r\n<!-- NUMBER: -->\r\n<!-- DATE: -->\r\n<!-- KEYWORDS: -->\r\n<!-- TEXT: -->\r\n<p></p>\r\n<p></p>\r\n<p></p>\r\n"),\
					("current_entries_to_update", "None"), ("current_html_template", "default.html"), ("auto_delete_merge_update", "1"),\
					 ("auto_reindex_entries", "1"), ("display_fail_messages", "1"), ("display_success_messages", "1")]

		for row in row_list:
			sm.add(row)
			msg = "\n\tAdd to " + row[0] + ": " + row[1]
			sr(sm, msg)
		
		sys.stdout.write("\n")


if __name__ == "__main__":

	path_to_db = ".waxtablet/wtab_usr_data/wtab_app" # modify this path as needed
	sg = sqlmg.SQLiteMgr(path_to_db)
	sm = sqlmin.SQLiteMinor(sg.make_conn(), "settings")

	try:
		create_app_db_and_table(sg)
		populate_wtab_app_db(sm)
	except Exception as e:
		sys.stdout.write("\n\tError: " + str(e) + "\n\n")




