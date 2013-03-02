#!/usr/bin/perl

require "getopts.pl";

$debug = 1;

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
    print "DEBUG: grepbpm $class\n";
    open(GREP, "grepbpm $class |") or die "Cant call grepbpm $class: $!\n";
    while ($line = <GREP>) {
	chomp($line);
	print ("DEBUG: LINE$line\n") if ($debug);
	if ($line =~ m/^\s*(.*): (.*)$/) {
	    $plugin = $1;
	    $class = $2;
	    print "DEBUG: PLUGIN=$plugin, CLASS=$class\n" if ($debug);
	    if (usePlugin($plugin)) {
		unless (fileExists($class)) {
		    explode($plugin);
		    generateJavaCode();
		}
		callEmacs($class);
	    }
	}
    }
}
sub usePlugin {
    my ($plugin) = @_;
    print "Use '$plugin' ? (y/n) ... ";
    $answer = <>;
    if ($answer =~ m/^[yY].*/) {
	return 1;
    }
    return 0;
}

sub explode {
    my ($plugin) = @_;
    print "DEBUG(explode): explode.pl $plugin\n" if ($debug);
    system("explode.pl", $plugin)
}

sub generateJavaCode {
    print "DEBUG(generateJavaCode): generateJavaCode.pl $tmp\n" if ($debug);
    system("generateJavaCode.pl", $tmp);
}

sub callEmacs {
    my ($file) = @_;
    print "DEBUG(callEmacs): FILE=$file\n" if ($debug);
    $file =~ s/^(.*).class/\1.java/g;
    print "DEBUG(callEmacs): emacs $tmp/$file\n" if ($debug);
    system("emacs $tmp/$file &");
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
