#! /bin/bash


function chain_rename () {
	
	set -e	
	
	cat $6 | head -1 > $7

	cat $6 | while read line; do
		if [[ $line != \ATOM* ]] ; then
			continue
		fi
	
		if [[ ${line:21:1} = "A" ]]
			then 
				s1=${line:0:21}
				s2=$1
				s3=${line:22}
				echo "$s1$s2$s3" >> $7
		fi
	
			if [[ ${line:21:1} = "B" ]]
			then 
				s1=${line:0:21}
				s2=$2
				s3=${line:22}
				echo "$s1$s2$s3" >> $7
		fi
	
			if [[ ${line:21:1} = "C" ]]
			then 
				s1=${line:0:21}
				s2=$3
				s3=${line:22}
				echo "$s1$s2$s3" >> $7
		fi
	
			if [[ ${line:21:1} = "D" ]]
			then 
				s1=${line:0:21}
				s2=$4
				s3=${line:22}
				echo "$s1$s2$s3" >> $7
		fi
	
			if [[ ${line:21:1} = "E" ]]
			then 
				s1=${line:0:21}
				s2=$5
				s3=${line:22}
				echo "$s1$s2$s3" >> $7
		fi
	done

	cat $6 | tail -1 >> $7
}

chain_rename "F" "G" "H" "I" "J" 2bg9_cropped.pdb temp1.pdb 
#chain_rename "K" "L" "M" "N" "O" 2bg9_cropped.pdb temp2.pdb 
#chain_rename "P" "Q" "R" "S" "T" 2bg9_cropped.pdb temp3.pdb 
