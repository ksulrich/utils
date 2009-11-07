#!/usr/bin/perl -w

my @files = @ARGV;
my $path = pop @files;

$path =~ s|^(.*)/$|$1|;
print "FILES=@files\n";
print "PATH=$path\n";
my $cmd = "scp '@files' klulrich\@ecurep.mainz.de.ibm.com:" . $path . "/.";
#print "CMD=$cmd\n";
print "Execute \"$cmd\"\n(y/n) ... ";
$ans = <STDIN>;
print "ANS=$ans\n";
if ($ans =~ /[yY]/) {
#  print "EXEC\n";
  system($cmd) == 0 or
    die "Cant get $path from ecurep server\n";
}
