
import sys

sys.path.append("../waxtablet/")

import wtterm

if __name__ == '__main__':

	w = wtterm.WTTermIO()
	w.add("Here is sentence one!")
	w.add("Here is sentence two!")
	w.add("Here is sentence three!")
	w.add("Here is sentence four!")

	w.pad(1, 1)
	#w.display(None, 2, 1, 1)

	#w.display(w.prompt("What would you like to enter? Enter something: ", 2, 0, 0), 2, 1, 1)
	
	w.border_char = ""
	words = "Odhinn Sleipnir Skadhi Baldur Freyr Freyja Loki Thor Brisingamen"
	w.word_display(words.split(" "), 2, 1, 1) 
