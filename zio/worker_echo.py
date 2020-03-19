"""Majordomo Protocol worker example.

Uses the mdwrk API to hide all MDP aspects

Author: Min RK <benjaminrk@gmail.com>
"""

import sys
from generaldomo.worker import Worker
import zmq
import zio
import json
import numpy as np
import torch

def main():
    verbose = '-v' in sys.argv
    worker = Worker("tcp://localhost:5555", b"echo", zmq.CLIENT, verbose)
    reply = None
    while True:
        request = worker.recv(reply)
        if request is None:
            break # Worker was interrupted
        m = zio.Message()
        m.fromparts(request)
        # m.decode(request)
        print(m)
        reply = m.toparts()

if __name__ == '__main__':
    main()