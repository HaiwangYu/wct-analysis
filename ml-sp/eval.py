#!/usr/bin/env python

import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def criteria(a):
  if a > 0:
    return True
  else:
    return False

def eval(f0m, f1m):
  both = np.logical_and(f0m, f1m)
  inefficiency = np.logical_xor(f0m, both)
  impurity = np.logical_xor(f1m, both)
  ntruth = np.count_nonzero(f0m)
  nreco = np.count_nonzero(f1m)
  print("inefficiency: ", np.count_nonzero(inefficiency), "/", ntruth, " = ", np.count_nonzero(inefficiency)/ntruth*100, "%")
  print("impurity: ", np.count_nonzero(impurity), "/", nreco, " = ", np.count_nonzero(impurity)/nreco*100, "%")

if __name__ == '__main__':

  event = 95

  # truth
  apa   = 0
  tag   = 'ductor'
  data  = h5py.File('g4-tru-%d.h5'%apa, 'r')
  key   = '/%d/frame_%s%d'%(event,tag,apa)
  f0    = np.array(data[key])

  # reco
  apa   = 0
  tag   = 'gauss'
  data  = h5py.File('g4-rec-%d.h5'%apa, 'r')
  key   = '/%d/frame_%s%d'%(event,tag,apa)
  f1    = np.array(data[key])

  # f0m = np.vectorize(criteria)(f0)
  # f1m = np.vectorize(criteria)(f1)
  
  f0m = f0
  f1m = f1

  truth_th = 0

  f0m[f0m<=truth_th] = 0
  f0m[f0m>truth_th] = 1
  # f1m[f1m<=0] = 0
  # f1m[f1m>0] = 1


  eval(f0m, f1m)


  plt.imshow(np.ma.masked_where(f1m<=0,f1m), cmap='hsv', interpolation="none"
  , extent = [0 , 2560, 0 , 600]
  , origin='lower'
  # , aspect='auto'
  )
  plt.colorbar()

  # plt.imshow(f0m, cmap='jet', interpolation="none"
  plt.imshow(np.ma.masked_where(f0m<=0,f0m), cmap='cool', interpolation="none"
  , extent = [0 , 2560, 0 , 600]
  , origin='lower'
  # , aspect='auto'
  , alpha=0.3
  )
  plt.xlim([0, 800])
  # plt.ylim([3000, 4000])
  plt.grid()
  plt.show()
