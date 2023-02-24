import numpy as np
import subprocess as subp
import sys
import os
import cat_update as ct
import glob
import sys


def BuildMultiPro(pdb,nPro,shape,box_size):
    nPro=int(nPro)
    if nPro <= 1:
        print(">> No reason to run this script..")
        print(">> Exiting now..")
        sys.exit()   
    
    subp.call("mkdir MultiPro",shell=True)
    
    if shape == "circle":
        sep_angle = (2*np.pi)/nPro
        radius = box_size/3
        for i in range(0,nPro):
            x = np.cos(i*sep_angle)*radius
            y = np.sin(i*sep_angle)*radius
            subp.call("gmx editconf -f ./%s -o MultiPro/%s_%d.pdb -translate %f %f 0" %(pdb,pdb[0:-4],i,x,y),shell=True)
    elif shape == "grid":
        grid_dim = np.ceil(np.sqrt(nPro))
        gridpoint_sep = box_size/(grid_dim+1)
        for i in range(0,int(grid_dim)):
            y = i*gridpoint_sep*-1
            for j in range(0,int(grid_dim)):
                if i*grid_dim+j == nPro:
                    break
                x = j*gridpoint_sep
                subp.call("gmx editconf -f ./%s -o MultiPro/%s_%d.pdb -translate %f %f 0" %(pdb,pdb[0:-4],((i*grid_dim)+j),x,y),shell=True)





    subp.call("vmd -e ~/CGBuilder/BuildMultiProt/chain_name_temp.tcl",shell=True)
    if len(glob.glob("./new_proteins/*.pdb")) == nPro:
        subp.call("rm -rf MultiPro/",shell=True)
    else:
        print("\n>> %s" % str(len(glob.glob("./new_proteins/*.pdb"))))
        print("\n>> Something has broke! It might be your path..")
        sys.exit()
    subp.call("cd new_proteins",shell=True)
    ct.protein_lists(pdb)
    subp.call("rm -rf new_proteins",shell=True)

    subp.call("vmd -e ~/CGBuilder/BuildMultiProt/pre_martinize.tcl",shell=True)
BuildMultiPro(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
#BuildMultiPro("5x29_0_vert.pdb", 7, "grid",40)