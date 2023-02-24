puts "Please compare the topology output order with the original topology"
puts "See insaneX.bkp \n"

proc assign {} {
	
	set protein_species [string range [glob *cg.pdb] 0 3]
	set bin [glob /u2/home_u2/lms464/github/JPC_Special/common/grace/*.tcl]
	foreach b $bin {
		if {[string match "*${protein_species}*" "${b}"]} {
			source "${b}"
			return
		}
	}
	set mes ["If you see this there is not an assign script for your protein yet.\nEndding the build."]
	error ${mes}
}

;#source ~/lms464/github/JPC_Special/common/grace/assign_helices_2BG9_CG_KW.tcl
#assign
;# The first chunk of code set up file naming and writing constant stings
;# ie: #include "../martini_ff/martini_v2.2.itp"

source /u1/home/lms464/lms464/github/JPC_Special/common/grace/assign_helices_2BG9_CG_lms2.tcl

;# Makes sure the name for the new pdb file uses the old file name
set infile [molinfo top get name]
set outfile [split $infile .]
set outfile [lindex $outfile 0]
set outfile [append outfile ".pdb"]

;# Make topology backup

set 2bRemoved ""

set W [atomselect top "resname W"]
set water [$W num]
$W delete

set CL [atomselect top {resname ION and name "CL\-"}]
set cl [$CL num]
$CL delete

set NA [atomselect top {resname ION and name "NA\+"}]
set na [$NA num]
$NA delete

set ION [atomselect top "resname ION"]

set top_index [string index $outfile 2]
exec mv insane${top_index}.top insane${top_index}.bkp
set top_update [open "insane${top_index}.top" "w"]

puts $top_update "#include \"../martini_ff/martini_v2.2.itp\""
puts $top_update "#include \"../martini_ff/martini_v2.0_solvents.itp\" "
#puts $top_update "#include \"../martini_ff/martini_v2.0_lipids_all_201506.itp\" "
puts $top_update "#include \"../martini_ff/martini_v2.0_CHOL_02.itp\" "
puts $top_update "#include \"../martini_ff/martini_lipid_all.itp\" "
puts $top_update "#include \"../martini_ff/martini_v2.0_ions.itp\" "
puts $top_update "#include \"../martini_ff/martini_v2.2_aminoacids.itp\" "

;# includes proper protein chains and adds number of proteins to topology file

set nProtein [atomselect top "name BB"]
foreach nP [lsort -unique [$nProtein get chain]] {
	if {$nP=="X"} {continue}
	puts $top_update "#include \"Protein_${nP}.itp\" "
}
puts $top_update "\n\[ system \]\n; name\n\n\[ molecules \]\n; name  number\n"

foreach nP [lsort -unique [$nProtein get chain]] {
	if {$nP=="X"} {continue}
	puts $top_update "Protein_${nP}        1"
}

$nProtein delete

;# Selects the lipids 
;# TODO set this up so it can deal with multiple builds
set heads [atomselect top "name PO4 ROH and (not resname W ION) and (not name BB SC1 to SC4)"]
set lips [lsort -unique [$heads get resname]]
set midgar [lindex [measure center $heads] 2]
$heads delete

;# Selects the lipids to be removed from the system
set removed [atomselect top "(resname $lips and name PO4 ROH) and (within 12 of name BB)"];#(within 20 of occupancy 2)"]
foreach renm [$removed get resname] rei [$removed get resid]  {
    set 2bRemoved "$2bRemoved (resname $renm and resid $rei) or "
}
$removed delete

set 2bRemoved [string range $2bRemoved 0 [expr [string length $2bRemoved] - 5]]

;# Write out the change in lipids to the new top file
;# Gromacs doesn;t seem to like this step...
;# Deleting lipids alter's the FF set up (fine)
;# But there is a mismatch between .gro and .top 
foreach h [list "z > $midgar" "z < $midgar"] {
	foreach lip $lips {
		set toTop [atomselect top "(resname $lip and name PO4 ROH and ($h)) and (not ($2bRemoved))"]
		puts $top_update "$lip          [$toTop num]"
	}
}
#puts $2bRemoved
puts $top_update "W            $water"
puts $top_update "NA+            $na"
puts $top_update "CL-            $cl"
close $top_update
set sel [atomselect top "all and (not ($2bRemoved))"]
$sel writepdb $outfile
$sel delete

puts ">>> Lipids have been removed from the center of the protein/(s)"

exit
