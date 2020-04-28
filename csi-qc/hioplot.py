#!/usr/bin/env python

import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


def get_wave(data, key, ch, tick_min, tick_max):
  frame = np.array(data[key])
  wave = frame[tick_min:tick_max, ch]
  return wave

def show_frame(data, event, apa, tag) :
  key = '/%d/frame_%s%d'%(event,tag,apa)
  f = data.get(key)
  if f is None:
    print('f is None')
    return
  frame = np.array(f)
  print(frame.shape)
  frame_ma = np.ma.array(frame)

  # plt.gca().set_title(tag)

  # plt.hist(frame.reshape(-1), bins=100, range=(-2000,2000))

  plt.imshow(frame_ma, cmap="jet", interpolation="none"
  # , extent = [0 , 2560, 0 , 6000]
  , origin='lower'
  # , aspect='auto'
  , aspect=0.8/4.7
  # , aspect=0.1
  )
  # plt.colorbar()
  # plt.xlim([0, 1600])
  # plt.xlim([0, 800]) # U
  # plt.xlim([800, 1600]) # V
  plt.xlim([2080, 2560]) # W
  # plt.clim([2300,2400]) # orig U, V
  # plt.clim([885,915]) # orig W
  plt.clim([0,10000])

  # plt.grid()
  # plt.show()
  plt.savefig('{}-{}.png'.format(tag,event), dpi=300)
  return


if __name__ == '__main__':
  apa = 0
  tags = [
    # 'ductor'
    # 'orig',
    'gauss'
  ]
  
  data = h5py.File('g4-rec-%d.h5'%apa, 'r')
  # data = h5py.File('g4-tru-%d.h5'%apa, 'r')

  plt.figure()

  start = 100
  for event in range(start, start+len(list(data.keys()))) :
    print("hioplot event: ", event)
    for tag in tags:
      show_frame(data, event, apa, tag)