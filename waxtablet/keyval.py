"""

..	currentmodule:: waxtablet
	:platform: Linux, Unix, Windows
	:synopsis:  

.. moduleauthor:: aescwork@protonmail.com


"""

import sqlmg
import sqlmin


class KvDict(dict):
		
	"""
		A class working with the KeyVal dictionary, including accessing the database to read from and update values in the columns of the
		selected table.  This class supports a python dictionary and a database from the dictionary can populate itself and to which it can update.
	"""

	def __init__(self, sm, key_col, val_col):

		self.sm = sm
		self.kc = key_col
		self.vc = val_col
		rows = self.sm.read_all()
		if rows:
			for row in rows:
				dict.__setitem__(self,row[0],row[1])
			
	def __setitem__(self,key,value):
		
		dict.__setitem__(self,key,value)
		self.sm.update(self.vc, value, self.kc, key)


class KeyVal(object):
	"""
		Get values from a database table and put them in a dictionary.  This is for working with only two columns of a table, 
		with the first column being the 'key', and the other being the 'value' of key-value pairs. If a value is assigned to the 
		dictionary of the object of this class, write it to the database as well.
	"""

	def __init__(self, db, table, key_col, val_col):
		

		"""
		Args: 
			db (str):		the name of/path to the database file.
			table (str):	the table in the database to be accessed.

		"""
		
		self.sg = sqlmg.SQLiteMgr(db)
		self.sm = sqlmin.SQLiteMinor(self.sg.make_conn(), table)
		self.status = "None"
		self.result = ""

		try:
			self._d = KvDict(self.sm, key_col, val_col)	# a dictionary to hold the values from the table
			self.result = "OK"
		except Exception as e:
			self.result = "FAIL"
			self.status = "In KeyVal, initialize KvDict: ", self._d.sm.status, ", ", str(e)

	@property
	def d(self):
		return self._d


