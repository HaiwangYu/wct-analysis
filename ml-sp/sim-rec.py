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

  plt.gca().set_title(tag)

  # plt.hist(frame.reshape(-1), bins=100, range=(-2000,2000))

  # plt.imshow(np.ma.masked_where(frame_ma<=0,frame_ma), cmap="rainbow", interpolation="none"
  # plt.imshow(frame_ma>0, cmap="viridis", interpolation="none"
  plt.imshow(frame_ma, cmap="bwr", interpolation="none"
  # , extent = [0 , 2560, 0 , 6000]
  , origin='lower'
  , aspect='auto'
  # , aspect=0.8/4.7
  # , aspect=0.1
  )
  # plt.colorbar()
  # plt.xlim([0, 2560])
  # plt.xlim([0, 800]) # U
  plt.xlim([800, 1600]) # V
  # plt.clim([0,1])
  plt.clim([-4000,4000])

  plt.grid() 
  plt.show()
  return


if __name__ == '__main__':
  apa = 0
  tags = [
    # 'decon_charge',
    # 'tight_lf',
    # 'loose_lf',
    # 'mp2_roi',
    # 'mp3_roi',
    # 'cleanup_roi',
    # 'break_roi_1st',
    # 'break_roi_2nd',
    # 'shrink_roi',
    # 'extend_roi',
    # 'dnn_sp'
    'gauss'
  ]
  

  data = h5py.File('data-%d.h5'%apa, 'r')


  plt.figure()

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


