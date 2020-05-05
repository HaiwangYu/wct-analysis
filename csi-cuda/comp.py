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

def comp(event, ch, tmin, tmax):
  print('ch: ', ch, ': ', tmin, ', ', tmax)

  apa   = 0
  tag   = 'orig'

  # ref
  key   = '/%d/frame_%s%d'%(event+100,tag,apa)
  data  = h5py.File('ref.h5', 'r')
  frame = np.array(data[key])
  # frame = np.transpose(frame, axes=[1, 0])
  # frame = frame[:,800:1600]
  w0 = get_wave(frame, key, ch, tmin, tmax)

  # test
  key   = '/%d/frame_%s%d'%(event,tag,apa)
  data  = h5py.File('cuda.h5', 'r')
  frame = np.array(data[key])
  # frame = np.transpose(frame, axes=[1, 0])
  # frame = frame[:,800:1600]
  w1 = get_wave(frame, key, ch, tmin, tmax)

  plt.figure()
  a = plt.gca()
  a.set_title('ch: '+str(ch))

  plt.plot(w0,'-o', label='ref')
  plt.plot(w1,'-',  label='cuda')
  plt.legend(loc='best',fontsize=15)
  plt.grid()
  plt.show()
  
  #print('mean = %f' % np.mean(wave))
  #print('std. = %f' % np.std(wave))


if __name__ == '__main__':
  for ch in range(2142, 2560, 10):
    comp(0, ch, 0, 6000)
