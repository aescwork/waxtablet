#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
	A script for testing keyval to make sure the same keyval object is both reading from and updating a database.
"""
import sys
import os

sys.path.append("../waxtablet") 	# path to source code files

import sqlmg
import sqlmin
import wtterm
import keyval

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

	path_to_db = "wtab_usr_data/wtab_app"

	sg_read = sqlmg.SQLiteMgr(path_to_db)
	sm_read = sqlmin.SQLiteMinor(sg_read.make_conn(), "settings")

	trm = wtterm.WTTermIO()
	k_v = keyval.KeyVal(path_to_db, "settings", "settings_key", "settings_val")

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
	#		sg_update = sqlmg.SQLiteMgr(path_to_db)
	#		sm_update = sqlmin.SQLiteMinor(sg_update.make_conn(), "settings")
			for row in rows:
				if setting_key in str(row[0]):
					d = "Using keyval to get this value from db.  Result: " + k_v.d[row[1]]				
					trm.display(d, 2, 0, 0)
					k_v.d = str(setting_val)
					d = "Using keyval to modify the database.  Keyval read Result: " + k_v.d[str(row[1])]
					trm.display(d, 2, 0, 0)

			del(sg_update)
			del(sm_update)
		
	except Exception as e:
		sys.stdout.write("\n\tError: " + str(e) + "\n\n")


