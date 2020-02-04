#!/usr/bin/env python
# -*- coding: utf-8 -*-

# common 
import sys
import os
import os.path as op

# dev: override installed
sys.path.insert(0, op.join(op.dirname(__file__), '..', '..'))

# bluemath climate_downloader csiro module 
from climate_downloader import csiro


# --------------------------------------------------------------------------- #
# data
p_data = op.abspath(op.join(op.dirname(__file__), '..', '..', 'data', 'download'))

# paths 
p_nc_grid = op.join(p_data, 'csiro_area', 'gridded')
p_nc_spec = op.join(p_data, 'csiro_area', 'spec')


# area coordinates (lon, lat)
lon1 = 168
lat1 = 8
lon2 = 170
lat2 = 10

# time start - time end (optional, 'yyyymm' format)
t_lims = ('199001', '199003')

# download area spec data
csiro.download_spec_area(
    p_nc_spec,
    lon1, lat1, lon2, lat2,
    time_limits=t_lims
)

# download area gridded data
gc = 'glob_24m'
csiro.download_gridded_area(
    p_nc_grid,
    lon1, lat1, lon2, lat2, gc,
    time_limits=t_lims
)

