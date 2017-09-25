# -*- coding: utf-8 -*-

import unittest
import sys
import datetime 
import sqlite3

sys.path.append("../fixtures/")
sys.path.append("../waxtablet/")

import sqlitemgr
import rdbrecord


class ReadEntryTailTest(unittest.TestCase):
	"""
		Test the tail() method of the ReadEntry class. Delete a couple of the objects from the entry_list of the ReadEntry object after
		the first method call, then call the method again.
	"""

	def setUp(self):

		table = "entries"
		db = "../fixtures/test_journal"

		sg = sqlitemgr.SQLiteMgr(db)
		re = rdbrecord.ReadEntry(sg.make_conn(), table, db)
		
		self.first_tail_comp = [(8, '2017-04-12'), (9, '2017-04-20'), (10, '2017-04-22'), (11, '2017-04-30'), \
								(12, '2017-05-04'), (13, '2017-05-12'), (14, '2017-06-15'), (15, '2017-06-22')]

		self.second_tail_comp =	[(9, '2017-04-20'), (11, '2017-04-30'), (12, '2017-05-04'), (14, '2017-06-15'), (15, '2017-06-22')]


		re.tail(8)
		self.first_tail = [(i.entry_number, str(i.entry_date)) for i in re.entry_list]
		self.first_tail_result = re.result

		del re.entry_list[2]
		del re.entry_list[4]

		re.tail()		# just use the default value for the argument to this method
		self.second_tail = [(i.entry_number, str(i.entry_date)) for i in re.entry_list]
		self.second_tail_result = re.result
	
				

	def test_tail(self):
		self.assertEqual(self.first_tail, self.first_tail_comp)	
		self.assertEqual(self.second_tail, self.second_tail_comp)	


	def test_result(self):
		self.assertEqual(self.first_tail_result, "OK")
		self.assertEqual(self.second_tail_result, "OK")


if __name__ == '__main__':
	unittest.main()


