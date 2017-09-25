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


class ReadEntryAll(unittest.TestCase):

	def setUp(self):

		table = "entries"
		db = "../fixtures/test_journal"

		conn = sqlite3.connect(db)
		self. = .(, ,)


	def test_method(self):
		self.assertEqual(self., self.)	


	def test_result(self):
		self.assertEqual(self., self.)



if __name__ == '__main__':
	unittest.main()


