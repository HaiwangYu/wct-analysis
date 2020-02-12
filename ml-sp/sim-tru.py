#!/usr/bin/env python

import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def show_frame(data, event, apa, tag) :
  key = '/%d/frame_%s%d'%(event,tag,apa)
  f = data.get(key)
  if f is None:
    print('f is None')
    return
  frame = np.array(f)
  frame_ma = np.ma.array(frame)
  plt.imshow(np.ma.masked_where(frame_ma<=50,frame_ma), cmap="bwr", interpolation="none"
  #plt.imshow(frame, cmap="rainbow", interpolation="none"
  # , extent = [0 , 2560, 0 , 600]
  # , extent = [0 , 2300, 0 , 4800]
  #, norm=LogNorm()
  , origin='lower'
  # , aspect=0.8/4.7 # 1 tick ~ 0.8 mm; 1 pitch ~ 4.7 mm 
  # , aspect=0.1
  , aspect='auto'
  )
  # plt.colorbar()
  # plt.xlim([0,800]) # U
  # plt.xlim([800,1600]) # V
  # plt.ylim([4000, 4500])
  # plt.clim([0,5000])
  plt.grid()
  plt.show()


if __name__ == '__main__':
  apa = 0
  tag = 'ductor'

  data = h5py.File('eval-80-80/g4-tru-%d.h5'%apa, 'r')


  plt.figure()

  for event in range(0, len(list(data.keys()))) :
    print("processing event: ", event)
    show_frame(data, event, apa, tag)