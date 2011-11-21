#!/usr/bin/perl 

require "getopts.pl";

my $debug = undef;
my $max =0;
my $file = "UNKNOWN";
$opt_d = undef;

# Name of running program
($progname = $0) =~ s#.*/##;

&Getopts("d") || usage($progname);

if ($#ARGV != 0) {
    usage($progname);
}

open(fd, "find . -print |") or 
  die "Cant call find: $!\n";

while (<fd>) {
  chomp();
  s/^\.\///g;
  s/^\.\\//g;
  my $len = length();
  if ($opt_d) { print "$len: $_\n"; }
  if ($len > $max) {
    $max = $len;
    $file = $_;
  }
}

print "Longest file: $file\n Containes: $max characters\n";

sub usage {
  my ($progname) = @_;

  printf STDERR "Usage: %s [-d] <directory>\n", $progname;
  printf STDERR "       -d: Debug flag\n";
  exit 1;
}
