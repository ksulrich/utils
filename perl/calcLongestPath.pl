#!/usr/bin/perl 

my $max =0;
my $file = "UNKNOWN";

# Name of running program
($progname = $0) =~ s#.*/##;

if ($#ARGV != 0) {
  print "Usage: $progname <directory to check>\n";
  exit(1);
}

open(fd, "find . -print |") or 
  die "Cant call find: $!\n";

while (<fd>) {
  chomp();
  s/^\.\///g;
  s/^\.\\//g;
  my $len = length();
  if ($len > $max) {
    $max = $len;
    $file = $_;
  }
}

print "Longest file: $file\n Containes: $max characters\n";

