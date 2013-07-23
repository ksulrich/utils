#!/usr/bin/perl

require "getopts.pl";

$debug = 0;

$tmp = "/tmp/xxx";

# Name of running program
($progname = $0) =~ s#.*/##;

&Getopts("d") || usage($progname);

my $class = shift @ARGV;
usage() unless (defined($class));

print "DEBUG: grepbpm $class\n" if ($debug);
$class = norm_class($class);
if (fileExists("$class.class")) {
    callEmacs("$class.java");
} else {
    print "DEBUG: grepbpm $class\n" if ($debug);
    open(GREP, "grepbpm $class |") or die "Cant call grepbpm $class: $!\n";
    my @plugins = undef;
    while ($line = <GREP>) {
	next if ($line =~ m/^\s*$/);
	chomp($line);
	print ("DEBUG: LINE$line\n") if ($debug);
	if ($line =~ m/^\s*(.*): (.*)$/) {
	    $plugin = $1;
	    $class = $2;
	    push(@plugins, $plugin);
	    print "DEBUG: PLUGIN=$plugin, CLASS=$class\n" if ($debug);
	}
    }
    my $len = scalar(@plugins);
    if ($len < 2) {
	print "Code not found\n";
	exit(0);
    } 
    if ($len == 2) {
	$plugin = @plugins[1];
	print "DEBUG: len==2: Use $plugin\n" if ($debug);
    } else {
	my $i = 0;
	foreach $plugin (@plugins) {
	    print "$i: $plugin\n";
	    $i++;
	}
	print "What plugin? ... ";
	$ans = <>;
	$ans =~ s/(\d+).*/\1/;
	print "DEBUG: Use $ans\n" if ($debug);
	$plugin = $plugins[$ans];
    }
    explode($plugin);
    generateJavaCode();
    callEmacs($class);
}

sub explode {
    my ($plugin) = @_;
    $plugin =~ s/ /\\ /g;
    print "DEBUG(explode): cd /tmp/xxx/src; jar xf $plugin\n" if ($debug);
    system("mkdir -p /tmp/xxx/src; cd /tmp/xxx/src; jar xf $plugin");
}

sub generateJavaCode {
    print "DEBUG(generateJavaCode): generateJavaCode.pl $tmp\n" if ($debug);
    system("generateJavaCode.pl $tmp 2>/dev/null");
}

sub callEmacs {
    my ($file) = @_;
    print "DEBUG(callEmacs): FILE=$file\n" if ($debug);
    $file =~ s/^(.*).class/\1.java/g;
    print "DEBUG(callEmacs): emacs $tmp/src/$file\n" if ($debug);
    system("emacs $tmp/src/$file &");
}

sub norm_class {
    my ($file) = @_;
    print "DEBUG(norm_class): FILE=$file\n" if ($debug);
    $file =~ s/^(.*).class/\1/g;
    $file =~ s|\.|/|g;
    print "DEBUG(norm_class): Return $file\n" if ($debug);
    return $file;
}

sub fileExists {
    my ($file) = @_;
    print "DEBUG(fileExists): Exists ? $tmp/$file\n" if ($debug);
    return -e "$tmp/$file";
}

sub usage {
    my ($progname) = @_;

    printf STDERR "Usage: %s [-d] <class_name>\n", $progname;
    printf STDERR "       -d: Debug flag\n";
    exit 1;
}
