#!/usr/bin/env python
# -*- coding: utf-8 -*-

# common 
import sys
import os
import os.path as op

# dev: override installed
sys.path.insert(0, op.join(op.dirname(__file__), '..', '..'))

# bluemath climate_downloader csiro module 
from climate_downloader import noaa


# --------------------------------------------------------------------------- #
# data
p_data = op.abspath(op.join(op.dirname(__file__), '..', '..', 'data', 'download'))

# paths 
p_down = op.join(p_data, 'noaa_sst_v5')

# download SSTv5
data = noaa.download_sst_v5(p_down, overwrite=False)

print(data)

