#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GBuilder ver 2.0
Created on Wed Nov  9 12:08:06 2016

@author: liamsharp

This script is designed for pLGIC's!

This code should be fairly self contained. 
The get_ functions are built so one can test
and debug when nessisary. 

Topology_Editor.py IS NEEDED. Otherwise 
topology files will not work.

This script builds strings for system generation
based on commands and input files. 
"""

import argparse
import glob
import subprocess as subp
import os
import sys

from Topology_Editor import Standard_Top, Harmonic_top, Propofol_top

global PATH
PATH="/u2/home_u2/lms464"
#PATH="/Users/liamsharp/Desktop/lms464"

class CGSystem(object):
    
    #This does NOT require having a protein. It can make just a membrane
    def __init__(self, proName=None, c_in=None, l_as=None, ring=None, elast=None, posr=None, boxarray=None, asym=None, nmol=None):
        self.proName = None
        self.inPro = None
        self.c_in = c_in
        self.neur = None
        self.l_as = l_as
        self.ring = ring
        self.elast = elast
        self.elastParam = None
        self.posr = posr
        self.boxarray = boxarray
        self.asym = asym
        self.nmol = nmol
        
        if proName is not None:
            self.proName = proName[:4]
            dir_list = ["elic","gabar","glic","nachr","mixed","gpro"]
            for dl in dir_list:
                if os.path.exists("%s/PDB/%s/%s"%(PATH,dl,proName))==True:
                    self.inPro = "%s/PDB/%s/%s" %(PATH,dl,proName)
        '''if elast is not None:
            try:
                E = open("elas.txt",'r')
                #Custom elas.txt file
            except:
                E = open("%s/CGBUILD/elas.txt"%PATH)
            elastParam=E.readline()
            self.elastParam=elastParam.split()'''
                    
        
    # For testing
    def get_proName(self):
        return self.proName
    def get_inPro(self):
        return self.inPro
    def get_Cin(self):
        return self.c_in
    def getBox(self):
        return self.boxarray
    def getPFL(self):
        return self.nmol
      
   #Gets a string from a single line of the concentrtion file
    def get_concentration(self, inLine):
        if self.l_as == True:
            from Mamal_Lipid import Mamal_Lipid
            print(">>> Building asymetrical lipid membrane...")
            print(">>> Loading mamal leaflet compositions....\n")
            Line = inLine.split()
            con = Mamal_Lipid(Line)
        elif self.l_as == False:
            print(">>> You are building a model membrane... No lipid asymetry selected...\n")
            Line = inLine.split()
            con = ""
            for l,c in zip(Line[::2],Line[1::2]):
                con = "-l %s:%d "%(l,int(c)) + con
        return con
    
    # If protein is inclued write string to build CG model
    # This function does one of two things,
    #   1) adds position restraints
    #   2) adds no restraints (this requires the function
    #       groGetter to build the harmonic restraints)
    # groGetter has been implemented into script
    
    def martinizeString(self):
        if self.proName is not None:
            #if (self.elast == True):
            #    el_file = open("elast.dat","w")
            #    el_file.write("%s"%str(self.inPro)[29:33])
            #    el_file.close()
            if (self.posr == True and self.elast == False):
                mout = "python %s/martini_ff/martinize2.6.py -f %s -o %s_cg.top -x %s_cg.pdb -n %s_index.ndx -sep -dssp /u2/software/dssp/install/2.0.4/dssp -cys auto -p backbone"%(PATH
                        ,str(self.inPro),str(self.proName),str(self.proName),str(self.proName))
                print(">>> (^・x・^)")
                return mout
            elif (self.posr == True and self.elast == True):
                mout = "python %s/martini_ff/martinize2.6.py -f %s -o %s_cg.top -x %s_cg.pdb -n %s_index.ndx -sep -dssp /u2/software/dssp/install/2.0.4/dssp -cys auto -p backbone"%(
                        PATH,str(self.inPro),str(self.proName),str(self.proName),str(self.proName))

                print(">>> ∪･ω･∪")
                return mout
            
            elif (self.posr == False and self.elast == True):
                print(">>> You are building a system with only harmonic restraints. This is acceptable with small systems (<5 proteins), but is a poor idea for larger systems...\n>>>")
                mout = "python %s/martini_ff/martinize2.6.py -f %s -o %s_cg.top -x %s_cg.pdb -n %s_index.ndx -sep -dssp /u2/software/dssp/install/2.0.4/dssp -cys auto"%(
                        PATH,str(self.inPro),str(self.proName),str(self.proName),str(self.proName))
                return mout

            elif (self.posr == False and self.elast == False):
                print(">>> No restraints have been added to this protein(s)...\n>>> This protein will fall apart.../n >>> Ending build...")
                print(">>> ( ･ω･)ﾉ")
                os._exit()
        else :
            return ">>>echo 'No Protein\n(╯°□°）╯︵ ┻━┻'"
            
    
    #Builds string for cg membrane w/ or w/o protein    
    def insaneString(self):
        self.out = []
        
        # if asymetrical membranes are specified
        # this if statment builds a string for the 
        # difference in lipids.
        # If no asym... is specified, an
        # empty string is produced
        
        if self.asym is None:
            asm = ""
        else:
            asm = " -asym %s " %self.asym
        
        
        # To be used in multiple proteins. Fills in
        # the gap made in the PDB file.
        if self.ring == True:
            rang = "-ring "
        else:
            rang = ""
        
        # if specific dimentions are required
        # for membrane shape/size (no protein, 
        # or large membranes), the x, y, and z
        # dimentions are used here to make a 
        # string for the insane script
        
        if self.boxarray is None:
            box = "  "
        else:
            box = " -x %f -y %f -z %f " %(self.boxarray[0],self.boxarray[1],self.boxarray[2])
        
        if (self.c_in=="rat"):
            self.neur= "/u1/home/lms464/lms464/github/JPC_Special/tasks/13_Lipidomic_Comparisons/neuron.dat"
            f = open(self.neur)
            conc = f.read()
            f.close()
            if (self.proName is None):
                self.out.append("python "+PATH+"/martini_ff/insane2015.py -pbc hexagonal -d 15 -dz 9 -sol W -solr 0.5 "+ asm +" -o insane0.gro -p insane0.top -pbc optimal" + str(box) + str(conc) +" -dm 3 -center -salt .15 -charge auto") #changed salt to 0
            elif (self.proName is not None):
                self.out.append("python "+PATH+"/martini_ff/insane2015.py -f "+str(self.proName)+"_cg.pdb -pbc hexagonal -d 15 -dz 9 -sol W -solr 0.5 " + asm + " -o insane0.gro -p insane0.top " + str(box)+" " + str(conc) + " -dm 3 -center -salt 0.15 -charge auto "+rang+"")
            #TODO read in a file that is alread set up!
            print(self.out)
            self.c_in = "/u1/home/lms464/lms464/github/JPC_Special/tasks/13_Lipidomic_Comparisons/neuron_lip.dat"
            return self.out
        
        else:
            with open(self.c_in) as f:
                for sy,line in enumerate(f):
                    conc = self.get_concentration(line)
                    if (self.proName is None):
                        self.out.append("python "+PATH+"/martini_ff/insane2015.py -pbc hexagonal -d 15 -dz 9 -sol W -solr 0.5 "+ asm +" -o insane"+str(sy)+".gro -p insane"+str(sy)+".top -pbc optimal" + str(box) + str(conc) +"-dm 3 -center -salt .15 -charge auto") #changed salt to 0
                    elif (self.proName is not None):
                        self.out.append("python "+PATH+"/martini_ff/insane2015.py -f "+str(self.proName)+"_cg.pdb -pbc hexagonal -d 15 -dz 9 -sol W -solr 0.5 " + asm + " -o insane"+str(sy)+".gro -p insane"+str(sy)+".top " + str(box)+" " + str(conc) + "-dm 3 -center -salt 0.15 -charge auto "+rang+"")
            return self.out

    '''Generating Harmonic Bonds via this method has shown to break down for more than 4-5 proteins
    this script will now be using Martini's elastic network.'''

# Minimizes the protein structure before embedding it in a membrane
# To be used with harmonic restraints

    def gro2pdb(self,fnum):
        selection = ['1','q']
        with open("ndx_out" , 'w') as ndx_out:
            for l in selection:
                ndx_out.write(l+'\n')
        ndx_out.close()
        subp.call("gmx make_ndx -f em%d -o em_pro%d.ndx < ndx_out"%(fnum,fnum),shell=True)
        subp.call("gmx trjconv -s em%d.tpr -f em%d.gro -n em_pro%d.ndx -o Harmonic%d.pdb < ndx_out"%(fnum,fnum,fnum,fnum),shell=True)
        log.write("gmx make_ndx -f em%d -o em_pro%d.ndx < ndx_out\n\n"%(fnum,fnum))
        log.write("gmx trjconv -s em%d.tpr -f em%d.pdb -n em_pro%d.ndx -o Harmonic%d.gro < ndx_out\n\n"%(fnum,fnum,fnum,fnum))
        return

# Collects gromac id numbers to be used in VMD check
# Calls Hamonic Generator script for vmd and outputs an itp file for each chain
# This can work for multiple proteins, but has been built for only 2BG9, easily modified..
    def harmoncBuilder(self,flnum):
        import Harmonic
        for c in [gloob[10] for gloob in glob.glob("./Protein_*.itp")]:
            subp.call("grep ' BB ' Protein_"+c+".itp | awk '{print $1}' > frag"+c+".txt",shell=True)
            log.write("grep ' BB ' Protein_"+c+".itp | awk '{print $1}' > frag"+c+".txt\n\n")
        subp.call("vmd Harmonic%s.pdb -dispdev text -e %s/CGBUILD/Harmonic_Generator4.tcl"%(flnum[6],PATH),shell=True)
        log.write("vmd Harmonic%s.gro -dispdev text -e %s/CGBUILD/Harmonic_Generator4.tcl\n\n"%(flnum[6],PATH))
        Harmonic_top(str(flnum))
        Harmonic.harmonic_id_org()
        return 

    # Called if we use propofol
    def prflBuild(self,fl):

        subp.call("gmx grompp -f %s/martini_ff/em.mdp -c PFL.pdb -p PFL.top -maxwarn 10 -o em_PFL"%PATH,shell=True)
        subp.call("gmx mdrun -deffnm em_PFL -v",shell=True)
        subp.call("gmx grompp -f "+PATH+"/martini_ff/em.mdp -c "+fl+".gro -p "+fl+".top -maxwarn 10 -o em_"+fl ,shell=True)
        subp.call("gmx mdrun -deffnm em_"+fl,shell=True)
        subp.call("gmx insert-molecules -f em_"+fl+".gro -ci em_PFL.gro -nmol "+self.nmol+" -o merge_"+fl+".gro",shell=True)
        Propofol_top(fl, self.nmol)
        return
    # In atempts to not have to change mdp files by hand, I have
    # included this function to produce a md.mdp file
    # for each membrane produced.
    def MDParameters(self):
        with open(self.c_in) as cin:
            for c_i,c_line in enumerate(cin):
                c_line = c_line.split()
                if self.proName is not None: 
                    proname = "Protein"
                    if self.elast==True or self.posr==True:
                        rest = "-DRUBBER"
                    # elif self.elast==True and self.posr!=True: 
                    #     rest = "-DRUBBER"
                    # elif self.elast!=True and self.posr ==True: 
                    #     rest = "-DPOSRES"
                    else:
                        rest = ""
                elif self.proName is None: 
                    rest = " "
                grps = [cc for cc in c_line[::2]]
                if self.proName is not None: grps.append(proname) 
                grps.append("W")
                grps.append("Ion")
                if self.nmol is not None: grps.append("PFL")
                tau_t = [str(1)]*len(grps)
                ref_t = [str(323)]*len(grps)
                fl = "%s/CGBUILD/md.mdp"%PATH
                lines = []
                with open(fl) as f:
                    for line in f:
                        if line.startswith("define"):
                            if self.proName is not None:
                                lines.append("define                   = "+rest+'\n')
                                continue
                                 
                            else: continue
                        elif line.startswith("dt"):
                            lines.append("dt                       = .025\n")
                        elif line.startswith("nsteps"):
                            lines.append("nsteps                   = 200000000\n")
                        elif line.startswith("energygrps"):
                            lines.append("energygrps               = " + ' '.join(grps)+"\n")
                        elif line.startswith("nstlog"):
                            lines.append("nstlog                   = 10000\n")
                        elif line.startswith("nstenergy"):
                            lines.append("nstenergy                = 10000\n")
                        elif line.startswith("nstxout-compressed"):
                            lines.append("nstxout-compressed       = 20000\n")
                        elif line.startswith("tc-grps"): 
                            lines.append("tc-grps                  = " + ' '.join(grps)+'\n')
                            
                        elif line.startswith("tau_t"):
                            lines.append("tau_t                    = " + ' '.join(tau_t)+'\n')
                            
                        elif line.startswith("ref_t"):
                            lines.append("ref_t                    = " + ' '.join(ref_t)+'\n')
                            
                        else: lines.append(line)
                mdi = open("md"+str(c_i)+".mdp", 'w')
                for l in lines:
                    mdi.write(l)
                mdi.close()
    
    # Automates the building of CG'ed systems
    def Builder(self):

        martinize = self.martinizeString()
            
        insane = self.insaneString()
        
        for i,insn in enumerate(insane):
            global log
            log = open("CGBuilder.log", 'w')
            subp.call(martinize,shell=True)
            log.write("<<<CGBuild Log>>>\n\n")
            log.write(martinize+"\n\n")
            log.write(insn+"\n\n")
            if self.elast == True:
                subp.call(insn,shell=True)
                Standard_Top(self.proName,"insane%d"%i)
                subp.call("gmx grompp -f %s/martini_ff/em.mdp -c insane%d.gro -r insane%d.gro -p insane%d.top -o em%d -maxwarn 10"%(PATH,i,i,i,i),shell=True)
                subp.call("gmx mdrun -deffnm em%d -v"%i,shell=True)
                log.write("gmx grompp -f %s/martini_ff/em_kristen.mdp -c insane%d.gro -r insane%d.gro -p insane%d.top -o em%d -maxwarn 10\n\n"%(PATH,i,i,i,i))
                log.write("gmx mdrun -deffnm em%d -v\n\n"%i)
                self.gro2pdb(i)
                self.harmoncBuilder("insane%d"%i)
                if self.ring == True:
                    subp.call("vmd em%s.gro -dispdev text -e %s/CGBUILD/lipid_remove.tcl"%(str(i),PATH),shell=True)
                    log.write("vmd em%s.gro -dispdev text -e %s/CGBUILD/lipid_remove.tcl"%(str(i),PATH))
                    Harmonic_top("insane%d"%i)
                    if os.path.isfile("insane%d.bkp"%i) == True:
                        print(">>> Topology updated.")
                    else: 
                        print(">>> No lipids were removed. This is an issue...")
                        sys.exit()

            
            else:
                subp.call(insn,shell=True)
                Standard_Top(self.proName,"insane%d"%i )
                if self.ring == True:
                    subp.call("gmx grompp -f %s/martini_ff/em_kristen.mdp -c insane%d.gro -r insane%d.gro -p insane%d.top -o em%d -maxwarn 10"%(PATH,i,i,i,i),shell=True)
                    subp.call("gmx mdrun -deffnm em%d -v -maxh .01"%i,shell=True)
                    log.write("gmx grompp -f %s/martini_ff/em_kristen.mdp -c insane%d.gro -r insane%d.gro-p insane%d.top -o em%d -maxwarn 10\n\n"%(PATH,i,i,i,i))
                    log.write("gmx mdrun -deffnm em%d -v\n\n"%i)
                    subp.call("vmd em%d.gro -dispdev text -e %s/CGBUILD/lipid_remove.tcl"%(i,PATH),shell=True)
                    log.write("vmd em%d.gro -dispdev text -e %s/CGBUILD/lipid_remove.tcl"%(i,PATH))
                    if os.path.isfile("insane%d.bkp"%i) == True:
                        print(">>> Topology updated.")
                    else: 
                        print(">>> No lipids were removed. This is an issue...")
                        sys.exit()
                    
            if self.nmol is not None:
                self.prflBuild("insane%d"%i)
                
        self.MDParameters()
        log.write("Hurray I am ran!")
        log.close()
        return

# Takes in the martinized, and insane commands to
# build systems one after another (or one at a time).
# At the moment, commands MUST be put in in this order.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-name', action="store",required=False, dest="proName",help="Protein to be inputed.")
    parser.add_argument('-con', action="store",required=True,dest="c_in",help="Should be a text/data file in the form of LIPID1 N1 LIPID2 N2 ...")
    parser.add_argument('-lasym', action="store_true",required=False,dest="l_as",help="Tell script if there is lipid asymetry between leaflets.")
    parser.add_argument('-ring', action="store_true",required=False,dest="ring",help="Calls Insane's ring funciton to put lipids within protein. ")
    parser.add_argument('-e', action="store_true",required=False,dest="elast",help="Tells the script whether there will be harmonic networks. ")
    parser.add_argument('-p', action="store_true",required=False,dest="posr",help="If there is a position restraint on the back bone or not.")
    parser.add_argument('-x', action="store",required=False,dest="x",help="x dimentions.")
    parser.add_argument('-y', action="store",required=False,dest="y",help="y dimentions.")
    parser.add_argument('-z', action="store",required=False,dest="z",help="z dimentions.")
    parser.add_argument('-asym', action="store",required=False,dest="asym",help="difference in leaflet size (input number of lipids).")
    parser.add_argument('-nmol', action="store",required=False,dest="nmol",help="number of 'extra' molecules to add (use for propofol).")
    results = parser.parse_args()
    boxarray = None
    ''' if (results.elast == True) and (results.posr == True):
        print(">>> Choose either -e or -p, do not choose both")
        sys.exit()  '''
    if (results.x == None) or (results.y == None) or (results.z == None):
        cgSys = CGSystem(results.proName,results.c_in,results.l_as,results.ring,results.elast,results.posr,boxarray,results.asym,results.nmol)
    else:
        boxarray = [float(results.x),float(results.y),float(results.z)]
        cgSys = CGSystem(results.proName,results.c_in,results.l_as,results.ring,results.elast,results.posr,boxarray,results.asym,results.nmol)
    cgSys.Builder()
    return

def mesg():
    line = []
    line.append("\n\nHEY LIAM! Don't forget to figure out a better sorting method for -ring option!\n\n")
    line.append("\n\n\"This script is designed for pLGIC's!")
    line.append("This code should be fairly self contained.")
    line.append("Topology_Editor.py IS NEEDED. Otherwise")
    line.append("topology files will not work.")
    line.append("This script builds strings for")
    line.append("system generation based on commands")
    line.append("and input files.\n\n")
    return line

#TODO Implement    
def SubpLog(inval):
    subp.call(inval,shell=True)
    log.write(inval)

    
if __name__ == "__main__":
    for l in mesg():
        print(l)
    main()
