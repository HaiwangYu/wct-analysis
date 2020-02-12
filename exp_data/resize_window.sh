#!/bin/bash

# resize the last window
# usage: ./resize_window.sh
 
str=`wmctrl -l | tail -n1`

IFS=' ' # space is set as delimiter
read -ra ADDR <<< "$str" # str is read into an array as tokens separated by IFS
wid=${ADDR[0]}
wmctrl -i -r ${wid} -e 0,0,0,1000,800
