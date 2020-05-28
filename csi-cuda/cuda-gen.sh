#!/usr/bin/env bash

time lar -j 1 -c cuda-gen.fcl -n 1 g4.root -o detsim.root
# time wire-cell -l stdout:info -c cuda-gen.jsonnet -V reality=data -V engine=Pgrapher
