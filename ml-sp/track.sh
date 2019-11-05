#!/usr/bin/env bash

time wire-cell -l stdout -l wct-sim-check.log -L info -L io:debug -L ana:trace -c wct-sim-check.jsonnet
