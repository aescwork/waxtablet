# -*- coding: utf-8 -*-

import unittest
import sys
import datetime 
import sqlite3

sys.path.append("../fixtures/")
sys.path.append("../waxtablet/")

import sqliteminor
import sqlitemgr
import rdbrecord
import entry


class CreateEntryTest(unittest.TestCase):

	"""
		Test this class by creating an entry in the test_journal database, then:
			1. Test all the numbers of entries in the database.
			2. Test the contents returned by a read on the database using the number for the added entry as a referant.
			3. Test the number returned from the CreateEntry create() method: (should just be 1).
	"""

	def setUp(self):

		numbers_list = list()
		table = "entries"
		db = "../fixtures/test_journal"

		sg = sqlitemgr.SQLiteMgr(db)
		conn = sg.make_conn()
		self.sm = sqliteminor.SQLiteMinor(conn, table)
		
		test_entry = entry.Entry(16, "<h2 class='title'>A test Title</h2><p>This is a test entry.  No Godlore to speak of.</p>",\
							"test godlore", datetime.date(2017,	6, 25) , table, db)

		
		self.number_added_comp = 1
		self.entry_numbers_comp = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
		self.added_entry_matter_comp = [(16, "<h2 class='title'>A test Title</h2><p>This is a test entry.  No Godlore to speak of.</p>", '2017-06-25', 'test godlore')] 

		self.ce = rdbrecord.CreateEntry(conn, table, db)
		self.number_added = self.ce.create(test_entry.entry_number, test_entry.entry_text, test_entry.entry_keywords, test_entry.entry_date)
		self.create_result = self.ce.result
		self.entry_numbers = [i[0] for i in self.sm.read_all("entry_number")]
		self.added_entry_matter = self.sm.read_search_rows("entry_number", 16)

		self.sm.delete("entry_number", 16)


	def test_create(self):
		self.assertEqual(self.number_added, self.number_added_comp)	
		self.assertEqual(self.entry_numbers, self.entry_numbers_comp)	
		self.assertEqual(self.added_entry_matter, self.added_entry_matter_comp)	


	def test_result(self):
		self.assertEqual(self.create_result, "OK")


			
	
if __name__ == '__main__':
	unittest.main()


