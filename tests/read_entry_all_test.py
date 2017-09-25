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

class ReadEntryAll(unittest.TestCase):

	"""
		Test the all() method of the ReadEntry class by checking the retrieved objects' entry numbers against a comparison list.
	"""

	def setUp(self):

		table = "entries"
		db = "../fixtures/test_journal"

		sg = sqlitemgr.SQLiteMgr(db)
		conn = sg.make_conn()
		
		self.entry_numbers_comp = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

		self.re = rdbrecord.ReadEntry(conn, table, db)
		self.re.all()
		self.entries = self.re.entry_list
		self.all_result = self.re.result


	def test_all(self):
			
		for i in range(1,15):
			self.assertEqual(self.entry_numbers_comp[i], self.entries[i].entry_number)

	def test_result(self):
		self.assertEqual(self.re.result, "OK")



if __name__ == '__main__':
	unittest.main()





