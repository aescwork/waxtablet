"""

..	currentmodule:: waxtablet
	:platform: Linux, Unix, Windows
	:synopsis:  

.. moduleauthor:: aescwork aescwork@protonmail.com


"""

import os
import sys
import datetime
from collections import OrderedDict

import sqlmg
import rdbrecord as rdb
import keyval 
import entry as E
import flwk	
import wtterm
import wtfileio
import db_utils

class Controller():


	def __init__(self, args):

		"""

		Args: 
			args (list): the arguments gathered in argparse in main (waxtablet.py)

		"""

		self.args = args
		self.da = sqlmg.SQLiteMgr()
		self.top_ok = wtterm.WTTermIO()		# terminal output
		self.top_ok.border_char = " "
		self.top_fail = wtterm.WTTermIO()		# terminal output of any failure messages
		self.top_fail.border_char = " "
		self.invalid_v_opt = True 
		self.default_wtab_app_path = ""

		self.EXIT_CODE = 0
		self.entry_list = list()

		self.rdbe = None	# rdb.Entries
		self.fw = flwk.FileWork()

		# handle first access of the locs_wtab_app database
		
		user_name = ""
		wtab_app_path = ""
		os_name = os.name

		try:	
			if os_name == 'nt':			# get user name, home directory info for a MS Windows user 
				user_name = os.environ['USERNAME']
				self.default_wtab_app_path = os.path.join("C:", "\Users", user_name, "waxtablet", "wtab_usr_data") 
			elif os_name == 'posix':			# get user name, home directory info for a 'posix' (linux, unix) user
				user_name = os.environ['USER']
				if user_name == "root":	
					try:									# fist-time user of this application needs to run sudo to add his information
						user_name = os.environ['SUDO_USER']	# to locs_wtab_app database
					except:
						self.top_fail.display("The root user may not use this application as root.  Exiting.", 2, 1, 0)
						self.EXIT_CODE = 1
						self.wt_exit()
						
				self.default_wtab_app_path = os.path.join("/", "home", user_name, ".waxtablet", "wtab_usr_data")


		except Exception as e:
			
			self.top_fail.display("Error Accessing User Information for location of wtab_app: " + str(e) + " ...Exiting.", 2, 2, 2)
			self.EXIT_CODE = 1
			self.wt_exit()

		# if wtab_app

		if os.path.isfile(self.default_wtab_app_path):
			wtab_app_path = self.default_wtab_app_path
		else:
			if db_utils.create_wtab_app(self.default_wtab_app_path, os_name, user_name):
				wtab_app_path = self.default_wtab_app_path
				
			else:
				self.top_fail.display("Unable to create the wtab_app database file for user " + user_name, 2, 1, 0)
				self.top_fail.display("Make sure you have permissions to create files and directories in the specified location: " + wtab_app_path, 2, 1, 0)
				self.top_fail.display("Make sure there are no additional problems such as lack of storage space, etc.  Exiting.", 2, 1, 2)
				self.EXIT_CODE = 1
				self.wt_exit()
		
		
		try:
			self.sa = keyval.KeyVal(os.path.join(wtab_app_path, "wtab_app"), "settings", "settings_key", "settings_val") 	# application settings
		except Exception as e:
			self.top_fail.display("Error Accessing wtab_app database file for user " + user_name + ": " + str(e) + " ...Exiting.", 2, 2, 2)
			self.EXIT_CODE = 1
			self.wt_exit()

		#### paths to files
		try:
			self.current_db = os.path.join(self.sa.d['path_to_entry_databases'], self.sa.d['current_entry_database'])
			self.current_html_template = os.path.join(self.sa.d['path_to_html_templates'], self.sa.d['current_html_template'])
			self.output_html_file = self.sa.d['path_to_output_html_file']
			self.input_html_file = self.sa.d['path_to_input_html_file']
	
			self.fio = wtfileio.WTFileIO("entries", self.current_db, self.input_html_file, self.output_html_file, self.current_html_template)	# file input/output
		
		except Exception as e:
			self.top_fail.display("Error accessing waxtablet files:  " + str(e) + " ...Exiting.", 2, 2, 1)
			self.top_fail.display("Make sure wtab_app is located at " + wtab_app_path + ".", 2, 1, 3)
			self.EXIT_CODE = 1
			self.wt_exit()
				

		if self.args.M:
			"""
				Run a quick initialization which presents a menu prompting the user for certain information (see i_menus())
			"""
			self.i_menus()


		if self.args.N:
			"""
				Create a new entry entry database.
			"""

			self.da.db = os.path.join(self.sa.d['path_to_entry_databases'], self.args.N)
			self.da.create_db()
			self.da.new_table("entries").add_table_column("entry_number", "integer").add_table_column("entry_text", "text").add_table_column("entry_keywords", "text").add_table_column("entry_date", "date").create_table()

			if self.da.result  == "FAIL":
				self.top_fail.add(self.da.result + ": " + self.da.status)
				self.EXIT_CODE = 1
				self.wt_exit()
				
			
		if self.args.C:
			"""
				Change the current entry database.
			"""
			
			self.sa.d['current_entry_database'] = self.args.C 


		if self.args.P:

			"""
				Change the template used to display Entries.
			"""

			self.sa.d['current_html_template'] = self.args.P


		if self.args.D:
			"""
				Delete a entry database.  args.D should just be the name of the database itself without the path to it.
			"""
		
			del_db = os.path.join(self.sa.d['path_to_entry_databases'], self.args.D)
			self.fw.delete_file(del_db)
			if self.fw.result == "FAIL":
				self.top_fail.add(self.fw.result + ": " + self.fw.status)
				self.EXIT_CODE = 1
				

		if self.args.R:
			"""
				Delete an html template.  args.R should just be the name of the html template itself without the path to it.
			"""
			del_templ = os.path.join(self.sa.d['path_to_html_templates'], self.args.R)
			self.fw.delete_file(del_templ)
			if self.fw.result == "FAIL":
				self.top_fail.add(self.fw.result + ": " + self.fw.status)
				self.EXIT_CODE = 1



		if self.args.S:
			"""
				Display all of the available entry databases in the terminal.
			"""

			try:
				self.show_files(wtterm.WTTermIO(), self.sa.d['path_to_entry_databases'])
			except Exception as e:
				self.top_fail.add("FAIL:  " + str(e) + " -- " + self.fio.status)
				self.EXIT_CODE = 1
			

		if self.args.L:
			"""
				Display all of the available html templates in the terminal.
			"""


			try:
				self.show_files(wtterm.WTTermIO(), self.sa.d['path_to_html_templates'], ".html")
			except Exception as e:
				self.top_fail.add("FAIL:  " + str(e) + "  -- " + self.fio.status)

			
	
		if self.args.T:
			"""
				Outputs (writes) basic information about how to structure and use the input.html file for creating entries to the input.html file.
				  (Will not execute if the -v option is passed in.)
			"""

			self.fio.content = self.sa.d['basic_input_html_file_template'].replace("\t", "")
			self.fio.input_html_path = self.sa.d['path_to_input_html_file']
			self.fio.to_input_file()
			if self.fio.result == "FAIL":
				self.top_fail.add(self.fio.result + ":  " + self.fio.status)
				self.EXIT_CODE = 1


		####	PROCESS ARGUMENTS FOR ENTRIES	####


		if self.args.v == "c":
			"""
				Create an Entry in the database.
			""" 
			self.invalid_v_opt = False
			entry = None
			self.rdbe = rdb.CreateEntry(self.current_db, "entries")				# create rdb object to add entry to db

			entry_number = self.get_latest_entry_number() + 1

			self.fio.input_html_path = self.sa.d['path_to_input_html_file']
			self.fio.from_input_file(True)										# get the text from input.html

			if self.fio.result == "FAIL":
				self.top_fail.add("FAIL: " + "Get Entry or Entries from input.html -- " + self.fio.status)
				self.EXIT_CODE = 1
			else:
				if len(self.fio.entry_list) == 1:
					self.entry_list = self.fio.entry_list
				
				if self.entry_list:
					e = self.entry_list[0]
					e.entry_number = entry_number
					e.entry_date = datetime.datetime.now().strftime("%Y-%m-%d")
					self.rdbe.create(e.entry_number, e.entry_text, e.entry_keywords, e.entry_date)
					
					if self.rdbe.result == "FAIL":
						self.top_fail.add("FAIL: " + "In CreateEntry either 0 or wrong number of rows added to the current Entry database. (Make sure input.html has only one entry.)")
						self.EXIT_CODE = 1
				else:
					self.top_fail.add("FAIL: " + "WTFileIO from_input_file(): Unable to retrieve entries from input.html.")
					self.EXIT_CODE = 1

				
		if self.args.v == "r":
			"""	
				Retrieve (read) one or more Entries from the database. 
			"""	
			self.invalid_v_opt = False
			self.rdbe = rdb.ReadEntry(self.current_db, "entries")
			self.verb_actions()
			
			if self.rdbe.result == "FAIL":
				self.top_fail.add("FAIL: " + "Read Entries from database -- " + self.rdbe.status)
				self.EXIT_CODE = 1
			
			else:
				self.fio.entry_list = self.entry_list
				self.fio.output_html_path = self.sa.d['path_to_output_html_file']
				self.fio.html_template_path = os.path.join(self.sa.d['path_to_html_templates'], self.sa.d['current_html_template'])
				self.fio.to_output_html()
				if self.fio.result == "FAIL":
					self.top_fail.add("FAIL: " + self.fio.status)
					self.EXIT_CODE = 1

			self.wt_exit()		


		if self.args.v == "u":
			"""	
				Select one or more Enties in the database to update.
			"""	
			self.invalid_v_opt = False
			entries_to_update = ""
			self.rdbe = rdb.UpdateEntry(self.current_db, "entries")
			self.verb_actions()

			if self.rdbe.result == "FAIL":
				self.top_fail.add("FAIL: " + "Update Entries -- " + self.rdbe.status)
				self.EXIT_CODE = 1

			for entry in self.entry_list:
				entries_to_update = entries_to_update + str(entry.entry_number) + " "

			self.sa.d['current_entries_to_update'] = entries_to_update.rstrip().lstrip()
			
			self.fio.entry_list = self.entry_list
			self.fio.to_input_file(True)

			if self.fio.result == "FAIL":
				self.top_fail.add("FAIL: " + self.fio.status)
				self.EXIT_CODE = 1

			self.wt_exit()


		if self.args.v == "d":
			"""	
				Delete one or more Entries in the database.
			"""	

			self.invalid_v_opt = False
			self.rdbe = rdb.ReadEntry(self.current_db, "entries")
			self.verb_actions()
			if self.rdbe.result == "FAIL":
				self.top_fail.add("FAIL: " + "Retrieve Entries for Deletion -- " + self.rdbe.status)
				self.EXIT_CODE = 1
			
			else:
				entry_list = self.rdbe.entry_list
				self.rdbe = rdb.DeleteEntry(self.current_db, "entries")
				self.rdbe.entry_list = entry_list
				self.verb_actions()
				self.top_ok.display(str(self.rdbe.rows_affected) + " rows deleted.", 2, 2, 2)

	
			if self.sa.d['auto_reindex_entries'] == "1":
				self.rdbe.sg.consecutive_reindex("entry_number", "entries")

		
			self.wt_exit()


		if self.args.v == "U":
			"""	
				Commit one or more updated Entries in the database.
			"""	
		
			self.invalid_v_opt = False
			self.rdbe = rdb.UpdateEntry(self.current_db, "entries")
			self.fio.from_input_file()
			if self.fio.result == "FAIL":
				self.top_fail.add("FAIL: " + " WTFileIO read entries from input.html for commit update -- " + self.fio.status)
				self.EXIT_CODE = 1
			else:
				self.rdbe.entry_list = self.fio.entry_list 
				self.rdbe.commit_update()

				if self.rdbe.result == "FAIL":
					self.top_fail.add("FAIL: RDBRecord Commit updated entries to database -- " + self.rdbe.status)
					self.EXIT_CODE = 1
				else:
					self.top_ok.display(str(self.rdbe.rows_affected) + " rows updated.", 2, 1, 1)

				if self.sa.d['auto_delete_merge_update'] == "1":							# if set to automatically delete merged updates, and 
																						# if entries were merged for update in input.html, delete
					entry_numbers = self.sa.d['current_entries_to_update']		# the entries which were merged into the remaining updates.
					delete_entries = list()
				
					for e_n in entry_numbers.split(" "):
						wr = True
						for e_nmbr in self.rdbe.entry_list:
							if e_nmbr.entry_number == int(e_n):	
								wr = False
								break
						if wr:
							delete_entries.append(e_n)
	
					if len(delete_entries) > 0:								
						de = rdb.DeleteEntry(self.current_db, "entries")
						for ent_nmbr in delete_entries:
							de.entry_list.append(E.Entry(ent_nmbr, "", "", "", "")) # just append to the DeleteEntry object's entry_list entries which
																						# have only the number of the entry to be deleted.
						de.search("entry_number", delete_entries)	

					if self.sa.d['auto_reindex_entries'] == "1":
						self.rdbe.sg.consecutive_reindex("entry_number", "entries")

			
			self.wt_exit()

		if self.args.v and self.invalid_v_opt:
			self.top_ok.display("Invalid Argument to option -v: " + self.args.v, 2, 1, 1)
			


		if self.args.A:
			"""
				Set to automatically merge updates in the database when updates form input.html are committed.
			"""
			if self.sa.d['auto_delete_merge_update'] == "1":							# if set to automatically delete merged updates, unset it.
				self.sa.d['auto_delete_merge_update'] = "0"						
				self.top_ok.display("Entries which have been merged into other Entries will not be deleted after committing update.", 2, 1, 1)

			elif self.sa.d['auto_delete_merge_update'] == "0":							# if not set to automatically delete merged updates, set it.
				self.sa.d['auto_delete_merge_update'] = "1"							
				self.top_ok.display("Entries which have been merged into other Entries will be deleted after committing update.", 2, 1, 1)
			

		if self.args.I:
			"""
				Set to automatically merge updates in the database when updates form input.html are committed.
			"""
			if self.sa.d['auto_reindex_entries'] == "1":							# if set to automatically delete merged updates, unset it.
				self.sa.d['auto_reindex_entries'] = "0"						
				self.top_ok.display("Entry numbers will not be re-indexed after update or deletion.", 2, 1, 1)

			elif self.sa.d['auto_reindex_entries'] == "0":							# if not set to automatically delete merged updates, set it.
				self.sa.d['auto_reindex_entries'] = "1"							
				self.top_ok.display("Entry numbers will be re-indexed after update or deletion so they are consecutive.", 2, 1, 1)

		if self.args.l:
			"""
				Display all keywords
			"""

			self.top_ok.display("Keywords for the database " + self.sa.d['current_entry_database'], 2, 2, 2) 
			self.show_keywords_from_entries()

		self.wt_exit()


	def verb_actions(self):
		"""
			Process the arguments for the options which work with Entries.
		"""
		
		search_scope = "has-any"


		if self.args.q:
			"""
				Target only entries whose specified columns have all corresponding search values. (Strict search.  Default is a liberal search.)
	
			"""
			search_scope = "has-all"


		if self.args.a:
			"""
				Target all entries. 
			"""

			self.rdbe.all("*")
			if self.rdbe.result == "FAIL":
				self.top_fail.add(self.rdbe.result + ": " + self.rdbe.status)

		if self.args.n:
			"""
				Target a range either entry_numbers or entry_dates.  
				Format:

						-n "from to"
						
				Args should be either for a range of entry_dates:

						-n "2017-02-11 2017-03-15"
						
				or entry_numbers:
	
						-n "2 11"
						

				all numbers/dates enclosed in double quotes, each number/date within separated only by a space
			"""

			self.args.n = self.args.n.replace(",", "")		# remove any possible commas
			range_args = self.args.n.split(" ")

			if "-" in self.args.n:
				f = range_args[0].split("-") 
				if len(f[1]) == 1:
					f[1] = "0" + f[1]
				frm = '-'.join(f)

				t = range_args[1].split("-") 
				if len(t[1]) == 1:
					t[1] = "0" + t[1]
				to = '-'.join(t)

				column = "entry_date"
			else:
				frm = int(range_args[0])
				to = int(range_args[1])
				column = "entry_number"

			self.rdbe.range(column, frm, to)
			if self.rdbe.result == "FAIL":
				self.top_fail.add(self.rdbe.result + ": " + self.rdbe.status)


		if self.args.j:
			"""
				Target the first n numbers of entries.  
				Format:
						-h "n"
			
						-h 10
		
			"""

			head_number = 5
			if self.args.j.isdigit():
				head_number = self.args.j
		
			self.rdbe.head(head_number)
			if self.rdbe.result == "FAIL":
				self.top_fail.add(self.rdbe.result + ": " + self.rdbe.status)


		if self.args.t:

			tail_number = 5
			if self.args.t.isdigit():
				tail_number = self.args.t
		
			self.rdbe.tail(tail_number)
			if self.rdbe.result == "FAIL":
				self.top_fail.add(self.rdbe.result + ": " + self.rdbe.status)


		if self.args.e:
			"""
				Target the entries with the passd-in keywords 
				Format:
						-e "word1 word2 word3 word4"

				words enclosed in quotes separated only by a space
			"""

			keywords = self.add_modulos(self.args.e.split(" "))
	
			self.rdbe.search(["entry_keywords"], keywords, None, search_scope)
			if self.rdbe.result == "FAIL":
				self.top_fail.add(self.rdbe.result + ": " + self.rdbe.status)


		if self.args.f:
			"""
				Target the entries with the passd-in date.  Date must in the format YYYY-MM-DD (Year-Month-Day).  Year, Month and Day
				must be numbers (Day is the Calendar date.)
				Format:
						-f "YYYY-MM-DD"

						-f "2017-02-11"

			"""

			self.rdbe.search(["entry_date"], [self.args.f], None, search_scope)
			if self.rdbe.result == "FAIL":
				self.top_fail.add(self.rdbe.result + ": " + self.rdbe.status)
	

		if self.args.m:
			"""
			Target the entries with the passd-in date-member. date-member must be a number.

				Format:

						-m "date-member date-member-number"

						-m "year 2017"

						-m "month 2"

						-m "day 11"

			"""

			members = self.args.m.split(" ")
			if len(members[1]) == 1:
				members[1] = "0" + members[1]

			self.rdbe.search("entry_date", members[1], members[0])
			if self.rdbe.result == "FAIL":
				self.top_fail.add(self.rdbe.result + ": " + self.rdbe.status)


		if self.args.s:

			"""
				Target the entries with the passd-in text.

				Format:
						-s "word1 word2 word3 word4"

				words enclosed in quotes, separated only by a space
			"""

			text = self.add_modulos(self.args.s.split(" "))
			self.rdbe.search("entry_text", text, None, search_scope)
			if self.rdbe.result == "FAIL":
				self.top_fail.add(self.rdbe.result + ": " + self.rdbe.status)


		if self.args.g:
			"""
				Target the entries by the list of passed-in numbers.  (Can only work with entry_numbers, passed in as strings and converted
				to a list.

				Format:
						-g "n1 n2 n3 n4"

						-g "1 2 4 10"


				numbers enclosed in quotes, separated only by a space
			"""

			numbers = self.args.g.split(" ")
			self.rdbe.search("entry_number", numbers, None, search_scope)
			if self.rdbe.result == "FAIL":
				self.top_fail.add(self.rdbe.result + ": " + self.rdbe.status)


		self.entry_list = self.rdbe.entry_list


	def i_menus(self):

		"""
			1. setup the main menu (above) as a list in the i_menu object
			2. go into a loop
			3. clear and display main menu
			4. wait for input to prompt - user inputs a number
			5. Each number the user may enter is a key in a dictionary to a value.  The value is actually either a function
				self.top_ok.display("Entry numbers will be re-indexed after update or deletion so they are consecutive.", 2, 1, 1)
				or a function call which is executed, performing the work for the option.
		"""
		i_menu = wtterm.WTTermIO()
		i_menu.display_messages = ["Settings Main Menu:",
									"1. Set the full (absolute) path to the directory where the html templates are to be stored.",
									"2. Set the full (absolute) path to the directory where the entry databases are to be stored.",
									"3. Set the current html template to be used for displaying entries. ",
									"4. Set the full (absolute) paths to the input.html and output.html files. ",
									"5. Set the current entry database.",
									"6. Delete one or more html templates.",
									"7. Delete one or more entry databases.",
									"8. Auto-delete Merged Entries on Update (Selecting this toggles to set it or not, based on its current status.)",
									"9. Set to display fail and success messages on after executions are completed.",
									"10. Clear and re-display menu.",
									"11. Exit."]

		def one(m):
			"""	
			Set the full (absolute) path to the directory where the html templates are to be stored.
			"""	
	
			loc = self.sa.d['path_to_html_templates']
			
			m.display("Html templates current location: " + loc, 3, 1, 0)
			m.display("To accept this, press enter or enter the full path to the folder/directory where html templates are to be stored.", 3, 2, 2)
			u_i = m.prompt(": ", 3, 1, 0)
			if u_i == '':
				self.sa.d['path_to_html_templates'] = loc
			else:
				self.sa.d['path_to_html_templates'] = u_i

		def two(m):
			"""	
			Set the full (absolute) path to the directory where the entry databases are to be stored.
			"""	

			loc = self.sa.d['path_to_entry_databases']
			
			m.display("Entry databases current location: " + loc, 3, 1, 0)
			m.display("To accept this, press enter or enter the path to where entry databases are to be stored.", 3, 2, 2)
	
			u_i = m.prompt(": ", 3, 1, 0)

			if u_i == '':
				self.sa.d['path_to_entry_databases'] = loc
			else:
				self.sa.d['path_to_entry_databases'] = u_i


		def three(m):
			"""	
			Set the current html template to be used for displaying entries.
			"""	
			m.display("Available html templates: ", 3, 1, 1)
			self.show_files(m, self.sa.d['path_to_html_templates'], ".html")
			m.display("Current html template: " + self.sa.d['current_html_template'], 3, 1, 1)
			u_i = m.prompt(" (press enter to skip): ", 3, 1, 0)
			if u_i != '':
				self.sa.d['current_html_template'] = u_i


		def four(m):
			"""
			Set the full (absolute) paths to the directory to the input.html and output.html files. 
			"""	
			m.display("The current path to input.html: " + self.sa.d['path_to_input_html_file'], 3, 1, 1)
			u_i = m.prompt("Enter the new full (absolute) path (press enter to skip) : ", 3, 1, 0)

			if u_i != '':
				self.sa.d['path_to_input_html_file'] = u_i

			m.display("The current path to output.html: " + self.sa.d['path_to_output_html_file'], 3, 1, 1)
			u_i = m.prompt("Enter the new full (absolute) path (press enter to skip) : ", 3, 1, 0)

			if u_i != '':
				self.sa.d['path_to_output_html_file'] = u_i

				p_i = flwk.FileWork(os.path.join(u_i, "input.html"))
				p_o = flwk.FileWork(os.path.join(u_i, "output.html"))

			
	#		p_i.write_to_file(self.sa.d['basic_input_html_file_template'])
	#		p_o.write_to_file(" ")
	#		p_i.close_file()
	#		p_o.close_file()
			
	
		def five(m):
			"""	
			Set the current entry database.
			"""	
			m.display("The current entry_database is: " + self.sa.d['current_entry_database'], 3, 1, 1)
			m.display("Available entry databases: ", 3, 1, 1)
			self.show_files(m, self.sa.d['path_to_entry_databases'])
			u_i = m.prompt(" (press enter to skip): ", 3, 1, 0)
			if u_i != '':
				self.sa.d['current_entry_database'] = u_i


		def six(m):
			"""
			Delete one or more html templates.
			"""
			m.display("Enter the names of one or more templates, each one separated ONLY by a single space. ", 3, 1, 1)
			m.display("Available html templates: ", 3, 1, 1)
			self.show_files(m, self.sa.d['path_to_html_templates'], ".html")
			u_i = m.prompt(" (press enter to skip): ", 3, 1, 0)
			if "default.html" in u_i:
				m.display("The default.html file cannot be deleted from this menu.", 3, 2, 1)
				u_i = m.prompt(" press enter to continue: ", 3, 1, 0)
			else:
				delete_files = u_i.split(" ")
				if delete_files != '':
					for df in delete_files:
						self.fio.delete(os.path.join(self.sa.d['path_to_html_templates'], df))
			
									
		def seven(m):
			"""
			 Delete one or more entry databases.
			"""
			m.display("Enter the names of one or more Entry databases, each one separated ONLY by a single space. ", 3, 1, 1)
			m.display("Available Entry databases: ", 3, 1, 1)
			self.show_files(m, self.sa.d['path_to_entry_databases'])
			u_i = m.prompt(" (press enter to skip): ", 3, 1, 0)

			delete_files = u_i.split(" ")
			if delete_files != '':
				for df in delete_files:
					self.fio.delete(os.path.join(self.sa.d['path_to_entry_databases'], df))
			


		def eight(m):
			"""
			 Set to automatically delete Entries if their contents have been merged with another Entry during an update. 
			"""
			if self.sa.d['auto_delete_merge_update'] == "1":
				m.display("Entries will not be deleted from their Entry database if they are merged in an update.", 3, 1, 1)
				self.sa.d['auto_delete_merge_update'] = "0"
				
			elif self.sa.d['auto_delete_merge_update'] == "0":
				m.display("Entries will be deleted from their Entry database if they are merged in an update.", 3, 1, 1)
				self.sa.d['auto_delete_merge_update'] = "1"

			u_i = m.prompt(" press enter to continue: ", 3, 1, 0)

		def nine(m):
			"""
			Set to display fail and success messages after executions are completed.
			"""
			u_i = list()
			m.display("Display fail messages after execution? ", 3, 1, 1)
			u_i.append(m.prompt("Enter 'y' or 'n': ", 3, 1, 0))
			
			m.display("Display success messages after execution?", 3, 1, 1)
			u_i.append(m.prompt("Enter 'y' or 'n': ", 3, 1, 0))
			
			ind = 0
			for i in u_i:
				if i != 'y':
					if i != 'n':
						u_i[ind] = 'y'
				ind = ind + 1



		def ten(m):
			"""
			Clear and re-display menu.
			"""
			try:
				if os.name == "nt":
					os.system('cls')
				else:
					os.system('clear')
			except Exception as e:
				pass
			finally:
				m.pad(2, 2)
				if m.border_char != " ":
					m.border_char = "*"
					m.display(None, 2, 1, 1)


		ten(i_menu)
		msg_dict = {'1' : one,
					'2' : two,
					'3' : three,
					'4' : four,
					'5' : five,
					'6' : six,
					'7' : seven,
					'8' : eight,
					'9' : nine,
					'10' : ten}

		while(1):

			ten(i_menu)
			selection = i_menu.prompt("Select from the above menu: ", 2, 1, 0)

			if selection == "11":
				i_menu.display_messages = []
				i_menu.border_char = " "
				ten(i_menu)
				break

			elif selection == "":
				selection = i_menu.prompt("Select from the above menu: ", 2, 1, 0)
			else:
				msg_dict[selection](i_menu)       

			if not(selection in msg_dict):           
				self.wt_exit()			


	def add_modulos(self, words):

		i = 0
		for v in words:                # surround search terms with modulos to match a substring in the database
			words[i] = '%' + v + '%'
			i = i + 1
	
		return words
	


	def show_files(self, m, path, file_ext=None):
		m.border_char = " "
		m.word_display(self.fio.get_file_names(path, file_ext), 3, 1, 1)
		m.border_char = "*"


	def show_keywords_from_entries(self):

		kr = rdb.ReadEntry(self.current_db, "entries")	

		kr.all()
		keywords = list()
		for e in kr.entry_list:
			k = filter(None, list(OrderedDict.fromkeys([i.replace(" ", "").replace(",", " ") for i in str(e.entry_keywords).split(" ")])))
			keywords = keywords + k
			keywords = filter(None, list(OrderedDict.fromkeys(keywords))) 


		i = 0
		self.top_ok.display("", 0, 1, 0)
		for word in keywords:
			self.top_ok.display(word, 1, 0, 0)
			if i == 4:
				self.top_ok.display("", 0, 1, 0)
				i = 0
			i = i + 1
				
		self.top_ok.display("", 0, 2, 0)

		if kr.result == "FAIL": 	
			self.top_fail.add(kr.result + ": (in show_keywords_from_entries, read from keywords table of current db) " + kr.status)


	def get_latest_entry_number(self):
		
		dln = rdb.ReadEntry(self.current_db, "entries")
		dln.tail(1)

		if len(dln.entry_list) == 0:
			return 0		
		else:
			return dln.entry_list[0].entry_number


	def wt_exit(self):
		"""
			Display all success and fail messages as specified in wtab_app db and exit with self.EXIT_CODE.
		"""

		try:
			if self.sa.d['display_fail_messages'] == "1":
				if len(self.top_fail.display_messages) > 0:
					self.top_fail.pad(2, 1)
					self.top_fail.display(None, 2, 0, 1)

			if self.sa.d['display_success_messages'] == "1":
				if len(self.top_ok.display_messages) > 0:
					self.top_ok.pad(2, 2)
					self.top_ok.display(None, 1, 2, 1)
		except:
			pass

		sys.exit(self.EXIT_CODE)

