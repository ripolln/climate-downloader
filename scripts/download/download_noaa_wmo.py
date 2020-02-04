#!/usr/bin/env python
# -*- coding: utf-8 -*-

# common 
import sys
import os
import os.path as op

# dev bluemath library 
sys.path.insert(0, op.join(op.dirname(__file__), '..', '..'))

# bluemath climate_downloader noaa module 
from climate_downloader import noaa


# --------------------------------------------------------------------------- #
# data
p_data = op.abspath(op.join(op.dirname(__file__), '..', '..', 'data', 'download'))
p_demo = op.join(p_data, 'noaa')
if not op.isdir(p_demo):
    os.makedirs(p_demo)

p_nc = op.join(p_demo, 'allstorms.ibtracs_all.nc')

# download all storms
noaa.download_ibtracs_all(p_nc)

