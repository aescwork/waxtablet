"""

..	currentmodule:: waxtablet
	:platform: Unix, Windows
	:synopsis: python application to create, read, update and delete log entries, and display them via html.



"""

"""
import os
import sys
"""

class Entry():


	def __init__(self, entry_number, entry_text, entry_keywords, entry_date, entry_db):

		"""
			A class which is a structure for the Entry object which is used by waxtablet to work with the log entries.
			Each log entry either retrieved from or heading to the database has an object.
			row[0] = entry_number			# type: int
			row[1] = entry_text				# type: string
			row[2] = entry_date				# type: datetime.date
			row[3] = entry_keywords			# type: string (keywords seperated by a single whitespace)
			row[4] = table					# type: string
			row[5] = db						# type: string
		"""

		self.entry_number = entry_number			
		self.entry_text = entry_text				
		self.entry_date = entry_date				
		self.entry_keywords = entry_keywords
		self.entry_db = entry_db

