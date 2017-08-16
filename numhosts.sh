#!/bin/bash
nh="$( nmap -sn  $1 | grep -c 'up' )"
nh=$(($nh -1))
echo -n `date` >> "$2.csv"
echo -n "," >> "$2.csv"
echo -n $2 >> "$2.csv"
echo -n "," >> "$2.csv"
echo -n $1 >> "$2.csv"
echo -n "," >> "$2.csv"
echo $nh >> "$2.csv"

