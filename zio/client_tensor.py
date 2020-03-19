"""
Majordomo Protocol client example. Uses the mdcli API to hide all MDP aspects

Author : Min RK <benjaminrk@gmail.com>

"""

import sys
from zio.domo.client import Client
import zmq
import zio
import json
import numpy as np
import h5py

import h5_utils as h5u

def main():
    verbose = '-v' in sys.argv
    client = Client("tcp://localhost:5555", zmq.CLIENT, verbose)
    requests = 1
    for i in range(requests):
        img = np.zeros((2,2,20),dtype=np.float32)
        try:
            label_tens = [{"dtype":'f',"part":1,"shape":img.shape,"word":4}]
            label_meta = {"tick":500}
            label_comb = {"TENS":{"tensors":label_tens, "metadata":label_meta}}
            label = json.dumps(label_comb)
            m = zio.Message(form='TENS', label=label, 
                 level=zio.MessageLevel.warning,
                 payload=[img.tobytes()])
            mmsg = m.toparts()
            print(mmsg)
            client.send(b"echo", mmsg)
        except KeyboardInterrupt:
            print ("send interrupted, aborting")
            return

    count = 0
    while count < requests:
        try:
            reply = client.recv()
        except KeyboardInterrupt:
            break
        else:
            # also break on failure to reply:
            if reply is None:
                break
            m = zio.Message()
            m.fromparts(reply)
            print(m)
        count += 1
    print ("%i requests/replies processed" % count)

if __name__ == '__main__':
    main()