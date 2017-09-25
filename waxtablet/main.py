"""

..	currentmodule:: waxtablet
	:platform: Unix, Windows
	:synopsis:  

.. moduleauthor:: aescwork@protonmail.com


"""
import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "src"))

import wtterm
import controller

def get_args():

	parser = argparse.ArgumentParser()
	group = parser.add_argument_group()

	group.add_argument("-v", "--verb", dest='v',  metavar='', help="Pass in one of four possible arguments -- \
								c: add a new entry\
								r: get one or more entries based on entry selection options\
								u: update one or more entries based on entry selection options\
								d: delete one or more entries based on entry selection options\
								U: The text and keywords of Entries to be edited are written to the input.html file with the u argument. \
									After the information has been modified in the input.html file, use this option to read \
									the information from the input.html file back into the database.") 

	group.add_argument("-a", "--all", dest='a', nargs='?',const=" ", metavar='', help="Target all Entries in the current Entry Database.")

	group.add_argument("-n", "--range", dest='n', metavar='', help="Target a range of Entries. Use for entry numbers (Ex. -n 2 12) or entry dates\
					 (Ex. -n 2017-03-11 2017-04-21).") 

	group.add_argument("-j", "--head",  dest='j', nargs='?',const=" ", metavar='', help="Target the first n number of Entries in the current\
						 Entry Database (If no argument is passed with the option, the default is 5).")

	group.add_argument("-t", "--tail",  dest='t', nargs='?',const=" ", metavar='', help="Target the last n number of Entries in the current\
						 Entry Database (If no argument is passed with the option, the default is 5).")

	group.add_argument("-e", "--keywords-search", dest='e', nargs='?',const=" ", metavar='', help="Target the Entries which have the passed-in keywords.\
						  Pass in all the keywords together surrounded by quotes,\ each keyword separated only by a single space.")

	group.add_argument("-f", "--date-search",  dest='f', metavar='', help="Target the Entries with passed-in date. \
						 Date must be in the format YYYY-MM-DD (year month day).") 

	group.add_argument("-m", "--date-member-search",  dest='m', metavar='', help="Target entries with a day (a numbered calendar date) a month\
							 (by number, 1 - 12) or a year.  Argument is the option followed by the date-member and the numerical value\
							 to search, in quotes, like: -m \"year 2017\" or -m \"month 2\" or -m \"day 11\".") 
	
	group.add_argument("-s", "--text-search", metavar='', dest='s', nargs='?', const=" ", help="Target entries containing the text passed in as an argument following this option.") 
	
	group.add_argument("-g", "--group-search", dest='g', metavar='', help="Target entries whose entry_numbers match the numbers passed \
						in as an argument following this option.") 

	group.add_argument("-q", "--strict-query", dest='q', nargs='?',const=" ", metavar='', help="Target only entries whose specified columns have all corresponding\
					 search values.")

	group.add_argument("-l", "--display-keywords", dest='l', nargs='?',const=" ", metavar='', help="Display all keywords in entries for the current\
						 entry database in the terminal.")

	group.add_argument("-A", "--auto-delete", dest='A', nargs='?',const=" ", metavar='', help="If two or more entries are written to the input.html file for an update\
						 and two or more are then merged, delete the entry or entries which were merged into the other entry. (See manual).")

	group.add_argument("-I", "--auto-reindex-entries", dest='I', nargs='?',const=" ", metavar='',\
						 help="Automatically re-number Entries in database after deletion or update so they are consecutive.(See manual).")

	group.add_argument("-N", "--new-entry-db", dest='N', metavar='', help="Create a new Entry database.  Ex. -N my-new-entry-database.") 

	group.add_argument("-C", "--change-to-entry-db", dest='C', metavar='', help="Change to a another Entry database. Ex. -C my-other-database.") 

	group.add_argument("-D", "--delete-entry-db", dest='D', metavar='', help="Delete an Entry database. Ex. -D my-new-entry-database.")

	group.add_argument("-S", "--show-all-entry-dbs", dest='S', nargs='?', const=" ", metavar='', help="Show All entry-databases.")

	group.add_argument("-P", "--change-template", dest='P', metavar='', help="Change to a new html template for displaying the entry contents.\
						  (The template will written to output.html.)") 

	group.add_argument("-L", "--show-all-templates", dest='L', nargs='?',const=" ", metavar='', help="Show all html templates.")

	group.add_argument("-R", "--delete-template", dest='R', metavar='', help="Delete an html template.") 

	group.add_argument("-M", "--settings-main-menu", dest='M', nargs='?',const=" ", metavar='', help="Show a menu to set/initialize the values for settings \
						in the waxtablet application database.")

	group.add_argument("-T", "--input-template", dest='T', nargs='?',const=" ", metavar='', help="Outputs (writes) basic information about how to \
						structure and use the input.html file for creating entries to the input.html file.")

	
	return parser.parse_args()


def main():

	args = get_args()
	if not len(sys.argv) > 1:
		wtterm.WTTermIO().display("waxtablet: Please enter one or more options with appropriate arguments.", 3, 2, 2)	
		sys.exit(1)

	controller.Controller(args)



