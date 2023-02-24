;#Name: Harmonic_Genorator
;#Version: 4
;#Authour: Liam Sharp
if 0 {
    Logic for update: 
    1) Differences found between method in Eldyns rubberBands function and mine
    2) Inaccurate use of lower bounds
    3) Consistent simulations crash if k>750 KJ/mol

    Of importance: on the the rubberBands procedure has been updated. All
    other procedures have not shown a issue to my (Liam's) knowledge 
}

proc decayFunction {dist shift rate power} {
    if 0 {
        Stolen form Martini! Works under the assumption that dist is already converted
        from A to nm
        # The function to determine the decay scaling factor for the elastic network
        # force constant, based on the distance and the parameters provided.
        # This function is very versatile and can be fitted to most commonly used
        # profiles, including a straight line (rate=0)
        }
        set out [expr 1.0 * exp(-1.0 * $rate * ($dist - $shift)**$power)]
    return $out

}

proc setGro {chn} {
    if 0 {
        Due to Gro and vmd not sharing the same identification schema,
        I output the gro id's to be compared to vmd's. This opens the
        Appropriate file
    }
	set out [list ]
	foreach line [read [ open "frag${chn}.txt"] ] {lappend out $line}
	return $out
}

;# Figures out which vmd serial ID matches
;# which gromacs ID
proc puller {l1 l2 l3} {
	set out [list ]
	foreach l $l3 {
		lappend out [ lindex $l1 [lsearch $l2 $l] ]
	}
	return $out
}


;# Determines the number of chains (or how many proteins)
;# Assumes you have opened up a file with ONLY a protein in it
proc NumChains {} {
    set tot_beads [atomselect top "chain A to E"]
    set controlBeads [$tot_beads num]
    $tot_beads delete
    set BBSC [atomselect top "name BB SC1 to SC4"]
    set nbeads [$BBSC num]
    $BBSC delete
    set beadRatio [expr $nbeads/$controlBeads]
    return [expr 5 * $beadRatio]
}

proc get_elastic_name {} {
	;# fever dream ignore
    set el_file [open "elast.dat" r]
    set read_el_file [split [read $el_file] "/n"]
    return [lindex $read_el_file 0]
}

proc rubberBands {ref atomlist refg grolist lowerBound upperBound decayFactor decayPower forceConstant minForce fout} {
    
    if {[string length $ref]==0 || [string length $refg]==0} { 
        error ">>> Oddity noticed... Ending run\n>>> Reference list is empty" 
    }
    
    #what BB's are close to the ref bead?
    set CLOSEBY [atomselect top "(serial $atomlist) and (pbwithin $upperBound of serial $ref) and (not serial $ref)"]
	set closeby [$CLOSEBY get serial]
	$CLOSEBY delete
    
	#what are the beads in the gro file?
    set closeG [puller $grolist $atomlist $closeby]
    set u2 [expr 1.0*$upperBound**2]
    
    if {[llength $closeby] != [llength $closeG]} { 
        error "Inconsistent number of atoms found. Wubaluba Dub Dub" 
    }
    
    foreach sec $closeby gro $closeG {
		set sref [atomselect top "serial $ref"]
		set ssec [atomselect top "serial $sec"]
		set p1 [list [$sref get x] [$sref get y] [$sref get z] ]
		set p2 [list [$ssec get x] [$ssec get y] [$ssec get z] ]
		$sref delete
		$ssec delete
		set d2 [expr 1.0*[vecdist $p1 $p2]**2]
		#puts "$d2, $u2"
		if {$d2<$u2} {
			if {$d2<[expr $lowerBound**2]} {
				continue
			}
            
            set d [expr 1.0*sqrt($d2)/10.0]
            set fscl [expr ${forceConstant}*[decayFunction $d $lowerBound $decayFactor $decayPower]]
            #puts $fscl
            if {[expr $fscl*$forceConstant > $minForce]} {
                set var1 [format %5d $refg ]
                if {[string is alpha $gro]} {
                    puts "$ref $refg"
                    puts "Not a number!"
                    return
                } else {
                    set var2 [format %5d $gro]
                }
                set var3 "      "
                set var4 6
                set var5 "   "
                set var6 [format %6.5f ${d}]
                if {[expr floor(${forceConstant}*[decayFunction $d $lowerBound $decayFactor $decayPower])] != ${forceConstant}} {
                puts $fout "${var1} ${var2}${var3}${var4}${var5}${var6} [expr 1.0*(${forceConstant}*[decayFunction $d $lowerBound $decayFactor $decayPower])]"
                } else {
                    puts $fout "${var1} ${var2}${var3}${var4}${var5}${var6} [expr 1.0*${forceConstant}]"
                }
            }
		}
    }
}



proc main {} {

    ;#set elast [get_elastic_name]
    source ~/lms464/github/JPC_Special/common/grace/assign_helices_2BG9_CG_lms2.tcl
    set lowerBound 4.6
    set upperBound 9.9999
    set decayFactor 0.0
    set decayPower 1.0
    set forceConstant 900.0
    set minForce 0.0
    
    set chans [atomselect top "name BB and not chain X"]
    set CHAINS [lsort -unique [$chans get chain]]
    puts $CHAINS
    $chans delete
    set nChains [NumChains]
    puts "$nChains"
	for {set i 0} {$i < $nChains} {incr i} {
        set chain [lindex $CHAINS $i]
        if {$chain == "X"} {
            continue
        }
        puts "\n########################################"
        puts "#Chain:       ${chain}"
        puts "########################################\n"
        set atlist [atomselect top "name BB and chain ${chain}"]
        set atomlist [$atlist get serial]
        $atlist delete
        set grolist [setGro $chain]
        set infile [molinfo top get name]
        set outfile [lindex [split $infile .] 0 ]
        set sys [string index $outfile 8]
        set wuba [open "./Harmonic_${chain}${sys}.itp" w]
        puts $wuba "\[ bonds ]"
        if { [llength $atomlist]!=[llength $grolist] } {
            error ">>> There is a mismatch between Gromacs' and VMD's BB beads count...\n>>>Exiting"
        }
        foreach ref $atomlist refg $grolist {
            rubberBands $ref $atomlist $refg $grolist $lowerBound $upperBound $decayFactor $decayPower $forceConstant $minForce $wuba
        }
        unset atomlist
        close $wuba
    }
}

main
exit
