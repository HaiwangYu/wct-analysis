#!/bin/env bash

rm -f dec-to-h5.log
time lar -j 1 -n $1 -c dec-to-h5.fcl raw-digits-n107.root