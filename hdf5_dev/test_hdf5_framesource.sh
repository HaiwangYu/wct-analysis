#!/usr/bin/env bash

# time wire-cell -V reality=data -V engine=TbbFlow -l stdout -L info -L hio:trace -c test_hdf5_framesource.jsonnet 

time wire-cell \
 -V reality=data \
\ # -V engine=Pgrapher \
-V engine=TbbFlow \
 -l stdout \
 -L info \
 -L hio:trace \
 -c test_hdf5_framesource.jsonnet 
