#!/bin/env bash

rm -f dec-to-dnnsp.log
time lar -j 1 -n $1 -c dec-to-dnnsp.fcl raw-digits-n107.root