#!/bin/env bash

rm -f dec-to-mlinput.log
time lar -j 16 -n $1 -c dec-to-mlinput.fcl raw-digits-n107.root