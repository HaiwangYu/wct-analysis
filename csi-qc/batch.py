#!/usr/bin/env python

import os
import sys

param = {
  'mu+': [-13, 0.56],
  'pi+': [211, 0.56],
  'p+': [2212, 1.3],
  'K+': [321, 0.98],
  'e-': [11, 0.47],
  'gamma': [22, 0.47],
  'pi0': [111, 0.56],
}

def single(particle, nevents):
  print('single: {} {}'.format(particle, nevents))

  cwd = os.getcwd()
  subdir = '{}/sample/{}'.format(cwd,particle)
  os.chdir(cwd)
  os.system('mkdir -p {}'.format(subdir))
  os.system('cp *.fcl *.jsonnet {}'.format(subdir))
  os.chdir('{}'.format(subdir))

  pid = param[particle][0]
  mom = param[particle][1]
  print('{} {}'.format(pid,mom))
  os.system('sed -i \'s/VAR_PID/{}/\' gen_protoDune_single.fcl'.format(pid))
  os.system('sed -i \'s/VAR_MOM/{}/\' gen_protoDune_single.fcl'.format(mom))

  os.system('lar -c gen_protoDune_single.fcl -n {} -o gen.root'.format(nevents))
  os.system('lar -c protoDUNE_refactored_g4.fcl -n {} gen.root -o g4.root'.format(nevents))
  os.system('lar -j 1 -c sim-truth-reco.fcl -n {} g4.root -o sp.root'.format(nevents))

  os.chdir(cwd)

def save(particle):
  cwd = os.getcwd()
  subdir = '{}/sample/{}'.format(cwd,particle)
  os.chdir(cwd)
  os.system('cp *.py {}'.format(subdir))
  os.chdir('{}'.format(subdir))
  os.system('./hioplot.py')
  os.system('./hioexport.py')
  os.system('rm *.fcl *.jsonnet *.py *.root *.h5')
  os.chdir(cwd)

def main():
  print('main:')
  nevents = sys.argv[1]

  for particle in param:
    if(sys.version_info[0]==2):
      single(particle, nevents)
    else:
      save(particle)

if __name__ == '__main__':
  print('batch:')
  main()
