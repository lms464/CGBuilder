# CGBuilder

OHHHHHH BOY. First, while lots of ''features'' that really should be simplified (looking at you Liam).

The bulk of the scripts can be found in CGBuilder_Main. The assign directory has 4 pLGIC helices assignment scripts for CG systems. BuildMutiProt is a set of scripts to make pdb files with multiple proteins.

Please consider the following. MOST of these scripts were built durring the summer between the end of my master's and start of my PhD and should be converted to bash *and* simplified! If anyone is interetsed in a bit of a side project let me know!

Here's the general way to run:

- create a concentration file (I call them con.txt) see the pun :D
- call sh build.sh < con.txt > < file name  > < optional protein >
    - While CGBuilder.py can mass produce systems on its own, its all in one file
    - Inside build.sh it has all the commands to call the CGBuilder.py script
- CGBuilder.py to determine how to run call python CGBuilder.py -h 
- Harominic Restraints are going to be a bit of a pain. I've built this tool to really only work with pLGICs, and it's dumb, it cannot distinguish between pLGICs. ie you have to change the assing script manually..
