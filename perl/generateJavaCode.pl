#!/usr/bin/perl -w

$dir = ".";
$dir = shift;

open(FIND, "find $dir -name \"*.class\" -print |") or 
    die "Cant call find: $!\n";
$home = `pwd`;
chomp($home);
while ($file = <FIND>) {
    chdir $home;
    chomp($file);
#    print "FILE: '$file'\n";
    $file =~ m|^(.*)/(.*)\.class$|;
    $dir = $1;
    $name = $2;
#    print "DIR: $dir, NAME: $name\n";
    chdir $dir or warn "Can not chdir to $dir. I am in \"", `pwd`, "\": $!";
#    print "IN: ", `pwd`;
    next if -e "$name.java";
#    print "Call jad -o -sjava $name.class\n";
    system("jad", "-lnc", "-o", "-sjava", "$name.class");
#    print "BACK: ", `pwd`;
}
