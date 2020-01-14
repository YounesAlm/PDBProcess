# PDBProcess

##Introduction

This is a small project which aims at simplify PDB files processing such as Bfactor computations.
For now on it is very basic and works by the sole argument --pdb who must have the .pdb extension.

###Usage
<pre><code>
chmod +x pdbProcessinglib.py 
./pdbProcessinglib.py --pdb [file.pdb]
</code></pre>

I would like to add features and pass by arguments the kind of action the user would like to perform

##Ideas for the future

* Implement a parsing command who translates AMBER nomenclature (CYX,HID...) to ROSETTA nomenclature (CYS,HIS...).
