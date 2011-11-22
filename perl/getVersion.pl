#!/usr/bin/perl

while (<>) {
    if (m/generatorVersion="(.*?)"/) {
        print $1;
    }
}
