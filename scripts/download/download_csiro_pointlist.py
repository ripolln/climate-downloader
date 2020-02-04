#!/usr/bin/env python
# -*- coding: utf-8 -*-

# common 
import os
import os.path as op

# dev: override installed
import sys
sys.path.insert(0, op.join(op.dirname(__file__), '..', '..'))

# bluemath climate_downloader csiro module 
from climate_downloader import csiro


# --------------------------------------------------------------------------- #
# data
p_data = op.abspath(op.join(op.dirname(__file__), '..', '..', 'data', 'download'))

# paths 
p_nc_grid = op.join(p_data, 'csiro_pointlist', 'gridded')
p_nc_spec = op.join(p_data, 'csiro_pointlist', 'spec')


# point list (lon, lat)
l_points = [(167.2, 9.6), (168, 9.2), (167.2, 8.4), (166.4, 9.2)]

# time start - time end (optional, 'yyyymm' format)
t_lims = ('199001', '199003')


# download point spec data
csiro.download_spec(p_nc_spec, l_points, time_limits=t_lims)

# download point gridded data
gc = 'glob_24m'
csiro.download_gridded(p_nc_grid, l_points, gc, time_limits=t_lims)

