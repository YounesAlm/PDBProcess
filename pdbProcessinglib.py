#!/usr/bin/python3
"""
MIT License

Copyright (c) 2020 Younes Bouchiba

contact : bouchiba@insa-toulouse.fr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from os.path import isfile
from pprint import pprint
from statistics import mean, stdev
import argparse

BbAtoms=['CA','C','N','O']

class pdb(object) :
    def __init__(self, pdbfile = None):
        self.dict = {}
        if pdbfile.endswith('.pdb'):
            self.load(pdbfile)
        else:
            print('Error : You must give a pdb file, you dumbass')
            exit(1)
    def load(self, pdbfile):
        with open( pdbfile ) as f:
            content = f.read()
            lines= content.split('\n')
            for l in lines:
                words = l.split()
                if len(words)>1 and words[0]=='ATOM' and words[3]!='WAT' and words[3]!='CL' and words[3]!='NA':
                    if str.isdigit(words[4]): #sometimes the chain identifier is lacking which can confuse the pdb parse
                        resid=int(words[4])
                        resname=words[3]
                        
                        atomid=int(words[1])
                        atomname=words[2]
                        atom_x=float(words[5])
                        atom_y=float(words[6])
                        atom_z=float(words[7])
                        bfact=float(words[9])
                        if resid not in self.dict:
                            self.dict[resid]={'resname':resname, 'atoms':{} }
                            self.dict[resid]['atoms'][atomid]={ 'name': atomname,'x':atom_x , 'y':atom_y, 'z':atom_z , 'bfact':bfact}
                        else:
                            self.dict[resid]['atoms'][atomid]={ 'name': atomname,'x':atom_x , 'y':atom_y, 'z':atom_z , 'bfact':bfact}
                    else: #caution, this condition is simplifying the situation in whether the chain name is here or not, it might get more complicated depending on the pdb formating
                        resid=int(words[5])
                        resname=words[3]
                        atomid=int(words[1])
                        atomname=words[2]
                        atom_x=float(words[6])
                        atom_y=float(words[7])
                        atom_z=float(words[8])
                        bfact=float(words[10])
                        if resid not in self.dict:
                            self.dict[resid]={'resname':resname, 'atoms':{} }
                            self.dict[resid]['atoms'][atomid]={ 'name': atomname,'x':atom_x , 'y':atom_y, 'z':atom_z , 'bfact':bfact}
                        else:
                            self.dict[resid]['atoms'][atomid]={ 'name': atomname,'x':atom_x , 'y':atom_y, 'z':atom_z , 'bfact':bfact}
    def printDict(self):
        pprint(self.dict)
#        for u in self.dict:
#            for v in self.dict[u]['atoms']:
#                print(self.dict[u]['atoms'][v]['name'])
    def computeBfact(self):
        for resid in self.dict:
            self.dict[resid]['BfactBb']={'lst':[],'mean':0,'sd':0}
            self.dict[resid]['BfactHeavy']={'lst':[],'mean':0,'sd':0}
            for at in self.dict[resid]['atoms']:
                if self.dict[resid]['atoms'][at]['name'] in BbAtoms:
                    self.dict[resid]['BfactBb']['lst'].append(float(self.dict[resid]['atoms'][at]['bfact']))
                self.dict[resid]['BfactHeavy']['lst'].append(float(self.dict[resid]['atoms'][at]['bfact']))
            self.dict[resid]['BfactBb']['mean']=mean(self.dict[resid]['BfactBb']['lst'])
            self.dict[resid]['BfactBb']['sd']=stdev(self.dict[resid]['BfactBb']['lst'])
            self.dict[resid]['BfactHeavy']['mean']=mean(self.dict[resid]['BfactHeavy']['lst'])
            self.dict[resid]['BfactHeavy']['sd']=stdev(self.dict[resid]['BfactHeavy']['lst'])
    def getBfacts(self):
        print('ResId,ResName,BBmean,BBsd,Heavymean,Heavysd')
        for resid in self.dict:
            print(resid,self.dict[resid]['resname'],self.dict[resid]['BfactBb']['mean'],self.dict[resid]['BfactBb']['sd'],self.dict[resid]['BfactHeavy']['mean'],self.dict[resid]['BfactHeavy']['sd'],sep=',')
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search contacts between all residues in a protein given in pdb format')
    parser.add_argument('--pdb', required=True, help='PDB file')
    param = parser.parse_args()
    currentpdb=pdb(param.pdb)
    currentpdb.computeBfact()
    #currentpdb.getBfacts()
    currentpdb.printDict()

