#!/bin/bash

if [ "$1" == "-h" ]; then
  echo "Usage: ./script [-h] subnet filename repeat_minutes"
  exit 0
fi

function funky  {
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
while true
do 
    funky $1 $2
    sleep $((60*$3))
done
