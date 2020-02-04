#!/usr/bin/env python
# -*- coding: utf-8 -*-

# common
import os
import os.path as op
import sys

# pip
import numpy as np

# dev: override library 
sys.path.insert(0, op.join(op.dirname(__file__), '..', '..'))

# bluemath climate_downloader gebco and gshhg modules
from climate_downloader import gebco, gshhg


# --------------------------------------------------------------------------- #
# resources and output
p_res = op.abspath(op.join(op.dirname(__file__), '..', '..',
                           'climate_downloader', 'resources'))
p_ext = op.abspath(op.join(op.dirname(__file__), '..', '..', 'data', 'extract'))

# output sub folder
p_out = op.join(p_ext, 'Guam')

# --------------------------------------
# extraction query
lon1_q, lon2_q = 144, 145  # -180 / 180
lat1_q, lat2_q = 13, 14   # -90 / 90

# GEBCO: extract bathymetry
xds_depth = gebco.extract_bathymetry(p_res, lon1_q, lat1_q, lon2_q, lat2_q)

# GSHHG: extract shoreline
np_shore = gshhg.extract_shoreline(p_res, lon1_q, lat1_q, lon2_q, lat2_q)


# --------------------------------------
# store data to files
if not op.isdir(p_out): os.makedirs(p_out)
print(xds_depth)

xds_depth.to_netcdf(op.join(p_out, 'depth.nc'),'w')  # depth to .nc file 
np.save(op.join(p_out, 'shore.npy'), np_shore)  # shore to .npy file

