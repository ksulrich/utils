#!/usr/bin/perl -w

$debug = 0;
$dir = ".";
$dir = shift;

open(FIND, "find $dir -name \"*.class\" -print |") or 
    die "Cant call find: $!\n";
$home = `pwd`;
chomp($home);
while ($file = <FIND>) {
    chdir $home;
    chomp($file);
    print "FILE: '$file'\n" if ($debug);
    if ($file =~ m|.*\$.*.class$|) {
	print "File is inner class, ignore\n" if ($debug);
	next;
    }
    $file =~ m|^(.*)/(.*)\.class$|;
    $dir = $1;
    $name = $2;
    print "DIR: $dir, NAME: $name\n" if ($debug);
    chdir $dir or warn "Can not chdir to $dir. I am in \"", `pwd`, "\": $!";
    print "IN: ", `pwd` if ($debug);

    # skip if java file exists
    next if -e "$name.java"; 
    print "jad", "-lnc", "-o", "-sjava", "$name.class", "\n" if ($debug);
    system("jad", "-lnc", "-o", "-sjava", "$name.class");
    print "BACK: ", `pwd` if ($debug);
}
