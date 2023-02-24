
# cd new_proteins
# python3
# from cat import *
# protein_lists()
# new molecule : "merge.pdb"

import os
import glob

def protein_lists(pdb):
    pdb_list = glob.glob("./new_proteins/*.pdb")
    length = len(pdb_list)
    outfile = open("./%s_multi.pdb"%(pdb[0:-4]),'w')
    for n in pdb_list:
        file_index = pdb_list.index(n)
        infile = open(n, "r")
        for text in infile:
                words = text.split()
                if len(words) > 0:
                    if len(text) == 0:
                        break
                    elif (words[0] == "END" and file_index < length ):
                        pass
                    elif (words[0] == "CRYST1" and file_index != 0):
                        pass
                    else:
                        outfile.write(text)
        infile.close()
    outfile.write("END")
    outfile.close()
