#!/usr/bin/perl -w

my $path = shift @ARGV;

my $pmr_dir = "/PMR";

if ($path =~ /^[\d]+[\d,A-Z]+$/) {
  @path = split(/ */, $path);
  $first = $path[0];
  $second = $path[1];
  $path = "/ecurep/pmr/$first/$second/$path"
}

print "PATH=$path\n";
chdir("$pmr_dir") or die("Cant cd to $pmr_dir");

my $cmd = "rsync -arvt klulrich\@ecurep.mainz.de.ibm.com:" . $path . " .";
print "CMD=$cmd\n";
system($cmd) == 0 or
  die "Cant get $path from ecurep server\n";

# cd to this directory
$path =~ s|^.*/(.*)$|$1|;
chdir $path;
system("explorer.exe .");
exec "/bin/bash";
