# -*- coding: utf-8 -*-

import unittest
import sys
import datetime 
import sqlite3

sys.path.append("../fixtures/")
sys.path.append("../waxtablet/")

import rdbrecord
"""
import keyval
import wtfileio
import wtterm
import controller
"""


class InstantiationTest(unittest.TestCase):

	def setUp(self):

		table = "entries"
		db = "../fixtures/test_journal"

		conn = sqlite3.connect(db)
		self.ce = rdbrecord.CreateEntry(conn, table, db)
		self.re = rdbrecord.ReadEntry(conn, table, db)
		self.ue = rdbrecord.UpdateEntry(conn, table, db)
		self.de = rdbrecord.ReadEntry(conn, table, db)


	def test_result(self):
		self.assertEqual(self.ce.result, "None")	
		self.assertEqual(self.re.result, "None")	
		self.assertEqual(self.ue.result, "None")	
		self.assertEqual(self.de.result, "None")	


	def test_status(self):
		self.assertEqual(self.ce.status, "None")
		self.assertEqual(self.re.status, "None")
		self.assertEqual(self.ue.status, "None")
		self.assertEqual(self.de.status, "None")




if __name__ == '__main__':
	unittest.main()


