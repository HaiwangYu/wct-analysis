#!/usr/bin/env python

import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def get_wave(data, key, ch, tick_min, tick_max):
  frame = np.array(data[key])
  wave = frame[tick_min:tick_max, ch]
  return wave

def comp(ch, tmin, tmax):
  apa   = 0
  tag   = 'ductor'
  key   = '/0/frame_%s%d'%(tag,apa)
  data  = h5py.File('g4-tru-%d.h5'%apa, 'r')

  w0 = get_wave(data, key, ch, tmin, tmax)

  # g4 reco
  apa   = 0
  tag   = 'gauss'
  data  = h5py.File('g4-rec-%d.h5'%apa, 'r')
  key   = '/0/frame_%s%d'%(tag,apa)

  w1 = get_wave(data, key, ch, tmin, tmax)


  plt.figure()

  plt.plot(w0,'-o', label='truth')
  plt.plot(w1,'-o', label='reco')
  plt.legend(loc='best',fontsize=15)
  plt.grid()
  plt.show()
  
  #print('mean = %f' % np.mean(wave))
  #print('std. = %f' % np.std(wave))


if __name__ == '__main__':
  for ch in range(0, 100, 10):
    comp(ch, 0, 1000)
