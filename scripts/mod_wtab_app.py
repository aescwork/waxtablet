#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
	A script to modify the values in wtab_app.
	for your platform/OS.
"""
import sys
import os

sys.path.append("/home/developer/.waxtablet/src") 	# path to source code files

import sqliteminor
import sqlitemgr
import wtterm


def sr(sm, msg):
	
	sys.stdout.write(msg)
	sys.stdout.write("\n\tResult/Status: " + sm.result + " -- " + sm.status)
	

def show_db_vals(sm, t):

	nmbr = 1
	row_list = list()
	t.display(" ", 0, 0, 2)
	for row in sm.read_all():
		content = str(nmbr) + "   " + str(row[0]) + "\t" + str(row[1])
		t.display(content, 2, 0, 1)			
		row_list.append([nmbr, row[0], row[1]])
		nmbr = nmbr + 1
	
	t.display(" ", 0, 0, 1)
	
	return row_list
		


if __name__ == "__main__":

	path_to_db = "/home/developer/.waxtablet/wtab_usr_data/wtab_app" # modify this path as needed

	sg_read = sqlitemgr.SQLiteMgr(path_to_db)
	sm_read = sqliteminor.SQLiteMinor(sg_read.make_conn(), "settings")

	trm = wtterm.WTTermIO()

	try:
		while(1):
			try:
				if os.name == "nt":
					os.system('cls')
				else:
					os.system('clear')
			except Exception as e:
				pass

			rows = show_db_vals(sm_read, trm)	
			setting_key = str(trm.prompt("Which setting? Enter a number or 'e' to exit: ", 2, 0, 0))
			if setting_key == "e":
				break
			setting_val = str(trm.prompt("Enter the new value for this setting: ", 2, 0, 0))
			sg_update = sqlitemgr.SQLiteMgr(path_to_db)
			sm_update = sqliteminor.SQLiteMinor(sg_update.make_conn(), "settings")
			for row in rows:
				if setting_key in str(row[0]):
					sm_update.update("settings_val", setting_val, "settings_key", row[1])

			del(sg_update)
			del(sm_update)
		
	except Exception as e:
		sys.stdout.write("\n\tError: " + str(e) + "\n\n")


