#!/bin/env bash

rm -f fgsp.log
time lar -j 1 -n 1 -c fgsp.fcl raw-digits-n107.root
