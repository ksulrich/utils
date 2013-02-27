#!/usr/bin/perl 

while (<>) {
    if (m/generatorVersion="([\d\.]+)"/) {
	print "$1\n";
    }
}
