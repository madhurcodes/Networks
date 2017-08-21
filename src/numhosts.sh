#!/bin/bash

if [ "$1" == "-h" ]; then
  echo "Usage: ./script [-h] subnet filename repeat_minutes [somestuff]"
  exit 0
fi

funk () {
nh="$( nmap -sn  $1 | grep -c 'up' )"
nh=$(($nh -1))
echo -n `date` >> "$2.csv"
echo -n "," >> "$2.csv"
echo -n $2 >> "$2.csv"
echo -n "," >> "$2.csv"
echo -n $1 >> "$2.csv"
echo -n "," >> "$2.csv"
echo $nh >> "$2.csv"
}
watch -n $(60*$3) funk
