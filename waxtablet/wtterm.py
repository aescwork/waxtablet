"""

..	currentmodule:: waxtablet
	:platform: Unix, Windows
	:synopsis:  manage all output to the terminal.

.. moduleauthor:: aescwork@protonmail.com

"""

"""
	file: wtterm.py
"""

import sys


class WTTermIO():

	def __init__(self):

		self.display_messages = list()
		self.tab_nmbr = 0 
		self.fore_line_space_nmbr = 0 
		self.aft_line_space_nmbr = 0
		self.tabs = "\t"
		self.aft_line_spaces = ""
		self.fore_line_spaces = ""
		self.top_pad = ""
		self.bottom_pad = ""
		self.border_char = "*"

	def add(self, content):

		"""
			Add content to the display_messages list.
			Args:
				content:	Matter to add to the display_messages list.
		"""


		self.display_messages.append(content)

	def pad(self, top=1, bottom=1):
		"""
			Specify the number of newlines before and after anything is displayed in the terminal with the display() method.
			Args:
				top (int):		number of newlines before output
				bottom (int):	number of newlines after output
		"""

		self.top_pad = "\n" * top
		self.bottom_pad = "\n" * bottom


	def prompt(self, to_prompt, nt=1, fnls=0, anls=0):
		"""
			Output a question and receive input from the user.  Return the user input to the calling code.
			Args:
					to_prompt:	The question or statement to output in the terminal (prompt).
					nt:			The number of tabs to output before displaying the prompt.
					nls:		The number of line spaces (newlines) to output before displaying the prompt.

			Returns:
					user_input	The User input.
		"""

		
		self.tabs_spaces(nt, fnls, anls)
		if sys.version_info[0] < 3:
			user_input = raw_input(self.format_content(to_prompt))
		else:
			user_input = input(self.format_content(to_prompt))
	
		return user_input 


	def display(self, content=None, nt=None, fnls=None, anls=None):

		"""
			Output formatted display of all display_messages in the terminal.  If an argument is passed in for content,
			print content only and exit.

			Args:
					content:	If passed in, just print the content, not the display_messages.
					nt (str):	The number of tabs to create for output.
					fnls (str):	The number of line spaces to create before the output.
					anls (str):	The number of line spaces to create after the output.
		"""

		self.tabs_spaces(nt, fnls, anls)
		if content:
			sys.stdout.write(self.format_content(content))
		else:
			chars = 0
			try:
				# calculate the number of characters to display as a border based on the biggest element in display_messages, or default to 10
				chars = len(filter((lambda x: len(x)==len(max(self.display_messages, key=len))), self.display_messages)[0]) if chars < 10 else 10	
			except:
				chars = 10

			dec = self.border_char * chars

			sys.stdout.write(self.top_pad)
			sys.stdout.write(self.format_content(dec))

			for dm in self.display_messages:
				sys.stdout.write(self.format_content(dm))

			sys.stdout.write(self.format_content(dec))
			sys.stdout.write(self.bottom_pad)


	def format_content(self, content):
		"""
			Format the content with the specified tabs before the content and line spaces (newlines) after.
	
		"""
		return self.fore_line_spaces + self.tabs + str(content) + self.aft_line_spaces


	def tabs_spaces(self, nt=0, fnls=0, anls=0):
		"""
			Set the number of tabs and new lines (line_spaces).
			Args:
					nt (str):	The number of tabs to create for output.
					nls (str):	The number of line spaces to create for output.
		"""
		

		if nt:
			nmbr_tabs = nt
		else:
			nmbr_tabs = self.tab_nmbr

		if fnls:
			fore_nmbr_spaces = fnls
		else:
			fore_nmbr_spaces = self.fore_line_space_nmbr

		if anls:
			aft_nmbr_spaces = anls
		else:
			aft_nmbr_spaces = self.aft_line_space_nmbr 


		self.tabs = "\t" * nmbr_tabs
		self.fore_line_spaces = "\n" * fore_nmbr_spaces
		self.aft_line_spaces = "\n" * aft_nmbr_spaces


	def word_display(self, content, nt, fnls, anls):
		"""
			Display single words in a formatted manner (two columns).
			
			Args:
				content (list):	The words to be displayed.

		.. note:: Used to display keywords or files in the html_templates or entry databases directories.

		"""
		i = 0
		l_c = len(content)
		swap_list = None
		if len(self.display_messages) > 0:				# If there are messages in the self.display_messages list, swap them
			swap_list = self.display_messages 	# over to a temporary list to save them.
			self.display_messages = []

		while(1):
			if i >= l_c:
				break
			if i == l_c - 1:
				self.display_messages.append(content[i])
				i = i + 1 
			else:
				self.display_messages.append(content[i] + "\t\t" + content[i+1])
				i = i + 2 

		self.display(None, nt, fnls, anls)

		if swap_list:
			self.display_messages = swap_list


