#!/usr/bin/perl -w

my $pmr = shift @ARGV;
my $path = $pmr;
my $pmr_dir = "/local/PMR";

if ($pmr =~ /^[\d]+[\d,A-Z]+$/) {
  @pmr = split(/ */, $pmr);
  $first = $pmr[0];
  $second = $pmr[1];
  $path = "/ecurep/pmr/$first/$second/$path"
}

print "PATH=$path\n";
chdir("$pmr_dir") or die("Cant cd to $pmr_dir");

my $cmd = "rsync -arvt klulrich\@ecurep.mainz.de.ibm.com:" . $path . " .";
print "CMD=$cmd\n";
system($cmd) == 0 or
  die "Cant get $path from ecurep server\n";

# cd to this directory
$dir =~ s|^.*/(.*)$|$1|;
chdir $dir;
#system("explorer.exe .");
system("emacs -fn 8x13 &");
#system("xterm &");
system("gnome-terminal &");

my $host = "ecurep.mainz.de.ibm.com";
#print "firefox https://$host/ae5/login/login.html#id=$pmr&path=$path &\n";
system("firefox https://$host/ae5/login/login.html#id=$pmr&path=$path &")
