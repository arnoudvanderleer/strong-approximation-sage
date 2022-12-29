#!/bin/bash
# Converts a sage file to a python file to use as a library

Filename="$(cut -d'.' -f1 <<< $1)"

jupyter nbconvert --to script $Filename.ipynb

mv $Filename.py $Filename.sage
sage -preparse $Filename.sage

mv $Filename.sage.py $Filename.py
rm $Filename.sage