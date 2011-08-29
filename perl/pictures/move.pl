#!/usr/bin/perl -w
# 
# $Id: move.pl,v 1.1 2004/01/13 09:13:34 klaus Exp $
#
# Erzeugt aus einem Tar Archive eine Struktur 
# <jahr>/<monat>_<tag>_<timestamp>.jpg
#
# Z.G. -rwxrw-r-- klaus/users  978402 2004-01-03 17:35:08 DSCI0040.JPG
# wird zu 2004/01_03_17:35:08.jpg
#
# Author: Klaus Ulrich

usage() if ($#ARGV < 0);

foreach $tar_file (@ARGV) {
    print "FILE: $tar_file\n";

    explode($tar_file);

    open(IN, "tar tfv $tar_file | ") or die "Cant open $tar_file: $!\n";
    while (<IN>) {
        my ($mode, $user, $size, $day_stamp, $time, $file) = split();
        #print "File: $file, Day_stamp=$day_stamp, Time=$time\n";
        my ($year, $month, $day) = split(/-/, $day_stamp);
        #print "File: $file, Year=$year, Month=$month, Day=$day\n";
        print "mkdir $year\n";
        mkdir($year);
        $time =~ s/:/_/g;
        my $ext = $file;
        $ext =~ s/^.*\.(.*)$/$1/g;
        #print "EXT=", lc($ext), "\n";
        my $dest = $year . "/" . $month . "-" . $day . "-" . $time . 
            "." . lc($ext);
        print "mv \"$file\" \"$dest\"\n";
        rename($file, $dest);
    }
    close(IN);
}

sub explode {
    my $archive = shift;

    system("tar xf $archive") == 0 
        or die "system tar xfv $archive failed: $?\n";
}

sub usage {
    die "Usage: $0 <tar_archive>\n";
}
