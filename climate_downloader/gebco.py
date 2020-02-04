#!/usr/bin/env python
# -*- coding: utf-8 -*-

# common
import os
import os.path as op

# pip
import xarray as xr


def extract_bathymetry(p_db, lon1_q, lat1_q, lon2_q, lat2_q, ids=False):
    'Extract bathymetry and ID from GEBCO database'

    # GEBCO database files
    p_gc = op.join(p_db, 'GEBCO', 'GEBCO_2019', 'GEBCO_2019.nc')
    p_id = op.join(p_db, 'GEBCO', 'GEBCO_2019_SID', 'GEBCO_2019_SID.nc')

    # depth
    with xr.open_dataset(p_gc) as xds_gc:
        xds_gc_area = xds_gc.sel(
            lon = slice(lon1_q, lon2_q),
            lat = slice(lat1_q, lat2_q),
        )
    xds_out = xds_gc_area

    # id (decode_cf=False needed)
    if ids:
        with xr.open_dataset(p_id, decode_cf=False) as xds_id:
            xds_id_area = xds_id.sel(
                lon = slice(lon1_q, lon2_q),
                lat = slice(lat1_q, lat2_q),
            )
        xds_out = xr.merge([xds_gc_area, xds_id_area])

    return xds_out

