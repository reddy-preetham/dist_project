Implementation of Twins for DiemBFT v4 in DistAlgo

PLATFORM:


The software platforms that are used in testing the algorithm are:


OS: 
macOS 11.6 (Big Sur) 
Windows 10


Python Implementation:
CPython


Python Versions used to test:
Python 3.6.13
Python 3.7.0
Python 3.7.9


DistAlgo Version used for implementation:
1.1.0b15


Type of host:
Laptop


BUGS AND LIMITATIONS:
–- Depending on the system processing performance, the value of delta(highest time for executing one round) can change. Adjust the value of delta depending on the delta


MAIN FILES:
-- Config: <path_of_project_folder>/config/config.da
-- Client: <path_of_project_folder>/src/client.da
-- Validator(Replica): <path_of_project_folder>/src/validator.da
-- Play Ground: <path_of_project_folder>/src/playground.da
-- runDMBFT: <path_of_project_folder>/src/rundmbft.da
-- generator: <path_of_project_folder>/src/generator.py
-- config test: <path_of_project_folder>/src/config_test.py


CODE SIZE:

1. Generator : 252 
2. Executor : 
-- Play Ground: 145
-- runDMBFT: 93


2. Count was obtained using cloc command - cloc --force-lang="Python" *.da .




LANGUAGE FEATURE USAGE:
Generator : lists : 9, dictionaries : 6
Executor :  lists : 2, sets : 6, dictionaries : 2,  comprehensions :  receive handlers - 7


CONTRIBUTIONS:



Manikanta Sathwik Yeluri:  33%
Test Executor, fixing bugs 

Preetham Reddy Katta: 33%
Fixing bigs, test generator in diemBFT, syncup

Sai Bhavana Ambati: 33%
- Test Generator, property checking
