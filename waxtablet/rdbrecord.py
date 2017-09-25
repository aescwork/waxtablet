"""

..	currentmodule:: waxtablet
	:platform: Unix, Windows
	:synopsis:  a python application to create, retrieve, update and delete log entries, and display them via html.

.. moduleauthor:: Vollund Leysing  aescwork@protonmail.com


"""

import os
from abc import ABCMeta, abstractmethod
import sqlmin 
import sqlmg
import entry 
import datetime
from operator import itemgetter	# try commenting this out this when running all the unit tests.  If they work without it, remove it


class RDBRecord():

	"""
		RDBRecord (Relational DataBase Record): An abstract parent class for child classes which handle creating, reading, 
		updating and deleting log entries.
	"""

	def __init__(self, db, table=None):

		self.sg = sqlmg.SQLiteMgr(db)
		self.sm = sqlmin.SQLiteMinor(self.sg.make_conn(), table)

		self.entry_list =  list()
		self.db = db
		self.result = "None"
		self.status = ""
		self.rows_affected = 0

	__metaclasss__ = ABCMeta


	@abstractmethod
	def all(self, column="*"):
		"""
		Do something with all of the entries from the table.

				
		"""

	
		
	@abstractmethod
	def range(self, column, frm, to):

		"""
		Do something with rows from a database within a range of values in the specified column.

	
		Args:
				column (str):			The name of the table column containing the values to evaluate for the range.
				frm (str) (other):		"from" --, the starting point of the range of values for the search.
				to (str) (other):		the end point of the range of values for the search.

		.. note:	

				Values are returned according to the type they are stored as in the table.  For instance, if a date is stored in a column
				whose sqlite type is DATE, a (python) datetime.date object will probably be returned.  Handle accordingly.  Moreover, values of different
				data types may be passed in with 'frm' and 'to' -- as long as they correspond with the data type of the column of the sqlite
				table, the retrieval should work.


		"""



	@abstractmethod
	def head(self, number=5):
		"""
		Do something with the first number of rows in the table or entry_list specified by the 'number' argument.

		Args:
			number (int):	the number of rows from the beginning of the table to retrieve.  The default is 5.

		"""



	@abstractmethod
	def tail(self, number=5):
		"""
		Do something with the last number of rows in the table or entry_list specified by the 'number' argument.

		Args:
			number (int):	the number of rows from the end of the table to retrieve.  The default is 5.

		"""



	@abstractmethod
	def search(self, column, search_val, date_member=None, search_scope="has-any", select_column="*"):
		"""
		Search for one or more entries in the table or entry_list based on column (db column):  

		Args:
			column (str), (list):		Table column(s) to search.
			search_val (str), (list):	The actual value for which to search.  Could also be a list (or a list of nested lists).
			date_member (str):			Possible values are "year", "month", "day".  This is for selecting
										entry objects from self.entry_list by looking for any one of the above
										in the entry_date attribute of the entry objects in self.entry_list.  (datetime.date
										objects are stored in the entry_date attribute of an entry object).
										

		"""

	def _res_stat(self, result, msg):

		sep = " "
		self.result = result
		if self.result == 'FAIL':
			if msg != "":
				sep = " -- "

		self.status = self.status + sep + str(msg)

class CreateEntry(RDBRecord):
	"""
		Class that handles updating one or more entries from a log database.	
	"""

	def create(self, entry_number, entry_text, entry_keywords, entry_date):

		"""

			Create/Insert an entry into the table.
			Args:
				entry_number:	
				entry_text:
				entry_date:
				entry_keywords:

		"""

 #   def __init__(self, entry_number, entry_text, entry_keywords, entry_date, entry_db):
		members = (entry_number, entry_text, entry_keywords, entry_date)
		
		try:
			res = self.sm.add(members)
			self._res_stat(sm.result, sm.status)

		except Exception as e: 
			self._res_stat("FAIL", self.sm.status + str(e))
			self._res_stat(self.sm.result, self.sm.status)
	
		return res



class ReadEntry(RDBRecord):
	"""
		Class that handles retrieving one or more entries from a log database.	After all of the methods in this class have
		been called, get the final rows retrieved by calling the entry_list member directly: entry_objects = read_entry_obj.entry_list
	"""

	def all(self, column="*"):

		try:
			rows = self.sm.read_all(column)
			self._populate_entry_list_objects(rows)
			self._res_stat(self.sm.result, self.sm.status)
		except Exception as e: 
			self._res_stat("FAIL", self.sm.status + str(e))


	def range(self, column, frm, to):

		if len(self.entry_list) > 0:
			try:
				temp_list = list()
				for entry in self.entry_list:
					if getattr(entry, column) >= frm and getattr(entry, column) <= to:
						temp_list.append(entry)
				
				self.entry_list = temp_list		
				self._res_stat(self.sm.result, self.sm.status)
			except Exception as e:
				self._res_stat("FAIL", str(e))

		else:
			try:
				rows = self.sm.read_range(frm, to, column)
				self._populate_entry_list_objects(rows)
				self._res_stat(self.sm.result, self.sm.status)
			except Exception as e:
				self._res_stat("FAIL", self.sm.status + str(e))


	def head(self, number=5):

		if len(self.entry_list) > 0:
			try:
				temp_list = list()
				c = 1
				self.entry_list.sort(key=lambda x: x.entry_number)	 # entry_list is a list of objects, so sort them by each object's entry_number attribute.
				for entry in self.entry_list:
					temp_list.append(entry)
					if c == number:
						break
					c = c + 1
					
				self.entry_list = temp_list
				self._res_stat(self.sm.result, self.sm.status)
			except Exception as e:
				self._res_stat("FAIL", self.sm.status + str(e))

		else:
			try:
	#			number = int(number) - 1
				rows = self.sm.read_head(str(number))	
				self._populate_entry_list_objects(rows)
				self._res_stat(self.sm.result, self.sm.status)
			except Exception as e:
				self._res_stat("FAIL", self.sm.status + str(e))
	


	def tail(self, number=5):

		self.entry_list.sort(key=lambda x: x.entry_number)	 # entry_list is a list of objects, so sort them by each object's entry_number attribute.
		e_l_size = len(self.entry_list)
		if e_l_size > 0:

			try:
				if e_l_size > number:
					temp_list = list()
					index = e_l_size - number
					for entry in self.entry_list[index:]:
							temp_list.append(entry)	

					self.entry_list = temp_list			
					self._res_stat(self.sm.result, self.sm.status)
			except Exception as e:	
				self._res_stat("FAIL", self.sm.status + str(e))

		else:
			try:
				rows = self.sm.read_tail(number)	
				self._populate_entry_list_objects(rows)
				self._res_stat(self.sm.result, self.sm.status)
			except Exception as e:	
				self._res_stat("FAIL", self.sm.status + str(e))
		

	def search(self, columns, search_val, date_member=None, search_scope="has-any", select_column="*"):

		"""
			column must be single values in a list. search_val may EITHER be single values in a list OR a list of nested lists.  
			values in search_val should NOT be pre- or appended with modulos (%) if the self.entry_list is being searched.  Searches in
			entry_text, entry_number and/or entry_keywords should be done separately from searches in entry_date.
		"""

		if len(self.entry_list) > 0:				# if there are any entries in self.entry_list, a database query was already done, so
			try:									# search self.entry_list instead
				delete_indices = list()
				search_list = list()
				col_index = 0
				for entry_index in range(0, len(self.entry_list)):	 
					hit_list = list()
					for column in columns:
						if len(search_val) > col_index:
							if search_val[col_index] is list:
								search_list = search_val[col_index]
						if len(search_val) == col_index:
							if search_val[col_index-1] is list:
								search_list = search_val[col_index-1]
						else:
							search_list = search_val

						for sv in search_list:
							if self._col_search_val(self.entry_list[entry_index], column, sv, date_member):
								hit_list.append("hit")
							else:
								hit_list.append("miss")

						col_index = col_index + 1

					if search_scope == "has-any" and ("hit" not in hit_list):
						delete_indices.append(entry_index)
					elif search_scope == "has-all" and ("miss" in hit_list):
						delete_indices.append(entry_index)
	
				for i in sorted(delete_indices, reverse=True):
					del self.entry_list[i]

				self._res_stat(self.sm.result, self.sm.status)
			except Exception as e:	
				self._res_stat("FAIL", self.sm.status + str(e))

		else:
			try:
				if date_member:
					rows = self.sm.read_by_date_part(date_member, columns, search_val)
				else:
					rows = self.sm.read_search_rows(columns, search_val, search_scope, select_column)

				self._populate_entry_list_objects(rows)
				self._res_stat(self.sm.result, self.sm.status)
			except Exception as e:	
				self._res_stat(self.sm.result, str(self.sm.status) + " -- In ReadEntry: " + str(e))




	def _col_search_val(self, entry, column, sv, date_member):

		if date_member:
			if getattr(entry.entry_date, date_member) == int(sv):
				return True
		elif str(sv) in str(getattr(entry, column)):
			return True
		else:
			return False


	def _populate_entry_list_objects(self, rows):
		"""
			Compose the Entry objects and populate entry_list with them.
		"""
		if rows:

 #   def __init__(self, entry_number, entry_text, entry_keywords, entry_date, entry_db):

	#	members = (entry_number, entry_text, entry_keywords, entry_date)
			for row in rows:
				self.entry_list.append(entry.Entry(row[0], row[1], row[2], row[3], self.db))
		
		
class UpdateEntry(RDBRecord):
	"""
		Class that handles updating one or more entries from a log database.  The range, all, head, tail, and search methods
		call the method of the same name from the ReadEntry class in order to populate the entry_list, which can then
		be passed on to another object which would be directly involved in actually modifying the contents of each entry.

		.. warning:	
		The UpdateEntry object needs to have a new, separate connection to the database for the commit_update method which 
		hasn't been used for any other operation.  Even the same UpdateEntry object which has been used for the other methods which
		retrieve data (by passing it to a ReadEntry object) cannot be used for a call to commit_update().  Either delete the object
		or create a separate UpdateEntry object with a separate database connection. If deleting the ReadEntry object, any entry_list 
		which the UpdateEntry object has from calling the other methods (or by assignment) should be copied to another variable 
		before deleting the object.
	"""



	def range(self, column, frm, to):
		"""
		Retrieves or extracts from self.entry_list all of the entries within a certain specified range, puts them in self.entry_list and passes them
		on for the calling code to modify each.

		"""


		try:
			re = ReadEntry(self.db, "entries")
			re.range(column, frm, to)
			self.entry_list = re.entry_list
			self._res_stat(self.sm.result, self.sm.status)
		except Exception as e:	
			self._res_stat("FAIL", self.sm.status + str(e))



	def all(self, column="*"):

		"""
		Retrieves all of the entries, puts them in self.entry_list and passes them on for the calling code to modify each.
		(first operation)

		"""

		try:
			re = ReadEntry(self.db, "entries")
			re.all(column)
			self.entry_list = re.entry_list
			self._res_stat(self.sm.result, self.sm.status)
		except Exception as e:	
			self._res_stat("FAIL", self.sm.status + str(e))


	def head(self, number=5):

		"""
		Retrieves or extracts from self.entry_list the first 'number' entries, puts them in self.entry_list and passes them on for the calling code to modify each.


		"""

		try:
			re = ReadEntry(self.db, "entries")
			re.head(number)
			self.entry_list = re.entry_list
			self._res_stat(self.sm.result, self.sm.status)
		except Exception as e:	
			self._res_stat("FAIL", self.sm.status + str(e))



	def tail(self, number=5):

		"""
		Retrieves or extracts from self.entry_list the last 'number' entries, puts them in self.entry_list and passes them on 
		for the calling code to modify each.


		"""

		try:
			re = ReadEntry(self.db, "entries")
			re.tail(number)
			self.entry_list = re.entry_list
			self._res_stat(self.sm.result, self.sm.status)
		except Exception as e:	
			self._res_stat("FAIL", self.sm.status + str(e))


	def search(self, column, search_val, date_member=None, search_scope="has-any", select_column="*"):

		"""
		Retrieves all entries which fall within the search criteria.  The search can be based on one or more columns, and one or more 
		values.

		 puts them in self.entry_list and passes them on for the calling code to modify each.


		"""

		try:
			re = ReadEntry(self.db, "entries")
			re.search(column, search_val, date_member, search_scope, select_column)
			self.entry_list = re.entry_list
			self._res_stat(self.sm.result, self.sm.status)
		except Exception as e:	
			self._res_stat("FAIL", self.sm.status + str(e))


	def commit_update(self):

		"""
		Calls the update method in sqlminor.  Updates entry text and entry keywords for each entry which had previously been selected
		for update.
		.. warning:	
		The UpdateEntry object needs to have a new, separate connection to the database for the commit_update method which 
		hasn't been used for any other operation.  Even the same UpdateEntry object which has been used for the other methods which
		retrieve data (by passing it to a ReadEntry object) cannot be used for a call to commit_update().  Either delete the object
		or create a separate UpdateEntry object with a separate database connection. If deleting the ReadEntry object, any entry_list 
		which the UpdateEntry object has from calling the other methods (or by assignment) should be copied to another variable 
		before deleting the object.

		"""


		try:
			if len(self.entry_list) > 0:
				for e in self.entry_list:
					self.rows_affected = self.rows_affected + self.sm.update(["entry_text", "entry_keywords"],[e.entry_text, e.entry_keywords], \
					"entry_number", e.entry_number)

					self._res_stat(self.sm.result, self.sm.status)

		except Exception as e:	
			self._res_stat("FAIL", self.sm.status + str(e))


class DeleteEntry(RDBRecord):

	"""
		Deletes entries from the specified database table.  This object is only used to delete Entries by number.  The actual selection of numbers
		to be deleted is performed beforehand by a (separate) ReadEntry object.  The entry_list of that ReadEntry object is then assigned to
		the DeleteEntry object.
		.. note:
		Make sure that the sqlmg object has the database and table names the DeleteEntry object is acting upon.
	"""

	def all(self, column="*"):

		"""
			entry_numbers must be every entry number from 1 to the number of entries there are in the database table.  The
			entry numbers must be (type) integers.
		"""
		

		try:
			entry_vals = self.get_entry_vals(column)
			
			self.rows_affected = self.sm.delete("entry_number", entry_vals) 
			self._res_stat(self.sm.result, self.sm.status)
		except Exception as e:	
			self._res_stat("FAIL", self.sm.status + str(e))


	def range(self, column, frm, to):

		"""
			Deletes entries based on either range or date.
		"""
		try:
			entry_vals = self.get_entry_vals(column)

			self.rows_affected = self.sm.delete(column, entry_vals)
			self._res_stat(self.sm.result, self.sm.status)
		except Exception as e:	
			self._res_stat("FAIL", self.sm.status + str(e))
		

	def head(self, column, number=5):

		entry_vals = list()

		try:
			column = "entry_number"
			entry_vals = self.get_entry_vals(column)
			
			self.rows_affected = self.sm.delete(column, entry_vals)
			self._res_stat(self.sm.result, self.sm.status)

		except Exception as e:	
			self._res_stat("FAIL", self.sm.status + str(e))
		

	def tail(self, column, number=5):

			
		entry_vals = list()

		try:
			column = "entry_number"

			for e in self.entry_list:
				entry_vals.append(e.entry_number)						

			entry_vals = self.get_entry_vals(column)

			self.rows_affected = self.sm.delete(column, entry_vals)
			self._res_stat(self.sm.result, self.sm.status)
		except Exception as e:	
			self._res_stat("FAIL", self.sm.status + str(e))
	
	
	def search(self, column, search_val, date_member=None, search_scope="has-any", select_column="*"):
		
		entry_vals = list()

		try:
			column = "entry_number"

			for e in self.entry_list:
				entry_vals.append(e.entry_number)						

			entry_vals = self.get_entry_vals(column)
			self.rows_affected = self.sm.delete(column, entry_vals, search_scope)
			self._res_stat(self.sm.result, self.sm.status)
		except Exception as e:	
			self._res_stat("FAIL", self.sm.status + str(e))


	def get_entry_vals(self, column):
		
		val_list = list()
		for e in self.entry_list:
			if column == "entry_date":
				val_list.append(e.entry_date)
			else:
				val_list.append(e.entry_number)

		return val_list
