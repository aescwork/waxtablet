

import sys

sys.path.append("../waxtablet/")

import entry as e

if __name__ == '__main__':


#     def __init__(self, entry_number, entry_text, entry_keywords, entry_date, entry_db):

	entry_data = [[1, "Text for the first entry.", "text first generic-entry test", "2017-2-11", "entries"],
				[2, "Text for the second entry.", "text second generic-entry test progress", "2017-2-12", "entries"],
				[3, "Text for the third entry.", "text third generic-entry test progress", "2017-2-12", "entries"],
				[4, "Text for the fourth entry.", "text fourth generic-entry test progress", "2017-2-20", "entries"],
				[5, "Text for the fifth entry.", "text fifth generic-entry test", "2017-2-20", "entries"],
				[6, "Text for the sixth entry.", "text sixth generic-entry test", "2017-2-21", "entries"],
				[7, "Text for the seventh entry.", "text seventh generic-entry test", "2017-3-1", "entries"]]

	delete_words = ["generic-entry", "progress"]
	entries = list()
	for ed in entry_data:
		entries.append(e.Entry(ed[0], ed[1], ed[2], ed[3], ed[4]))


	for entry in entries:
		print "\t", entry.entry_number, " ", entry.entry_text, " ", entry.entry_keywords, " ", entry.entry_date, " ", entry.entry_db

	print "\n\tAttempting to remove delete_words...\n"

	for entry in entries:
		for w in delete_words:
			if w in entry.entry_keywords:
				entry.entry_keywords = entry.entry_keywords.replace(" " + w, "")


	for entry in entries:
		print "\t", entry.entry_number, " ", entry.entry_text, " ", entry.entry_keywords, " ", entry.entry_date, " ", entry.entry_db
