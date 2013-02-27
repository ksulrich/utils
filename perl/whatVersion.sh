#!/bin/sh

PN=`basename $0`			# program name
VER='0.1 (beta)'

Usage () {
    echo "$PN - Display MM generator version, $VER (ku '11)
usage: $PN [MM.ear]" >&2

    exit 1
}

Msg () {
    for i
    do echo "$PN: $i" >&2
    done
}

Fatal () { Msg "$@"; exit 1; }

GetVersion () {
    # Determine base of the number
    for i
    do
    explode.pl -s "$i"
    if [ -e /tmp/xxx/META-INF/monResources.xml ]
        then
        echo -n "$i was generated with " 
        getVersion.pl /tmp/xxx/META-INF/monResources.xml
#        echo ""
    fi
    done
}


while [ $# -gt 0 ]
do
    case "$1" in
	--)	shift; break 2;;
	-h)	Usage;;
	-*)	Usage;;
	*)	break 2;;		# first MM.ear
    esac
    shift
done

if [ $# -gt 0 ]
then
    GetVersion "$@"
else					# read from stdin
    while read line
    do
	GetVersion $line
    done
fi

