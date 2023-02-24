import glob
import subprocess as subp

def Standard_Top(proName,fl):                                                                             # After being built, the .top files do not have the right
                                                                                                           # itp files. This funciton adds them and protein 
        print("################################################################################\n")        # files based on where there was a protein or not
        print(">>> Altering Topology file of: %s...\n" % fl)
        cAb = 0
        line=[]
        new_top=open('temp', 'w')
        
        line.append('#include "../martini_ff/martini_v2.2.itp"')                                            # Standard 5 with or without protein
        line.append('#include "../martini_ff/martini_v2.0_solvents.itp"')
        #line.append('#include "../martini_ff/martini_v2.0_lipids_all_201506.itp"')
        line.append('#include "../martini_ff/martini_v2.0_CHOL_02.itp"') 
        line.append('#include "../martini_ff/martini_lipid_all.itp"')
        line.append('#include "../martini_ff/martini_v2.0_ions.itp"')       
        
        print(">>> Added lipid and solution .itp files...\n")
        
        if proName is not None:
            line.append('#include "../martini_ff/martini_v2.2_aminoacids.itp"')                             # Only if protien exists
            nPro = len(glob.glob("./Protein_*.itp"))
            for nPro in glob.glob("./Protein_*.itp"):
                line.append('#include "Protein_%s.itp"' %nPro[10])
            print(">>> Added protein and aminoacid .itp files...\n")
        
        for i in range(len(line)):
            new_top.write(line[i]+'\n')
        
        line=[]
        f = open(fl+'.top', 'r')
        
        with open(fl+'.top','r') as f:                                                                             # I build a temporary file I write everything to,
            next(f)                                                                                         # then delete to original top file and replace it with
            for line in f:                                                                                  # the temp file
                if line.startswith('#'): continue
                if line.startswith('Protein'):
                    cAb+=1
                    if cAb>1:
                        if proName is not None:
                            p = [gloob[10] for gloob in glob.glob("./Protein_*.itp")]
                            for j in range(len(p)):
                                new_top.write('Protein_'+p[j]+'        1\n')
                        continue
                else:
                    new_top.write(line)
        f.close()
        print(">>> Moddifed File")
        new_top.close()
        subp.call("rm -f "+fl+".top",shell=True)
        subp.call("mv temp "+fl+'.top', shell=True ) 
        print("################################################################################\n\n")
        return

def Harmonic_top(fl):
    line = []
    new_top = open('tmp.log', 'w')
    sys = fl[6]
    with open(fl+".top") as f:
        for l in f:
            if l.startswith('#include "../martini_ff/'): line.append(l)
            else: break 
        for c in [gloob[8] for gloob in glob.glob('Protein_*.itp')]:
            line.append('#include "Protein_%s.itp"' % c)
            line.append('#ifdef RUBBER')
            line.append('#include "Harmonic_%s%s.itp"' % (c,sys))
            line.append('#endif')
        for l in f:
            if l.startswith('#'): continue
            else: line.append(l)   
    f.close()
    for l in line:
        new_top.write(l.split('\n')[0]+'\n')
    new_top.close()
    subp.call("mv -f tmp.log %s" %(fl+'.top') , shell=True)
    return 
    
def Propofol_top(fl, nmol):
    line = []
    new_top = open('tmp.log', 'w')
    with open(fl+".top") as f:
        for l in f:
            if l.startswith('#'): line.append(l)
            else: break
        line.append('#include "propfal.itp"')
        for l in f:
            if l.startswith('#'): continue
            else: line.append(l)          
        line.append('PFL              %s' % nmol)   
    for l in line:
        new_top.write(l.split('\n')[0]+'\n')
    f.close()
    new_top.close()
    subp.call("mv -f tmp.log %s.top" %fl, shell=True )
    return
