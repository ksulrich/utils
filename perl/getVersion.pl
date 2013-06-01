#!/usr/bin/perl 
# 
# Searches for generatorVersion= in .mm file
#

while (<>) {
    if (m/generatorVersion="([\d\.]+)"/) {
	print "$1\n";
    }
}
