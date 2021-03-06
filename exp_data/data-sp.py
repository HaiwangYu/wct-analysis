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
  frame = np.array(data[key])
  frame_ma = np.ma.array(frame)

  # plt.hist(frame.reshape(-1), bins=100, range=(-2000,2000))

  # plt.imshow(frame_ma, cmap="rainbow", interpolation="none"
  plt.imshow(np.ma.masked_where(frame_ma<=0,frame_ma), cmap="rainbow", interpolation="none"
  , extent = [0 , 2560, 0 , 600]
  , origin='lower'
  , aspect='auto'
  )
  plt.colorbar()
  # plt.xlim([0, 2560])
  # plt.xlim([0, 800]) # U
  plt.xlim([800, 1600]) # V
  # plt.ylim([4000, 4500])
  plt.clim([0,10000])

  plt.grid() 
  plt.show()
  return


if __name__ == '__main__':
  apa = 0
  tags = [
  # 'tight_lf', 
  # 'loose_lf', 
  # 'cleanup_roi', 
  # 'mp_roi', 
  # 'break_roi_1st', 
  # 'break_roi_2nd', 
  # 'shrink_roi', 
  # 'extend_roi', 
  'gauss'
  ]
  # data = h5py.File('g4-rec-%d.h5'%apa, 'r')
  data = h5py.File('data-%d.h5'%apa, 'r')


  plt.figure()

  # for event in range(0, len(list(data.keys()))) :
  for event in range(0, len(list(data.keys()))) :
    print("processing event: ", event)
    for tag in tags:
      show_frame(data, event, apa, tag)

  # plt.figure()
  # tag   = 'tight_lf'
  # key   = '/0/frame_%s%d'%(tag,apa)
  # for ch in range(800, 900, 10):
  #   print("processing channel: ", ch)
  #   wave = get_wave(data, key, ch, 4300, 4800)
  #   plt.plot(wave,'-o', label='ch=%d'%ch)
  #   plt.legend()
  #   plt.grid()
  #   plt.show()


