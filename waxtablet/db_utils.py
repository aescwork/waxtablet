"""

..	currentmodule:: db_utils 
	:platform: Linux, Unix, Windows
	:synopsis:  Handle basic functions for creating wtab_app database 

.. moduleauthor:: aescwork@protonmail.com


"""
import os
import stat

import sqlmg
import sqlmin


def setup_sqlite_modules(path_to_db, table):
	"""
		Setup the sqlmg and sqlmin objects for working with the locs_wtab_app database.

		Args:
				path_to_locs_wtab_app:		The path to the locs_wtab_app database.

		Returns:
				A list with the sqlmg and sqlmin objects.

	"""
	util_sg = sqlmg.SQLiteMgr(path_to_db)
	util_sm = sqlmin.SQLiteMinor()
	
	return [util_sg, util_sm]


def create_wtab_app(path_to_wtab_app, os_type, user_name):

	"""
		Create the wtab_app database file for the user. 

		Args:
				path_to_wtab_app:
								The path to location where the wtab_app path for the user is to reside.
		
	"""

	if "wtab_app" in path_to_wtab_app:
		path_to_wtab_app = path_to_wtab_app.replace("wtab_app", "")

	# find out if the directory in path_to_wtab_app already exists.  If not, create it
	md = False
	try:
		os.stat(path_to_wtab_app)
	except OSError:
		md = True
	
	if md:
		os.makedirs(path_to_wtab_app)
		
	path_to_wtab_app = os.path.join(path_to_wtab_app, "wtab_app")
	util_sg, util_sm = setup_sqlite_modules(path_to_wtab_app, "settings")
	util_sg.create_db()
	util_sg.new_table("settings").add_table_column("settings_key", "text").add_table_column("settings_val", "text").create_table()

	if os_type == 'posix':			# change the owner and file permissions on the wtab_app database so the (non-root) user can access it
		import pwd
		import grp		
		uid = pwd.getpwnam(user_name).pw_uid
		gid = grp.getgrnam(user_name).gr_gid
		os.chown(path_to_wtab_app, uid, gid)
		os.chmod(path_to_wtab_app, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH)


	del(util_sg)		# make sure to start with a fresh connection to the database
	util_sg = setup_sqlite_modules(path_to_wtab_app, "settings")[0]
	util_sm.table = "settings"
	util_sm.conn = util_sg.make_conn()
	row_list = [("path_to_html_templates", ""), ("path_to_entry_databases", ""), ("path_to_input_html_file", ""), ("path_to_output_html_file", ""),\
				 ("current_entry_database", ""), ("basic_input_html_file_template",\
				 "\r\n<!-- BEGIN ENTRY -->\r\n<!-- NUMBER: -->\r\n<!-- DATE: -->\r\n<!-- KEYWORDS: -->\r\n<!-- TEXT: -->\r\n<p></p>\r\n<p></p>\r\n<p></p>\r\n"),\
				("current_entries_to_update", "None"), ("current_html_template", "default.html"), ("auto_delete_merge_update", "1"),\
				 ("auto_reindex_entries", "1"), ("display_fail_messages", "1"), ("display_success_messages", "1")]

	for row in row_list:
		util_sm.add(row)

	if util_sm.result == "FAIL":
		return False

	return True

