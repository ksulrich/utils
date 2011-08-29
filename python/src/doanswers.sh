#!/bin/sh

echo -n "> "
while :
do
    read line
    python answers.py ~/Wissen/312-50.txt "$line" | less
    clear
    echo -n "> "
done
