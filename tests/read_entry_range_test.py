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


class ReadEntryRange(unittest.TestCase):
	"""

		Test the range method of the ReadEntry class. The ReadEntry object can return entries immediately populated from information in 
		the database or it can return entries already in its entry_list attribute.  The ReadEntry object will only search in the database
		if there are no (0) entry objects in its entry_list:
			1. Get a range of entries by number from the database
			(remove some entries from the entry_list to test the retrieval from the entry_list)
			2. Get a range of entries by number from the ReadEntry object's entry_list
			3. Get a range of entries by date from the database 
			(remove some entries from the entry_list to test the retrieval from the entry_list)
			4. Get a range of entries by date from the ReadEntry object's entry_list

	"""

	def setUp(self):

		table = "entries"
		db = "../fixtures/test_journal"

		sg = sqlitemgr.SQLiteMgr(db)
		conn = sg.make_conn()
		re = rdbrecord.ReadEntry(conn, table, db)
 
		""" 
			range of entries by number tests	      
		"""       

		self.first_range_call_comp = [(2, '2017-02-27'), (3, '2017-03-09'), (4, '2017-03-12'), (5, '2017-03-04'), (6, '2017-03-15'), \
									(7, '2017-04-04'), (8, '2017-04-12'), (9, '2017-04-20')]

		self.second_range_call_comp = [(2, '2017-02-27'), (3, '2017-03-09'), (4, '2017-03-12'), (6, '2017-03-15'), (7, '2017-04-04'), (9, '2017-04-20')]


		re.range("entry_number", 2, 9)		# get a range of entries from the database of entry_numbers 2 thru 9
		self.first_range_call = [(i.entry_number, str(i.entry_date)) for i in re.entry_list]
		self.first_range_call_result = re.result
		
		del re.entry_list[3]				# delete a couple of entries from the ReadEntry object's entry_list
		del re.entry_list[5]

		re.range("entry_number", 2, 9)		# get a range of entries from ReadEntry object's entry_list of entry_numbers 2 thru 9
		self.second_range_call = [(i.entry_number, str(i.entry_date)) for i in re.entry_list]
		self.second_range_call_result = re.result


		""" 
			range of entries by date tests	      
		"""  
 
		re.entry_list = []					# start over by clearing out the ReadEntry object's entry_list    

		self.first_range_call_date_comp = [(3, '2017-03-09'), (4, '2017-03-12'), (6, '2017-03-15'), (7, '2017-04-04'), (8, '2017-04-12'), \
											(9, '2017-04-20'), (10, '2017-04-22'), (11, '2017-04-30'), (12, '2017-05-04')]

		self.second_range_call_date_comp = [(3, '2017-03-09'), (4, '2017-03-12'), (6, '2017-03-15'), (8, '2017-04-12'), (9, '2017-04-20'), \
											(10, '2017-04-22'), (12, '2017-05-04')]


		re.range("entry_date", "2017-03-09", "2017-05-05")  
		self.first_range_call_date = [(i.entry_number, str(i.entry_date)) for i in re.entry_list] 
		self.first_range_call_date_result = re.result

		del re.entry_list[3]
		del re.entry_list[6]

		re.range("entry_date", "2017-03-09", "2017-05-05")  
		self.second_range_call_date = [(i.entry_number, str(i.entry_date)) for i in re.entry_list] 
		self.second_range_call_date_result = re.result 


	def test_range(self):
		self.assertEqual(self.first_range_call, self.first_range_call_comp)	
		self.assertEqual(self.second_range_call, self.second_range_call_comp)	
		self.assertEqual(self.first_range_call_date, self.first_range_call_date_comp)	
		self.assertEqual(self.second_range_call_date, self.second_range_call_date_comp)	


	def test_result(self):
		self.assertEqual(self.first_range_call_result, "OK")
		self.assertEqual(self.second_range_call_result, "OK")
		self.assertEqual(self.first_range_call_date_result, "OK")
		self.assertEqual(self.second_range_call_date_result, "OK")



if __name__ == '__main__':
	unittest.main()




