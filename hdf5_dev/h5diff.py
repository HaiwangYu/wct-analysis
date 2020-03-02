#!/usr/bin/env python

import sys
import numpy as np
import h5py
import matplotlib.pyplot as plt

def get_dataset(fn, key):

  data = h5py.File(fn, 'r')
  f = data.get(key)
  if f is None:
    print('f is None')
    return None
  frame = np.array(f)
  print(frame.shape)
  return frame

if __name__ == '__main__':

  fn1 = sys.argv[1]
  fn2 = sys.argv[2]
  key1 = sys.argv[3]
  key2 = sys.argv[3]
  if len(sys.argv) > 4:
    key2 = sys.argv[4]
  
  d1 = get_dataset(fn1, key1)
  d2 = get_dataset(fn2, key2)

  plt.gca().set_title(fn2 + ' - ' + fn1)
  plt.imshow(d2-d1, cmap="bwr", interpolation="none"
  # , extent = [0 , 2560, 0 , 6000]
  , origin='lower'
  , aspect='auto'
  # , aspect=0.8/4.7
  # , aspect=0.1
  )
  # plt.colorbar()
  # plt.xlim([0, 1600])
  # plt.xlim([0, 800]) # U
  # plt.xlim([800, 1600]) # V
  plt.clim([-1,1])

  plt.grid() 
  plt.show()



