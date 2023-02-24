proc pre_martinize {outname} {
	set sel [atomselect top all]
	set chains [lsort -unique [$sel get chain]]
	$sel delete

	for {set i 0} {$i < [llength $chains]} {incr i 5} {
		set sel [atomselect top "chain [lindex $chains $i] [lindex $chains [expr $i+1]] [lindex $chains [expr $i+2]] [lindex $chains [expr $i+3]] [lindex $chains [expr $i+4]]"]
		$sel set chain "[lindex $chains [expr $i/5]]"
		$sel delete
	}

	set sel [atomselect top all]
	$sel writepdb $outname
	$sel delete
}

set PATH "./*_multi.pdb"
set file [glob ${PATH}] 

mol load pdb $file

pre_martinize $file

mol delete top

exit