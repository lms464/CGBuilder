#!/bin/bash

set -e

comp_in=$1
out_dir=$2
if [ $# > 2 ]; then
    pro_in=$3
fi

echo " "

mk_file() {
    if [ -d "${out_dir}" ]; then
            echo "Dir exists. Please make a new directory"
    else
            mkdir ${out_dir}
    fi

    cd ${out_dir}
    echo "Working Directory: ${pwd}"
}

choose_comp_path() {
    if [ $comp_in == "Oocyte.dat" ] || [ $comp_in == "Rat.dat" ] || [ $comp_in == "Torpedo.dat" ] || [ $comp_in == "Asolectin.dat" ]; then
	    comp="/u1/home/lms464/lms464/github/JPC_Special/tasks/13_Lipidomic_Comparisons/${comp_in}"
	    echo "Lipid File: ${comp}"
	    mk_file
    elif [ $comp_in == 'rat'  ]; then
	 comp="rat"
	 mk_file
    else
	comp="${comp_in}"
        mk_file	
	if ! [ -f ${comp} ]; then
		cp ../${comp_in} ./
		echo "Lipid File: ${comp}"
	else
		echo "Lipid File: ${comp}"
	fi
    fi	
}

sel_pro() {
    if [ $# > 2 ]; then
	    pro=$pro_in
    else
    	    pro="2bg9_cropped.pdb"
    fi

    echo "Protein File: ${pro}"
}

choose_comp_path
sel_pro

echo "2bg9"&>elast.dat
date "+%H:%M:%S   %d/%m/%y"
export GMX_MAXCONSTRWARN=-1

python ../../CGBUILD/CGBuilder.py -name $pro  -con ${comp}  -e -p -x 40 -y 40 -z 35 &> build.log
#python ../../CGBUILD/CGBuilder.py -name $pro  -con ${comp} -lasym -ring -e -p -x 40 -y 40 -z 35  &> build.log
#python ../../CGBUILD/CGBuilder.py  -con ${comp} -lasym  -p -x 40 -y 40 -z 35  &> build.log
#python ../../CGBUILD/CGBuilder.py -name $pro  -con ${comp} -e -p  &> build.log


#if [ ! -f ./em0.tpr ]; then
#        exit 1
#fi

#gmx grompp -f ../martini_ff/em_kristen.mdp -c em0.pdb  -p insane0.top -maxwarn 10 -o em1 &>> build.log

#if [ ! -f ./em1.tpr ]; then
#	exit 1
#fi

#gmx mdrun -deffnm em1 -v &>> build.log
#export GMX_MAXCONSTRWARN=

#cd ../
date "+%H:%M:%S   %d/%m/%y"
