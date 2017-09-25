"""

..	currentmodule:: waxtablet 
	:platform: Unix, Windows
	:synopsis:  simple class template

.. moduleauthor:: aescwork@protonmail.com


"""

import os
import sys
import flwk
import entry
import datetime
from collections import OrderedDict

"""
	file: wtfileio.py
"""

class WTFileIO():

	"""
		This class does the following:
		1. Output the basic text-data structure template to the input.html file
		2. Read text for one or more Entries from the input.html file and put the information into Entry objects.
		3. Output Entry data to the input.html file for update.
		4. Composing the content of the output.html file by outputting the text of an html template file to output.html 
			breaking the output at the appropriate point to output Entry data to the output.html file, then finishing the 
			output of the html template file to output.html.
		5. Outputting the Manual to output.html using the current html template.
		6. Get and return to the calling code all file names from the entry database directory.
		7. Get and return to the calling code all file names from the html template directory.
	"""

	def __init__(self, table, db, input_html_path=None, output_html_path=None, html_template_path=None):

		"""

		Args: 
			file_path: (str)	The full path to the file which the WTFileIO object is work with.
		"""

		self.status = ""
		self.result = "None"

		self.input_html_path = input_html_path
		self.output_html_path = output_html_path
		self.html_template_path = html_template_path
		self.table = table
		self.db = db
		self.db_name = os.path.split(self.db)[1].replace("-", " ").replace("_", " ")
		self.content = None
		self.entry_list = list()
		self.e = entry.Entry(0, "", "", "", "")
		self.fw_to = flwk.FileWork()
		self.fw_from = flwk.FileWork()


	def to_input_file(self, output_entries=False):

		"""
		1. Output the basic text-data structure template to the input.html file
		3. Output Entry data to the input.html file for update.

			Args:
				output_entries (bool):	If True, output the contents of entry_list to the input.html file.
		"""

		try:
	
			self.fw_to.file_path = self.input_html_path
			self.fw_to.write_to_file("")		# empty out the input.html file
			if output_entries and self.entry_list:
				for entry in self.entry_list:		
					self.fw_to.append_to_file("<!-- BEGIN ENTRY -->\n"\
						+ "<!-- NUMBER: " + str(entry.entry_number)+ " -->\n"\
						 + "<!-- DATE: " + str(entry.entry_date) + " -->\n"\
						+ "<!-- KEYWORDS: " + str(entry.entry_keywords) + " -->\n"\
						+ "<!-- TEXT: -->\n" +str(entry.entry_text) + "\n\n")


			elif self.content: 
				self.fw_to.write_to_file(self.content)
			
			self._stat_res(self.fw_to.result, self.fw_to.status)
		except Exception as e:
			self._stat_res("FAIL", "In WTFileIO to_input_file(): " + str(e) + self.fw_to.status)
		finally:
			self.fw_to.close_file()


	def from_input_file(self, create=False):

		"""
		2. Read text for one or more Entries from the input.html file and put the information into Entry objects.
		Args:
			create (bool):	If True, this stops the loop before it can append a second Entry object to the entry_list.
							This is for a call to this method when used to create a new Entry in the current entry-database.

		"""

		line = ""
		i = 0
		concat_text = False
		brk = False

		try:
			self.fw_from.file_path = self.input_html_path
		
			while(1):
				line = self.fw_from.iterate_through_file("n")
				if line == "EOF":
					self.fw_from.iterate_through_file("s")
					brk = True


				elif "<!-- BEGIN ENTRY -->" in line and i > 0:
					if create and brk:
						self.entry_list.append(self.e)
						length = len(self.entry_list)
						if length > 1:							# prevent more than one list element being returned to controller.py when creating
							for ent in self.entry_list:			# a new entry.  The rule is that we only want the zeroth entry.
								if len(self.entry_list) == 1:
									break
								else:
									del(self.entry_list[length - 1])
						break

					self.entry_list.append(self.e)
					if brk:
						break
					if i > 1:
						self.e = entry.Entry(0, " ", " ", " ", " ")
					concat_text = False
				elif "<!-- NUMBER: " in line and not concat_text:
					number = line.rstrip().lstrip()[13:-4]
					if number.isdigit():
						self.e.entry_number = int(number)

				elif "<!-- DATE: " in line and not concat_text:
					date = line.rstrip().lstrip()[11:-4]
					if "-" in date:
						d = date.split("-")
						self.e.entry_date = datetime.date(int(d[0]),int(d[1]), int(d[2]))
					

				elif "<!-- KEYWORDS: " in line and not concat_text:
					keywords = line[15:-4]
					keywords = ' '.join(filter(None, list(OrderedDict.fromkeys([k.replace(" ", "").replace(",", "") for k in keywords.split(" ")]))))
					self.e.entry_keywords = keywords

				elif "<!-- TEXT: -->" in line and not concat_text: 
					concat_text = True	

				elif concat_text and line != "\n":
					self.e.entry_text = self.e.entry_text + line 
				i = i + 1
	
			self._stat_res(self.fw_from.result, self.fw_from.status)

		except Exception as e:
			self._stat_res("FAIL", self.fw_from.status + " " + str(e))
		finally:
			self.fw_from.close_file()


	def to_output_html(self):

		"""
		4. Composing the content of the output.html file by outputting the text of an html template file to output.html 
			breaking the output at the appropriate point to output Entry data to the output.html file, then finishing the 
			output of the html template file to output.html.
		5. Outputting the Manual to output.html using the current html template.
		"""

		res = None
	
		try:
			self.fw_to.file_path = self.output_html_path
			self.fw_from.file_path = self.html_template_path
			self.fw_to.write_to_file(" ")
			while(1):
				line = self.fw_from.iterate_through_file("n")
				if "<!-- INSERT ENTRIES -->" in line:
					if self.entry_list: 
						for entry in self.entry_list:
							self.fw_to.append_to_file("\n<div class=\"entry\">"\
											+ "\n<p class=\"entry_keywords\">" + str(entry.entry_keywords) + "</p>"\
											+ "\n" + str(entry.entry_text)\
											+ "\n<p class=\"entry_number\">(" + str(entry.entry_number) + "</p>"\
											+ "\n<p class=\"entry_date\">" + str(entry.entry_date) + ")</p>"\
											+ "\n<hr class=\"entry-bottom-line\"></hr>\n"\
											+ "\n</div>\n")

				elif line == "EOF":
					self.fw_from.iterate_through_file("s")
					self.fw_to.close_file()
					break
				else:
					if "db_name" in line:
						l = line.replace("db_name", self.db_name)
						self.fw_to.append_to_file(l)
					else:
						self.fw_to.append_to_file(line)

			self._stat_res(self.fw_from.result, self.fw_from.status)
		except Exception as e:
			self._stat_res(self.fw_to.result + ": (to output.html) " + self.fw_from.result + ": (template.html)",\
				self.fw_to.status + ": (to output.html) " + self.fw_from.status + ": (to template.html) " + str(e))
		finally:
			self.fw_from.close_file()
			self.fw_to.close_file()
		return res


	def get_file_names(self, path, file_ext=None):

		"""
		6. Get and return to the calling code all file names from the entry database directory.
		7. Get and return to the calling code all file names from the html template directory.

		Args:
			path (str):	The complete (absolute) path to the directory -- either the database file or the html template file.
  
		"""
		
		ret = list()
		res = list()
		try:
			res = os.listdir(path)
			if file_ext:
				for p in os.listdir(path):
					if file_ext in p:
						ret.append(p)
			else:
				ret = res
			self._stat_res("OK", "")						
		except Exception as e:
			self._stat_res("FAIL", "In wtfileio get_file_names(): " + str(e))						
			

		return ret


	def delete(self, path):
		
		self.fw_to.delete_file(path)
		self._stat_res(self.fw_to.result, self.fw_to.status)


	def _stat_res(self, result, status):
		
		self.result = result
		self.status = status



