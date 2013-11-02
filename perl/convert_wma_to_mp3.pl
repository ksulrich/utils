#!/usr/bin/perl -w
#
# Convert wma file to mp3 file
#
# Run:
# find . -name "*.wma" > files
# convert_wma_to_mp3.pl files

use strict;

while (<>) {
    my $file = $_;
    chomp($file);
    print "File: $file\n";
    next if ($file !~ /\.wma$/i);
    my $base = $file; 
    $base =~ s/\.wma$//i;
    #print "XXX: mplayer -ao pcm:file=\"$base.wav\" \"$file\"\n";
    system "mplayer -ao pcm:file=\"$base.wav\" \"$file\""; 
    #print "XXX: lame -h \"$base.wav\" \"$base.mp3\"\n";
    system "lame -h \"$base.wav\" \"$base.mp3\"";
    unlink("$base.wav");
    print "$base.wma converted to mp3.\n";
}
