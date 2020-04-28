#!/usr/bin/env python

import numpy as np
import h5py
from PIL import Image


def rebin(a, shape):
  sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
  if len(a.shape) == 3:
    sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1],a.shape[2]
  return a.reshape(sh).mean(3).mean(1)

def save_frame(data, event, apa, tag) :
  key = '/%d/frame_%s%d'%(event,tag,apa)
  f = data.get(key)
  if f is None:
    print('f is None')
    return
  frame = np.array(f)
  frame = frame[:,2079:2559]
  frame = rebin(frame,[frame.shape[0]//10,frame.shape[1]])
  print(frame.shape)
  
  # csv
  # np.savetxt('{}-{}.csv'.format(tag,event), frame, delimiter=',')
  
  # hdf5
  # with h5py.File('{}-{}.h5'.format(tag,event), 'w') as hf:
  #   hf.create_dataset("frame",  data=frame)

  # numpy
  with open('{}-{}.npy'.format(tag,event), 'wb') as f:
    np.save(f, frame)
  
  # png
  # print(np.max(frame), ', ', np.min(frame))
  # frame = frame - np.min(frame)
  # frame = frame/(np.max(frame)-np.min(frame))*255
  # img = Image.fromarray(np.uint8(frame) , 'L')
  # img.save('{}-{}.png'.format(tag,event))
  
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

  start = 100
  for event in range(start, start+len(list(data.keys()))) :
    print("hioexport event: ", event)
    for tag in tags:
      save_frame(data, event, apa, tag)