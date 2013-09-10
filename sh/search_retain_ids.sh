#!/bin/sh

# Needs to run on a CCWin installation server
# 
# Creates a list of "<retain_id>" "<user>" 

find /c/CCWin -name "owner.dat" -exec grep -v // {} \; | col -b | grep -v ^\# | sort | grep -v \"\" | grep -v "      " | grep -v -e '^[       ]*$'
