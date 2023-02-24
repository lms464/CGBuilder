set PATH "./MultiPro/*.pdb"
set files [lsort [glob ${PATH}]]  ;#finds all pdbs in current directory
set i 0
file mkdir new_proteins
foreach f $files {
    mol load pdb $f
    set chainstr "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    set chainchar [string index $chainstr $i]
    set chainlist [list A B C D E]
    for {set j 0} {$j < 5} {incr j} {
            set chain [atomselect top "chain [lindex $chainlist $j]"] ;# set atomselect of chain $j here
            $chain set chain [string index $chainstr $i]
            $chain delete
            incr i
    }
    set sel [atomselect top "all"]
    puts $f
    set k [expr {$i + 100} ]
    $sel writepdb "new_proteins/$k.pdb"
    $sel delete
    mol delete top
}
 
exit

