lar -c gen_protoDune_muon_1GeV_mono.fcl -n 1 -o gen.root
lar -c protoDUNE_refactored_g4.fcl -n 1 gen.root -o g4.root
lar -c pgrapher/experiment/pdsp/Quickstart/wcls-sim-drift-deposplat.fcl -n 1 g4.root -o detsim.root
lar -n1 -c pgrapher/experiment/pdsp/wcls-nf-sp.fcl detsim.root -o reco.root
