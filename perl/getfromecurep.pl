#!/usr/bin/perl -w

require "getopts.pl";

$opt_f = undef;
my $progname;

# Name of running program
($progname = $0) =~ s#.*/##;
&Getopts("f") || usage($progname);
if ($#ARGV != 0) {
    usage($progname);
}
my $pmr = shift @ARGV;
print "OPT_F: |$opt_f|, PMR=|$pmr|\n";


my $path = $pmr;
my $pmr_dir = "/local/PMR";
#my $pmr_dir = "/data/tmp/_KU";

if ($pmr =~ /^[\d]+[\d,A-Z]+$/) {
  @pmr = split(/ */, $pmr);
  $first = $pmr[0];
  $second = $pmr[1];
  $path = "/ecurep/pmr/$first/$second/$path"
}

unless ($opt_f) {
    print "PATH=$path\n";
    chdir("$pmr_dir") or die("Cant cd to $pmr_dir");

    my $cmd = "rsync --delete -arvt klulrich\@ecurep.mainz.de.ibm.com:" . $path . " .";
    print "CMD=$cmd\n";
    system($cmd) == 0 or
	warn "Cant get $path from ecurep server\n";

    print "XXX: $pmr_dir/$pmr\n";
    $dir = "$pmr_dir/$pmr";
    system("emacs -fn 8x13 $dir &");
    system("(cd $dir; gnome-terminal) &");
}

my $host = "ecurep.mainz.de.ibm.com";
#print "firefox https://$host/ae5/login/#id=$pmr &\n";
#system("firefox https://$host/ae5/login/#id=$pmr &");
print "google-chrome https://$host/ae5/login/#id=$pmr &\n";
system("google-chrome https://$host/ae5/login/#id=$pmr &");

sub usage {
  my ($progname) = @_;

  printf STDERR "Usage: %s [-f] <PMR>\n", $progname;
  printf STDERR "       -f: Do not download data from ecurep\n";
  exit 1;
}
