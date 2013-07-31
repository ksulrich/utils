#!/usr/bin/perl -w

#
# This setting needs to be adapted
#
my $BASE_DIR = "/opt/ibm/BPM/v8.0.1";

#
# this should not be touched
#
open(FD, "find $BASE_DIR -name \"*.jar\" -a -type f |") 
    or die "Can run find on $BASE_DIR: $!\n";

while (<FD>) {
    chomp();
    print "__ZIP__: $_\n";
    system("jar tf \"$_\"") == 0 or warn "Cant exec jar: $!\n";
}
close(FD);
