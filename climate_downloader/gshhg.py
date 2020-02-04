#!/usr/bin/env python
# -*- coding: utf-8 -*-

# common 
import os
import os.path as op
import sys

# pip 
import numpy as np
import shapefile

# docs: 
# http://www.soest.hawaii.edu/pwessel/gshhg/

def extract_shoreline(p_db, lon1_q, lat1_q, lon2_q, lat2_q):
    'Extract shoreline from GSHHG database'

    # GSHHG database files
    p_sh = op.join(p_db, 'GSHHG','gshhg-shp-2.3.7')

    # parameters
    db = 'GSHHS'  # GSHHS, WDBII (WDBII for border and river)
    resol = 'f'  # f, h, i, l, c (full, high, intermediate, low, crude)
    shore_l = 'L1'  # boundary between land and ocean, except Antartica

    # shapefile
    nfd = '{0}_shp'.format(db)
    nfl = '{0}_{1}_{2}.shp'.format(db, resol, shore_l)
    p_shp = op.join(p_sh, nfd, '{0}'.format(resol), nfl)

    # find shapefiles inside query area
    with shapefile.Reader(p_shp) as fR:
        shapes = fR.shapes()

        sel_shapes = []
        for ss in shapes:
            lon1_bb, lat1_bb, lon2_bb, lat2_bb = ss.bbox
            if not any(
                [
                    lon2_bb < lon1_q,
                    lon1_bb > lon2_q,
                    lat2_bb < lat1_q,
                    lat1_bb > lat2_q,
                ]
            ):
                sel_shapes.append(ss)

    # get shoreline data from shapefiles
    shore_lon = np.array([])
    shore_lat = np.array([])
    for ss in sel_shapes:

        # get shape lon and lat as np array 
        ss_lon = np.array([tup[0] for tup in ss.points])
        ss_lat = np.array([tup[1] for tup in ss.points])

        # remove data inside shape but outside bounding box
        ix_out = np.where(
            (ss_lon < lon1_q) | (ss_lon > lon2_q) | \
            (ss_lat < lat1_q) | (ss_lat > lat2_q)
        )
        ss_lon = np.delete(ss_lon, ix_out)
        ss_lat = np.delete(ss_lat, ix_out)

        # add nan to split coast
        ss_lon = np.append(ss_lon, np.nan)
        ss_lat = np.append(ss_lat, np.nan)

        # concatenate
        shore_lon = np.append(shore_lon, ss_lon)
        shore_lat = np.append(shore_lat, ss_lat)

    return np.column_stack((shore_lon, shore_lat))

