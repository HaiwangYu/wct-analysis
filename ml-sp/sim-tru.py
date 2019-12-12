#!/usr/bin/env python

import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def show_frame(data, event, apa, tag) :
  key = '/%d/frame_%s%d'%(event,tag,apa)
  frame = np.array(data[key])
  frame_ma = np.ma.array(frame)
  plt.imshow(np.ma.masked_where(frame_ma<=50,frame_ma), cmap="rainbow", interpolation="none"
  #plt.imshow(frame, cmap="rainbow", interpolation="none"
  # , extent = [0 , 2560, 0 , 600]
  # , extent = [0 , 2300, 0 , 4800]
  #, norm=LogNorm()
  , origin='lower'
  , aspect=0.8/4.7
  )
  plt.colorbar()
  # plt.xlim([0,2560])
  plt.xlim([0,1600])
  # plt.xlim([0, 1600])
  # plt.ylim([4000, 4500])
  # plt.clim([0,5000])
  plt.grid()
  plt.show()


if __name__ == '__main__':
  apa = 0
  tag = 'ductor'
  data = h5py.File('mu-prolonged-v-100-events/g4-tru-%d.h5'%apa, 'r')


  plt.figure()

  for event in range(0, len(list(data.keys()))) :
    print("processing event: ", event)
    show_frame(data, event, apa, tag)