#!/usr/bin/env bash

# time wire-cell -V reality=data -V engine=TbbFlow -l stdout -L debug -L hio:trace -c test_hdf5_framesource.jsonnet
# time wire-cell -V reality=data -V engine=Pgrapher -l stdout -L debug -L hio:trace -c test_hdf5_framesource.jsonnet 

time wire-cell \
-V reality=data \
-V engine=TbbFlow \
-l stdout \
-L info \
-c test_hdf5_framesource.jsonnet 
