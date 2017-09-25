import os
import sys
import errno


def install_dirs_files():

	# This function installs the additional necessary files for waxtablet in the user's home directory.     
	# 
	# The home directory is ascertained by first trying to find the normal (non-privileged, non-root) user name.
	# This is done by looking at the directory path where this setup.py file is located, then figuring out the user name and user's home directory 
	# from that.  This code makes a probably safe assumption that the  waxtablet source code will be downloaded to either the user's 
	# (normal) home directory or in a directory beneath it.  
	# 
	# The code which splits up the cur_dir path is from Python Cookbook by David Asher and Alex Martelli.  Source:
	# https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch04s16.html
	# 

	ERR_MSG = "\r\n\t\tUnable to install additional directories and files into the user's home directory.\r\n"
	ERR_MSG = ERR_MSG + "\t\tTry copying the io-files, html-templates and entry-databases directories into the user's home directory manually.\r\n"
	
	user_name = None
	home_dir = ""

	cur_dir = os.path.abspath(os.path.dirname(__file__))

	try:					
		os_name = os.name 
		allparts = []
		while 1:							# split up the path into its parts
			parts = os.path.split(cur_dir)
			if parts[0] == cur_dir:
				allparts.insert(0, parts[0])
				break
			elif parts[1] == cur_dir:
				allparts.insert(0, parts[1])
				break
			else:
				cur_dir = parts[0]
				allparts.insert(0, parts[1])


		dir_index = 0
		b = False
		for part in allparts:				# now figure out the normal user name its home directory
			home_dir = os.path.join(home_dir, part)
			if b:
				user_name = allparts[dir_index]
				break

			if os_name == 'nt':
				if part == "Users":
					b = True
			if os_name == 'posix':
				if part == "home":
					b = True

			dir_index = dir_index + 1

		if not os.path.isdir(home_dir):		# check to make sure home_dir actually exists.  If not, don't try to transfer the additional files
			sys.stdout.write(ERR_MSG)
			return

	except:
		except_msg = "\r\n\t\tError: " + str(e) + "\r\n\r\n"
		sys.stdout.write(except_msg)
		sys.stdout.write(ERR_MSG)
		return
		

	try:
		dirs_files = {"entry-databases":None, "html-templates":["default.html"], "io-files":["input.html", "output.html"], os.path.join("io-files", "css"):["media_queries.css", "waxtablet.css"]}

		if os_name == 'posix':				# if this is a linux/unix system, make the directory where the additional files go invisible.
			waxtablet_dir = ".waxtablet"	# also setup to reset file and group ownership back to the normal user name

		home_dir = os.path.join(home_dir, waxtablet_dir)

		if os.path.isdir(home_dir):		
			msg = "\r\n\r\n\t\t(" + home_dir + " already exists.)\r\n\r\n"
			sys.stdout.write(ERR_MSG)
			sys.stdout.write(msg)
			return


		os.mkdir(home_dir)
	
		for k, v in dirs_files.items():						# copy the files over
			cur_target_dir = os.path.join(home_dir, k)
			try:
				os.makedirs(cur_target_dir)
			except OSError as exc:
				if exc.errno == errno.EEXIST and os.path.isdir(cur_target_dir):
					pass
				else:
					raise

			if v:
				for f in v:
					cur_target_file = os.path.join(cur_target_dir, f)
					frm = open(os.path.join(k, f), "r")
					t = open(cur_target_file, "a")
					t.write(frm.read())
					frm.close()
					t.close()

	except Exception as e:
		EXCEPT_MSG = "\r\n\t\t" + str(e) + "\r\n"
		sys.stdout.write(ERR_MSG)
		sys.stdout.write(EXCEPT_MSG)


if __name__ == "__main__":

	install_dirs_files()
	sys.exit(0)

