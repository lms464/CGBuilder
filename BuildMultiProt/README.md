# Build Multiple Protein pdb's

LMS: 
It's been some time since I've run these. Initially these were built in collaberation with Kristen and before I was more comfortable in bash. I have also included a sample set of nAChR proteins.

This script places proteins of a specific species in a single pdb file around a circle. Please note I had issues with more than 5 proteins. I think I do not properly enlarge the second protein ring.

JWS: 
I fixed the problem with expanding beyond 5 proteins. There is now a max of 62 subunits or 12 pentamerics in one system. Per conversation with GB, expanding rings of protiens is no longer priority. I have made a grid feature that allows the user to select how wide they want the box to be and proteins will be evenly spaced accordingly.



To run:

python BuildMulti_Pro.py < protein.pdb  > < number of proteins > < "grid" or "circle" > < box size in nm >
