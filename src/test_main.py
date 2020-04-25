"""
Python Implementation of a Parser for a Subset of BASIC (ECMA 116 Standard)
Created by Nihad Kalathingal and Nick Green on 3/19/2020. Modified (03-20-2020)
    Kennesaw State University
    College of Computing and Software Engineering
    Department of Computer Science
    4308 Concepts of Programming Languages 03
    Module 3 – 2nd Deliverable
    Nihad Kalathingal (nkalathi@students.kennesaw.edu)
    Nick Green (ngreen@students.kennesaw.edu)
"""

from _parser import *

test_parser = parser()

test_parser.main('test/do_while.bas')