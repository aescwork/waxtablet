
import sys

sys.path.append("../waxtablet/")
sys.path.append("../temp/")

import wtfileio
import make_sample_db as msd
import sqliteminor
import sqlitemgr
import entry as e

if __name__ == '__main__':

	"""
		methods:
		to_input_file
		from_input_file
		to_output_html
		get_file_names
		delete
	msd.delete_all_from_db(sm)
	msd.populate_test_journal(sm)
	"""
	table = "entries"
	db = "test_journal"
	input_html_path = "../io_files/input.html"
	output_html_path = "../io_files/output.html"
	html_template_path = "../waxtablet/html-templates/default.html"
	path_to_db = "../temp/test_journal"
	entry_list = list()
	fio = wtfileio.WTFileIO(table, db, input_html_path, output_html_path, html_template_path)
	
	sg = sqlitemgr.SQLiteMgr(path_to_db)
	sm = sqliteminor.SQLiteMinor(sg.make_conn(), table)
	
	fio.entry_list = msd.populate_entry_object_list(sm)

	#fio.to_input_file(True)
	#fio.from_input_file()
	#fio.to_output_html()
	fio.delete("../target/rdbrecord.pyc")
	found = False

	for f in fio.get_file_names("../target/"):
		print "\t", f
		if f == "rdbrecord.pyc":
			found = True
	
	if found:
		print "\tFound rdbrecord.pyc"	
	else:
		print "\trdbrecord.pyc not found"

	
	
	"""
	for i in range(1,5):
		entry_list[i].entry_text = entry_list[i].entry_text.replace("\t", "") 
		fio.entry_list.append(entry_list[i])

	for entry in fio.entry_list:
		print "\t", entry.entry_number, " -- ", entry.entry_date, " -- ", entry.entry_keywords
	"""

