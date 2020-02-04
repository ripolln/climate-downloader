#!/usr/bin/env python
# -*- coding: utf-8 -*-

# common 
import os
import os.path as op

# dev: override installed
import sys
sys.path.insert(0, op.join(op.dirname(__file__), '..', '..'))

# pip
import numpy as np

# bluemath climate_downloader csiro module 
from climate_downloader import csiro


# --------------------------------------------------------------------------- #
# data
p_data = op.abspath(op.join(op.dirname(__file__), '..', '..', 'data', 'download'))

# paths 
p_demo = op.join(p_data, 'csiro_datamap')
if not op.isdir(p_demo):
    os.makedirs(p_demo)
p_nc_grid = op.join(p_demo, 'gridded')
p_nc_spec = op.join(p_demo, 'spec_info.nc')

# download spec info
xds_ispec = csiro.download_info_spec(p_nc_spec)
print('SPEC')
print(xds_ispec)
print()

# download point gridded data
print('GRIDDED')
ls_xds_igridd = csiro.download_info_gridded(p_nc_grid)
for xds_ig in ls_xds_igridd:
    print(xds_ig)
    print()

