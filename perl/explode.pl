#!/usr/bin/perl

require "getopts.pl";
use Cwd;
use File::Basename;

my $silent = 0;

$destDir = "/tmp/xxx";
$opt_s = undef;
$opt_d = undef;

# Name of running program
($progname = $0) =~ s#.*/##;

&Getopts("sd") || usage($progname);

$file = shift @ARGV;
#$file = `cygpath -aw $file`;
#$file =~ s/\\/\\\\/g;

unless ($file =~ m|^/|) {
    # we have an relative path name
    $file = Cwd::cwd . "/" . $file;
    #
    # for windows and cygwin, we need to substitue the cygdrive path
    #
    $file =~ s|/cygdrive/([abcdefg])/|$1:/|g;
}
print "DEBUG: file=$file\n" if ($opt_d);

sub usage {
  my ($progname) = @_;

  printf STDERR "Usage: %s [-d][-s]<jar-file>\n", $progname;
  printf STDERR "       -d: Debug flag\n";
  printf STDERR "       -s: Silent flag\n";
  exit 1;
}

#system("rm -rf $destDir") == 0 or die "Cant remove $destDir: $!\n";
mkdir $destDir;

chdir($destDir);
print "Explode $file\n" if ($opt_d);
system("jar xf $file") == 0 or die "Can't explode $file: $!\n";
@jars = glob("*.jar");
push(@jars, glob("*.war"));

foreach (@jars) {
    chomp();
    ($file,$path,$ext) = fileparse($_, qr{\.[jw]ar});
    #($file, $ext) =  split('\.');
    print "Explode '$file$ext'\n" if ($opt_d);
    mkdir $file;
    chdir $file;
    system("jar xf ../$file$ext") == 0 or 
      die "Cant explode $file$ext: $!\n";
    chdir "..";
}
print "Files sucessfully created in $destDir\n" unless ($opt_s);

