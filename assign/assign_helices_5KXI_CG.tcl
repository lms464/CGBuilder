set selall [atomselect top {all}]
$selall set occupancy 0.0
$selall set user 0.0
set M1occ 1
set M2occ 2
set M3occ 3
set M4occ 4
set bindingdomainocc 0
set neckocc 0
set tmloopocc 2.5
set Vocc 5
set helix_code_list [list 1 2 3 4]

#values based on original mk_occupancy2BG9.tcl script
set M1_start_list [list 210 262 223 210 219]
set M1_end_list [list 239 236 254 240 246]
set M2_start_list [list 241 248 256 241 248]
set M2_end_list [list 264 277 286 271 280]
set M3_start_list [list 274 282 287 274 283]
set M3_end_list [list 302 307 315 302 309]
set M4_start_list [list 305 310 318 305 312]
#arbitrary large end
set M4_end_list  [list 700 700 700 700 700]

#gromacs seems to not have the same residue asymmetry?
set M1_start_list [list 211 210 210 211 210]
set M1_end_list [list 236 236 236 236 236]
set M2_start_list [list 239 239 239 239 239]
set M2_end_list [list 263 262 261 262 263]
set M3_start_list [list 269 268 268 269 268]
set M3_end_list [list 300 300 300 300 300]
set M4_start_list [list 330 330 330 330 330]
#arbitrary large end
set M4_end_list  [list 7000 7000 7000 7000 7000]


#all this crazy infrastructure assumes that there is residue asymmetry and should work in that case

set res_start_list_2D [list $M1_start_list $M2_start_list $M3_start_list $M4_start_list] 
set res_end_list_2D [list $M1_end_list $M2_end_list $M3_end_list $M4_end_list] 
#set protein_sel [atomselect top "name BB and resid 230"]
#set frag_list [$protein_sel get fragment]
# set frag_start_list [list 0 787 1561 2332  3120]
# set frag_end_list [list 786 1561 2332 3120 5600]

set frag_start_list [list 0 859 1696 2533 3392]
set frag_end_list [list 858 1695 2532 3391 4228]

set selall [atomselect top "all"]
$selall set chain X
set chainlist [list A B C D E]
for {set i 0} {$i < 5} {incr i} {
  set fragstart [lindex $frag_start_list $i]
  set fragend [lindex $frag_end_list $i]
  set chainsel [atomselect top "fragment $fragstart to $fragend"]
  $chainsel set chain [lindex $chainlist $i] 
}


foreach helix_code $helix_code_list res_start_list $res_start_list_2D res_end_list $res_end_list_2D {
  puts "Doing helix $helix_code"
  set subunit 0
  foreach frag_start $frag_start_list frag_end $frag_end_list res_start $res_start_list res_end $res_end_list {
    set tmp_sel [atomselect top "name BB SC1 SC2 SC3 SC4 and resid $res_start to $res_end"]
    set tmp_frags [$tmp_sel get fragment]
    set frags ""   
    foreach frag $tmp_frags   {
        if {($frag < $frag_end) && ($frag > $frag_start) } {
            lappend frags $frag
        }
    }
    set sel [atomselect top "same residue as (fragment $frags and resid $res_start to $res_end)"]
    puts "assigning fragment $frags and helix_code $helix_code and res_start $res_start and res_end $res_end"
    $sel set user $helix_code
    $sel set occupancy $helix_code
   # $sel set chain [lindex $chainlist $subunit]
    incr subunit
    #$sel delete
  }
}







#set res_start_list_2D [list $M1_start_list $M2_start_list $M3_start_list $M4_start_list] 
#set res_end_list_2D [list $M1_end_list $M2_end_list $M3_end_list $M4_end_list] 
#set protein_sel [atomselect top "name BB and resid 230"]
#set frag_list [$protein_sel get fragment]

#foreach helix_code $helix_code_list res_start_list $res_start_list_2D res_end_list $res_end_list_2D {
#  foreach fragment $frag_list res_start $res_start_list res_end $res_end_list {
#    set sel [atomselect top "fragment $fragment and name BB and resid > $res_start and resid < $res_end"]
#    puts "assigning fragment $fragment and helix_code $helix_code and res_start $res_start and res_end $res_end"
#    $sel set user $helix_code
#    $sel delete
#  }
#}


 
#stuff below doesn't do anything but should be added to code above at some point

################
#binding domain


set binding [atomselect top {chain A  and resid < 211}]
$binding set user $bindingdomainocc
$binding delete

set binding [atomselect top {chain B  and resid < 216}]
$binding set user $bindingdomainocc
$binding delete

set binding [atomselect top {chain C  and resid < 224}]
$binding set user $bindingdomainocc
$binding delete

set binding [atomselect top {chain D  and resid < 211}]
$binding set user $bindingdomainocc
$binding delete

set binding [atomselect top {chain E  and resid < 220}]
$binding set user $bindingdomainocc
$binding delete
################
#loops in binding domain neck



set neck [atomselect top {chain A   and ((resid < 212 and resid > 208) or (resid < 139 and resid > 127) or (resid < 48 and resid > 44) or (resid < 176) and (resid > 171))}]
$neck set user $neckocc
$neck delete

set neck [atomselect top {chain B   and ((resid < 220 and resid > 215) or (resid < 142 and resid > 126) or (resid < 49 and resid > 43) or (resid > 185 and resid < 188))}]
$neck set user $neckocc
$neck delete

set neck [atomselect top {chain C   and ((resid < 142 and resid > 129) or (resid < 51 and resid > 46) or (resid < 288 and resid > 285) or (resid < 226 and resid >223))}]
$neck set user $neckocc
$neck delete

set neck [atomselect top {chain D   and ((resid < 212 and resid > 208) or (resid < 139 and resid > 127) or (resid < 48 and resid > 44) or (resid < 176) and (resid > 171))}]
$neck set user $neckocc
$neck delete

set neck [atomselect top {chain E   and ((resid < 220 and resid > 215) or (resid < 140 and resid > 126) or (resid < 48 and resid > 44) or (resid < 184) and (resid > 178))}]
$neck set user $neckocc
$neck delete

##################
#loops in tm domain



set tmloop [atomselect top {chain A   and ((resid < 275 and resid > 270))}]
$tmloop set user $tmloopocc
$tmloop delete

set tmloop [atomselect top {chain B   and ((resid > 276 and resid < 283))}]
$tmloop set user $tmloopocc
$tmloop delete

set tmloop [atomselect top {chain C   and ((resid < 288 and resid > 285))}]
$tmloop set user $tmloopocc
$tmloop delete

set tmloop [atomselect top {chain D   and ((resid < 275 and resid > 270))}]
$tmloop set user $tmloopocc
$tmloop delete

set tmloop [atomselect top {chain E   and ((resid > 279 and resid < 284))}]
$tmloop set user $tmloopocc
$tmloop delete
