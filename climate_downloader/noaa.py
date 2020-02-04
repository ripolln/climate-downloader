#!/usr/bin/env python
# -*- coding: utf-8 -*-

# common
import sys
import os
import os.path as op
import urllib.request
import gzip
import shutil
import time

# pip
import numpy as np
import xarray as xr


def download_ibtracs_all(p_ncfile):
    '''
    Download storms (Allstorms.ibtracs_all) netcdf from NOAA

    ftp file name: Allstorms.ibtracs_all.v03rXX.nc.
    ftp wind velocity in knots: x1.82 km/h
    '''

    # default parameters
    # TODO: update version
    ftp_down = 'ftp://eclipse.ncdc.noaa.gov/pub/ibtracs/v03r10/wmo/netcdf/'
    fil_down = 'Allstorms.ibtracs_wmo.v03r10.nc.gz'

    p_down = op.dirname(p_ncfile)
    p_gz = op.join(p_down, '{0}'.format(fil_down))
    p_temp = op.join(p_down, 'tempdl.nc')  # temporal file

    # download gz
    ftp_wmo = '{0}{1}'.format(ftp_down, fil_down)
    if not op.isfile(p_gz):
        urllib.request.urlretrieve(ftp_wmo, p_gz)

    # decompress .gz file
    with gzip.open(p_gz, 'rb') as f_in, open(p_temp, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

    # load and return xarray.Dataset
    xds_wmo = xr.open_dataset(p_temp).copy()

    # set lon to 0-360
    lon_wmo = xds_wmo.lon_wmo.values[:]
    lon_wmo[np.where(lon_wmo<0)] = lon_wmo[np.where(lon_wmo<0)]+360
    xds_wmo['lon_wmo'].values[:] = lon_wmo

    # store changes
    xds_wmo.to_netcdf(p_ncfile, 'w')

    # remove temp files
    os.remove(p_temp)
    os.remove(p_gz)

