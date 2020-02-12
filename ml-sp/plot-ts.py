#!/usr/bin/env python

import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

if __name__ == '__main__':
  apa = 0
  tags = [
    'dlroi',
    'dlcharge',
    # 'ch0',
    # 'ch1',
    # 'ch2',
  ]
  
  data = h5py.File('tsmodel-eval.h5','r')

  xlim = [0, 800]
  # xlim = [800,1600]
  # xlim = [0,2560]

  for event in range(0, 1) :

    fig = plt.figure()
    a = fig.add_subplot(1, 1, 1)
    a.set_title('SP charge')
    frame_ma = np.ma.array(np.array(data.get('/%d/frame_%s%d'%(event,tags[1],apa))))
    # plt.imshow(np.ma.masked_where(frame_ma<=0,frame_ma), cmap="bwr_r", origin='lower')
    print ("frame_ma.shape: ", frame_ma.shape)
    plt.imshow(np.transpose(frame_ma, axes=[1, 0])
    ,aspect='auto'
    # ,aspect=0.8/4.7
    ,cmap="bwr", origin='lower')
    plt.xlim(xlim)
    # plt.clim(-1,1)
    plt.clim(-4000,4000)
    # plt.colorbar()
    plt.grid()

    # fig = plt.figure()
    # a = fig.add_subplot(1, 1, 1)
    # a.set_title('CH2')
    # frame_ma = np.ma.array(np.array(data.get('/%d/frame_%s%d'%(event,tags[2],apa))))
    # plt.imshow(np.ma.masked_where(frame_ma<=0,frame_ma), cmap="jet", origin='lower')
    # # plt.xlim(xlim)
    # # plt.colorbar()
    # plt.grid()

    # fig = plt.figure()
    # a = fig.add_subplot(1, 1, 1)
    # a.set_title('CH3')
    # frame_ma = np.ma.array(np.array(data.get('/%d/frame_%s%d'%(event,tags[3],apa))))
    # plt.imshow(np.ma.masked_where(frame_ma<=0,frame_ma), cmap="jet", origin='lower')
    # # plt.xlim(xlim)
    # # plt.colorbar()
    # plt.grid()

    fig = plt.figure()
    a = fig.add_subplot(1, 1, 1)
    a.set_title('ROI')
    mask = np.array(data.get('/%d/frame_%s%d'%(event,tags[0],apa)))
    print ("mask.shape: ", mask.shape)
    plt.imshow(np.transpose(mask, axes=[1, 0])
    , origin='lower'
    , aspect='auto'
    # , aspect=0.8/4.7
    )
    # print("Mask non-zero",np.count_nonzero(mask))
    # plt.colorbar()
    plt.xlim(xlim)
    plt.clim(0.0,1)
    plt.grid()

    plt.show()


