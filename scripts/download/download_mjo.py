#!/usr/bin/env python
# -*- coding: utf-8 -*-

# common 
import sys
import os
import os.path as op


# dev bluemath library 
sys.path.insert(0, op.join(op.dirname(__file__), '..', '..'))

# bluemath climate_downloader mjo module 
from climate_downloader import mjo


# --------------------------------------------------------------------------- #
# data
p_data = op.abspath(op.join(op.dirname(__file__), '..', '..', 'data', 'download'))
p_nc_mjo = op.join(p_data, 'mjo.nc')

# Download MJO and store it in netcdf
y1 = '1979-01-01'
mjo.download(p_nc_mjo, init_year=y1)

