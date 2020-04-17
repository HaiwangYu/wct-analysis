"""Majordomo Protocol worker example.

Uses the mdwrk API to hide all MDP aspects

Author: Min RK <benjaminrk@gmail.com>
"""

import sys
import logging
from zio.domo.worker import Worker
import zmq
import zio
import json
import numpy as np
import torch

def main():
    verbose = '-v' in sys.argv
    worker = Worker("tcp://localhost:5555", b"torch:dnnroi", zmq.CLIENT, verbose=False)
    model = "ts-model/unet-l23-cosmic500-e50.ts"
    net = torch.jit.load(model)
    net.cuda()
    reply = None
    while True:
        request = worker.recv(reply)
        if request is None:
            break # Worker was interrupted
        m = zio.Message()
        m.fromparts(request)
        # logging.info('worker::recv: %s', m)
        label = json.loads(m.label)
        label_tens = label["TENS"]["tensors"]
        label_meta = label["TENS"].get("metadata")
        shape = label_tens[0]["shape"]
        # FIXME why a empty payload first
        payload = m._payload[0]
        if len(payload) == 0 :
            payload = m._payload[1]
        img = np.frombuffer(payload, dtype='f').reshape(shape)

        # numpy -> numpy
        img_tensor = torch.from_numpy(img) # chw
        img_tensor = img_tensor.cuda()
        with torch.no_grad():
            # input = img_tensor.unsqueeze(0)
            input = img_tensor
            if verbose:
              logging.info("input.shape: %s", input.shape)
            mask = net.forward(input).cpu().numpy() # 4D
            if verbose:
              logging.info("mask.shape: %s", mask.shape)

        label_tens = [{"dtype":'f',"part":0,"shape":mask.shape,"word":4}]
        m = zio.Message(form='TENS',
              label=json.dumps({"TENS":{"tensors":label_tens, "metadata":label_meta}}), 
              level=zio.MessageLevel.warning,
              payload=[mask.tobytes()])
        # logging.info('worker::send: %s', m)
        reply = m.toparts()



if __name__ == '__main__':
    main()