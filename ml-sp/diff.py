#!/usr/bin/env python

import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def get_wave(frame, key, ch, tick_min, tick_max):
  print(frame.shape)
  # plt.imshow(frame, origin='lower', aspect='auto')
  # plt.show()
  wave = frame[tick_min:tick_max, ch]
  return wave

def diff(event):

  apa   = 3
  tag   = 'orig'
  tag   = 'dnn_sp'
  tag   = 'dlcharge'

  # ref
  key   = '/%d/frame_%s%d'%(event,tag,apa)
  data  = h5py.File('6apa-service-gpu/data-%d.h5'%(apa), 'r')
  data  = h5py.File('6apa-service-gpu/tsmodel-eval.h5', 'r')
  frame = np.array(data[key])
  f0 = np.transpose(frame, axes=[1, 0])

  # test
  data  = h5py.File('6apa-service-100loop-gpu/data-%d.h5'%(apa), 'r')
  data  = h5py.File('6apa-service-100loop-gpu/tsmodel-eval.h5', 'r')
  key   = '/%d/frame_%s%d'%(event,tag,apa)
  frame = np.array(data[key])
  f1 = np.transpose(frame, axes=[1, 0])

  plt.figure()
  a = plt.gca()
  a.set_title('event: '+str(event))

  plt.imshow(f1-f0, cmap="bwr", interpolation="none"
  # , extent = [0 , 2560, 0 , 6000]
  , origin='lower'
  , aspect='auto')
  plt.clim(-1,1)
  plt.grid()
  plt.show()
  
  #print('mean = %f' % np.mean(wave))
  #print('std. = %f' % np.std(wave))


if __name__ == '__main__':
  diff(0)
