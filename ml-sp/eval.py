#!/usr/bin/env python

import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def criteria(a):
  if a > 0:
    return True
  else:
    return False

def rebin(a, shape):
  sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
  if len(a.shape) == 3:
    sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1],a.shape[2]
  return a.reshape(sh).mean(3).mean(1)

def eval_roi(f0, f1, th0 = 0, th1 = 0.5):
  f0m = f0.copy()
  f1m = f1.copy()
  f0m[f0m<=th0] = 0
  f0m[f0m>th0] = 1
  f1m[f1m<=th1] = 0
  f1m[f1m>th1] = 1
  num = 0
  den = 0
  for ich in range(0, f0m.shape[1]):
    start = 0
    end = 0
    for it in range(0, f0m.shape[0]):
      if f0m[it,ich] <= 0:
        if start < end:
          # print(ich, ', ', start, ', ', end, ' : ', np.count_nonzero(f1m[start:end,ich]))
          den = den + 1
          if np.count_nonzero(f1m[start:end,ich]) > 0:
            num = num + 1
        start = it
      else:
        end = it
  # print("efficiency: ", num, "/", den, " = ", (num)/den*100, "%")
  return [num, den]

def eval_pixel(f0, f1, th0 = 0, th1 = 0.5):
  f0m = f0.copy()
  f1m = f1.copy()
  f0m[f0m<=th0] = 0
  f0m[f0m>th0] = 1
  f1m[f1m<=th1] = 0
  f1m[f1m>th1] = 1
  num = np.count_nonzero(np.logical_and(f0m, f1m))
  den = np.count_nonzero(f0m)
  # print("efficiency: ", num, "/", den, " = ", (num)/den*100, "%")
  return [num, den]


def frame_truth(dataset, event, apa):
  apa   = 0
  tag   = 'ductor'
  data  = h5py.File('%s/g4-tru-%d.h5'%(dataset,apa), 'r')
  key   = '/%d/frame_%s%d'%(event,tag,apa)
  f0    = np.array(data[key])
  f0    = f0[:,800:1600]
  return f0

def frame_gauss(dataset, event, apa):
  tag   = 'gauss'
  data  = h5py.File('%s/g4-rec-%d.h5'%(dataset,apa), 'r')
  key   = '/%d/frame_%s%d'%(event,tag,apa)
  f1    = np.array(data[key])
  f1    = f1[:,800:1600]
  return f1

def frame_dlroi(dataset, event, apa):
  tag   = 'dlroi'
  data  = h5py.File('%s/tsmodel-eval.h5'%(dataset), 'r')
  key   = '/%d/frame_%s%d'%(event,tag,apa)
  f1    = np.array(data[key])
  f1    = np.transpose(f1, axes=[1,0])
  return f1

def plot_frame(f0, f1, truth_th = 0, reco_th = 0.5):
  fig = plt.figure()
  a = fig.add_subplot(1, 1, 1)
  a.set_title('Reco')
  plt.imshow(
    np.ma.masked_where(f1<=reco_th,f1)
    , cmap='hot_r', interpolation="none"
    # , extent = [0 , 2560, 0 , 600]
    , origin='lower'
    , aspect='auto'
  )
  f0m   = f0.copy()
  f0m[f0m<=truth_th] = 0
  f0m[f0m>truth_th] = 1
  plt.imshow(
    np.ma.masked_where(f0m<=0,f0m)
    , cmap='cool', interpolation="none"
    # , extent = [0 , 2560, 0 , 600]
    , origin='lower'
    , aspect='auto'
    , alpha=0.4
  )
  plt.grid()
  plt.show()

def eff_and_pur(dataset='./', gauss_input = False, roi_eval = False):
  if gauss_input == True:
    f0 = frame_truth(dataset, event, apa)
    f1 = frame_gauss(dataset, event, apa)
    truth_th = 100
    reco_th = 100
  else:
    f0 = frame_truth(dataset, event, apa)
    f0 = rebin(f0, [f0.shape[0]//10, f0.shape[1]])
    f1 = frame_dlroi(dataset, event, apa)
    truth_th = 100
    reco_th = 0.5

  # print('f0.shape: ', f0.shape)
  # print('f1.shape: ', f1.shape)

  # f0m = np.vectorize(criteria)(f0)
  # f1m = np.vectorize(criteria)(f1)

  # plot_frame(f0, f1, truth_th, reco_th)

  if roi_eval == True:
    [num, den] = eval_roi(f0, f1, truth_th, reco_th)
    print("efficiency: ", num, "/", den, " = ", (num)/den*100, "%")
    eff = (num)/den*100  
    [num, den] = eval_roi(f1, f0, reco_th, truth_th)
    print("purity: ", num, "/", den, " = ", (num)/den*100, "%")
    pur = (num)/den*100
  else:
    [num, den] = eval_pixel(f0, f1, truth_th, reco_th)
    print("efficiency: ", num, "/", den, " = ", (num)/den*100, "%")
    eff = (num)/den*100
    [num, den] = eval_pixel(f1, f0, reco_th, truth_th)
    print("purity: ", num, "/", den, " = ", (num)/den*100, "%")
    pur = (num)/den*100

  return [eff, pur]

if __name__ == '__main__':

  event = 0
  apa   = 0

  labels = [
    '75-75',
    '80-80',
    '82-82',
    '85-85',
    '87-75',
    '87-85',
    '87-87',
  ]
  eff_rf = []
  pur_rf = []
  eff_dl = []
  pur_dl = []
  eff_mp = []
  pur_mp = []

  for label in labels:
    [eff, pur] = eff_and_pur('nf-on/ref-'+label, gauss_input=True, roi_eval=True)
    eff_rf.append(eff)
    pur_rf.append(pur)
    # [eff, pur] = eff_and_pur('nf-on/eval-'+label, gauss_input=True, roi_eval=True)
    # eff_mp.append(eff)
    # pur_mp.append(pur)
    [eff, pur] = eff_and_pur('nf-on/eval-'+label, gauss_input=False, roi_eval=True)
    eff_dl.append(eff)
    pur_dl.append(pur)

  x = np.arange(len(labels))  # the label locations
  width = 0.20  # the width of the bars
  fig = plt.figure()
  ax = fig.add_subplot(2, 1, 1)
  # ax.bar(x - width, eff_rf, width, label='Ref.')
  # ax.bar(        x, eff_mp, width, label='MP')
  # ax.bar(x + width, eff_dl, width, label='DNN')
  ax.bar(x - width/2, eff_rf, width, label='Ref.')
  ax.bar(x + width/2, eff_dl, width, label='DNN')
  ax.set_ylabel('Efficiency [%]', fontsize=18)
  ax.set_xlabel(r'$\theta_{xz}(V)$ - $\theta_{xz}(U)$', fontsize=18)
  ax.legend(loc='best',fontsize=20)
  ax.grid()
  plt.ylim([0, 150])
  plt.xticks(x, labels, fontsize=18)

  ax = fig.add_subplot(2, 1, 2)
  # ax.bar(x - width, pur_rf, width, label='Ref.')
  # ax.bar(        x, pur_mp, width, label='MP')
  # ax.bar(x + width, pur_dl, width, label='DNN')
  ax.bar(x - width/2, pur_rf, width, label='Ref.')
  ax.bar(x + width/2, pur_dl, width, label='DNN')
  ax.set_ylabel('Purity [%]', fontsize=18)
  ax.set_xlabel(r'$\theta_{xz}(V)$ - $\theta_{xz}(U)$', fontsize=18)
  ax.legend(loc='best',fontsize=20)
  ax.grid()
  plt.ylim([0, 150])
  plt.xticks(x, labels, fontsize=18)

  plt.show()