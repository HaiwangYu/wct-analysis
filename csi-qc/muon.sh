lar -c gen_protoDune_single.fcl -n $1 -o gen.root
lar -c protoDUNE_refactored_g4.fcl -n $1 gen.root -o g4.root
lar -j 1 -c sim-truth-reco.fcl -n $1 g4.root -o sp.root
