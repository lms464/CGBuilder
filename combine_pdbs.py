"""
This script will take all PDB files in present directory and combine them into
one file.

Usage:
cd $your_directory
python3 combine_pdbs.py

This can be made smarter by changing the glob command to be more discriminant
"""

import glob


def indx_format(input_val, width):
	"""
	PDF format has fixed width columns. This proc will format your input so
	that it fills the prescribed width with blank spaces to the left. 

	Arguments:
	input_val: the item you wish to format (could be str, int, float, etc)
	width: the column width of the element you're writing to pdb
	"""

	#cast to string so we can concatenate spaces to the left
	strval = str(input_val)
	
	#measure string length
	length = len(strval)

	#error check
	if width-length < 0:
		print("You have exceeded the fixed width allowed for this data!")
		return
	elif width-length == 0:
		return strval

	#concatenate empty spaces to the left
	final_value = (' '*(width-length)+strval)

	return final_value


def combine():
	"""
	This script will take all PDB files in present directory and combine them into
	one file.
	"""

	#grab all the pdbs in the current directory
	files = glob.glob("*.pdb")

	#create counter for index numbers
	indx_ctr = 1

	#create an outfile
	with open("merged.pdb", "w") as output_pdb:

		#write first line in PDB format
		output_pdb.write("CRYST1    1.000    1.000    1.000  90.00  90.00  90.00 P 1           1 \n")
		
		#iterate through input files
		for file in files:

			#read them in
			with open(file, "r") as input_pdb:
				file_contents = input_pdb.readlines()

			#filter out the CRYST, END, or empty lines
			for line in file_contents:
				if line.startswith("CRYST") or line.startswith("END") or line.startswith("\n"):
					continue

				#replace the index number to keep numbering consistent
				line = line.replace(line[6:11], indx_format(indx_ctr, 5))

				#save the residue info for the TER line
				res_info = indx_format(line[17:26], 15)

				#print line to output file
				output_pdb.write(line)

				#increment index counter
				indx_ctr = indx_ctr+1

			#end with a TER line
			ter_line = "TER   " + indx_format(indx_ctr, 5) + res_info + "\n"
			output_pdb.write(ter_line)
			indx_ctr = indx_ctr+1

		#end file
		output_pdb.write("END")


if __name__ == "__main__":
	combine()
