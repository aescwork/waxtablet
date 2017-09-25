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
import setup_db_objects

def get_results(entry_list):
	return [(entry.entry_number, str(entry.entry_date)) for entry in entry_list]


class ReadEntrySearch(unittest.TestCase):

	"""

		Test the search method of the ReadEntry class. The ReadEntry object can return entries immediately populated from information in 
		the database or it can return entries already in its entry_list attribute.  The ReadEntry object will only search in the database
		if there are no (0) entry objects in its entry_list.  Search is either for terms in entry_number, entry_text and/or entry_keywords,
		or for a date-member in entry_date:

			1. search the database for some values in entry_text and entry_keywords -- liberal search, values can appear anywhere		
			2. search the database for some values in entry_text and entry_keywords -- strict search, all values must appear in specified columns

			3. search the database for rows with a certain date-member in entry_date -- liberal search, values can appear anywhere
			4. search the database for rows with a certain date-member in entry_date -- strict search, all values must appear in specified columns 

			5. search the database for entries with a specific date


			(search the database for some values in entry_text and entry_keywords -- liberal search, values can appear anywhere)
			7. search the resulting entry_list for some values in entry_text and entry_keywords -- liberal search, values can appear anywhere

			(search the database for some values in entry_text and entry_keywords -- liberal search, values can appear anywhere)
			8. search the resulting entry_list for some values in entry_text and entry_keywords -- strict search, all values must appear in specified columns

			9. search the entry_list for entries with a certain date-member in entry_date 


			10. search the entry_list for an entry with a specific date

		The basic idea is that, given the same entry data available to each,  the ReadEntry object will return the same results from 
		selecting from the entries in its entry_list attribute as it will a read on the database.
	"""

	def setUp(self):

		table = "entries"
		db = "../fixtures/test_journal"

		sg = sqlitemgr.SQLiteMgr(db)
		sg2 = sqlitemgr.SQLiteMgr(db)
		conn = sg.make_conn()
		conn2 = sg2.make_conn()
		sm = sqliteminor.SQLiteMinor(conn2, table)
		re = rdbrecord.ReadEntry(conn, table, db)
 

		self.text_keywords_liberal_comp = [(1, '2017-02-11'), (2, '2017-02-27'), (3, '2017-03-09'), (5, '2017-03-15'), (6, '2017-03-15'), \
											(9, '2017-04-20'), (11, '2017-04-30'), (12, '2017-05-04'), (14, '2017-06-15'), (15, '2017-06-22')]

		self.text_keywords_strict_comp = [(12, '2017-05-04')]
		self.date_member_comp = 	[(3, '2017-03-09'), (4, '2017-03-12'), (5, '2017-03-15'), (6, '2017-03-15')]
		self.date_search_comp = [(5, '2017-03-15'), (6, '2017-03-15')]



		""" 
			Database searches		
		"""       
		
		re.entry_list = []				# clear out the entry_list to force ReadEntry to read from the database
		re.search(["entry_text", "entry_keywords"], ["%Odhinn%", "%Aesir%"])
		self.text_keywords_liberal_db_result = re.result
		self.text_keywords_liberal_db = get_results(re.entry_list)

		re.entry_list = []			
		re.search(["entry_text", "entry_keywords"], ["%Odhinn%", "%Aesir%"], None, "has-all")
		self.text_keywords_strict_db_result = re.result
		self.text_keywords_strict_db = get_results(re.entry_list)

		re.entry_list = []			
		re.search("entry_date", "03", "month")
		self.date_member_db_result = re.result
		self.date_member_db = get_results(re.entry_list)


		re.entry_list = []			
		re.search(["entry_date"], ["2017-03-15"])
		self.date_search_db_result = re.result
		self.date_search_db = get_results(re.entry_list)


		""" 
			entry_list searches		
		"""       

		re.entry_list = setup_db_objects.populate_entry_object_list(sm)		#re-populate the entry_list of the ReadEntry object with all 
																			#the entries from the database
		re.search(["entry_text", "entry_keywords"], ["Odhinn", "Aesir"])
		self.text_keywords_liberal_el_result = re.result
		self.text_keywords_liberal_el = get_results(re.entry_list)


		re.entry_list = setup_db_objects.populate_entry_object_list(sm)
		re.search(["entry_text", "entry_keywords"], ["Odhinn", "Aesir"], None, "has-all")
		self.text_keywords_strict_el_result = re.result
		self.text_keywords_strict_el = get_results(re.entry_list)

		re.entry_list = setup_db_objects.populate_entry_object_list(sm)
		re.search("entry_date", "03", "month")
		self.date_member_el_result = re.result
		self.date_member_el = get_results(re.entry_list)


		re.entry_list = setup_db_objects.populate_entry_object_list(sm)
		re.search(["entry_date"], ["2017-03-15"])
		self.date_search_el_result = re.result
		self.date_search_el = get_results(re.entry_list)

		


	def test_search(self):
		self.assertEqual(self.text_keywords_liberal_db, self.text_keywords_liberal_comp)	
		self.assertEqual(self.text_keywords_liberal_el, self.text_keywords_liberal_comp)	
		self.assertEqual(self.text_keywords_strict_db, self.text_keywords_strict_comp)	
		self.assertEqual(self.text_keywords_strict_el, self.text_keywords_strict_comp)	
		self.assertEqual(self.date_member_el, self.date_member_comp)	
		self.assertEqual(self.date_member_db, self.date_member_comp)	
		self.assertEqual(self.date_search_db, self.date_search_comp)	
		self.assertEqual(self.date_search_el, self.date_search_comp)	


	def test_result(self):
		self.assertEqual(self.text_keywords_liberal_db_result, "OK")
		self.assertEqual(self.text_keywords_strict_db_result, "OK")
		self.assertEqual(self.text_keywords_liberal_el_result, "OK")
		self.assertEqual(self.text_keywords_strict_el_result, "OK")
		self.assertEqual(self.date_member_db_result, "OK")
		self.assertEqual(self.date_member_el_result, "OK")
		self.assertEqual(self.date_search_el_result, "OK")
		self.assertEqual(self.date_search_db_result, "OK")

	

if __name__ == '__main__':
	unittest.main()




