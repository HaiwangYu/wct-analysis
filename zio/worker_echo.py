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
    worker = Worker("tcp://localhost:5555", b"echo", zmq.CLIENT, verbose=False)
    reply = None
    while True:
        request = worker.recv(reply)
        if request is None:
            break # Worker was interrupted
        m = zio.Message()
        m.fromparts(request)
        if verbose:
            logging.info("echo: %s", m)
        reply = m.toparts()

if __name__ == '__main__':
    main()