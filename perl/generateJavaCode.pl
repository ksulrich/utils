#!/usr/bin/perl -w

$dir = ".";
$dir = shift;

open(FIND, "find $dir -name \"*.class\" -print |") or 
    die "Cant call find: $!\n";
$home = `pwd`;
chomp($home);
while ($file = <FIND>) {
    chomp($file);
    print "FILE: '$file'\n";
    $file =~ m|^(.*)/(.*)\.class$|;
    $dir = $1;
    $name = $2;
#    print "DIR: $dir, NAME: $name\n";
    chdir $dir;
#    print "IN: ", `pwd`;
    print "Call jad -o -sjava $name.class\n";
    system("jad", "-o", "-sjava", "$name.class");
    chdir $home;
#    print "BACK: ", `pwd`;
}
