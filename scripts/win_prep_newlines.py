
import sys

import os



if __name__ == "__main__":



	dir_name = sys.argv[1]

	t_n = "temp.py"
	
	for f in os.listdir(dir_name):

		f = os.path.join(dir_name, f)

		from_file = open(f, "r")

		to_file = open(t_n, "a")

		for line in from_file.readlines():

			if "\n" in line:

				to_file.write(line.replace("\n", "\r\n"))

			else:

				to_file.write(line)


		from_file.close()

		to_file.close()


		os.remove(f)

		os.rename(t_n, f);


		
