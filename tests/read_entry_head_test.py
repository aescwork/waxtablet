# -*- coding: utf-8 -*-

import unittest
import sys
import datetime 
import sqlite3

sys.path.append("../fixtures/")
sys.path.append("../waxtablet/")

import sqlitemgr
import rdbrecord


class ReadEntryHeadTest(unittest.TestCase):
	"""
		Test the head() method of the ReadEntry class. Delete a couple of the objects from the entry_list of the ReadEntry object after
		the first method call, then call the method again.
	"""

	def setUp(self):

		table = "entries"
		db = "../fixtures/test_journal"

		sg = sqlitemgr.SQLiteMgr(db)
		re = rdbrecord.ReadEntry(sg.make_conn(), table, db)
		
		self.first_head_comp = [(1, '2017-02-11'), (2, '2017-02-27'), (3, '2017-03-09'), (4, '2017-03-12'), (5, '2017-03-04'), \
								(6, '2017-03-15'), (7, '2017-04-04'), (8, '2017-04-12')]

		self.second_head_comp = [(1, '2017-02-11'), (2, '2017-02-27'), (4, '2017-03-12'), (5, '2017-03-04'), (7, '2017-04-04')]


		re.head(8)
		self.first_head = [(i.entry_number, str(i.entry_date)) for i in re.entry_list]
		self.first_head_result = re.result

		del re.entry_list[2]
		del re.entry_list[4]

		re.head()		# just use the default value for the argument to this method
		self.second_head = [(i.entry_number, str(i.entry_date)) for i in re.entry_list]
		self.second_head_result = re.result
	
				

	def test_head(self):
		self.assertEqual(self.first_head, self.first_head_comp)	
		self.assertEqual(self.second_head, self.second_head_comp)	


	def test_result(self):
		self.assertEqual(self.first_head_result, "OK")
		self.assertEqual(self.second_head_result, "OK")


if __name__ == '__main__':
	unittest.main()


