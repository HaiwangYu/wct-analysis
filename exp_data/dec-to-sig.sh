#!/bin/env bash

rm -f wcls-dec-to-sig.log
time lar -j 16 -n 1 -c dec-to-sig.fcl raw-digits-n10.root
