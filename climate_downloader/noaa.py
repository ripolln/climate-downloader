#!/usr/bin/env python
# -*- coding: utf-8 -*-

# common
import sys
import os
import os.path as op
import urllib.request
import requests
import gzip
import shutil
import time
from bs4 import BeautifulSoup

# pip
import numpy as np
import xarray as xr


def download_ibtracs_all(p_store):
    '''
    Download storms IBTrACS.ALL.v04r00.nc
    '''

    # ibtracks url
    url = 'https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r00/access/netcdf/'
    fn = 'IBTrACS.ALL.v04r00.nc'

    # prepare download folder
    if not op.isdir(p_store): os.makedirs(p_store)

    # download file
    remote = url + fn
    local = op.join(p_store, fn)

    with requests.get(remote) as fr, open(local, 'wb')as fl:
        fl.write(fr.content)

    print("{0} downloaded.".format(local))

    return xr.open_dataset(local)

def download_sst_v5(p_store, year_limits=(None, None), overwrite=False):
    '''
    Download NOAA SST data and stores it on netcdf format

    p_store      - path to store downloaded data
    year_limits  - optional. Start and end years to download
    overwrite    - True for overwriting previously downloaded files
    '''
    # prepare download folder
    p_dl = op.join(p_store, 'sst_v5.download')  # temp storage of monthly files
    if not op.isdir(p_dl): os.makedirs(p_dl)

    # default parameters
    url = 'https://www1.ncdc.noaa.gov/pub/data/cmb/ersst/v5/netcdf/'
    code = 'ersst.v5'

    # activate a requests session
    s = requests.Session()

    # get files at public folder (tryouts)
    sc = 999
    cts = 1
    max_cts = 10
    while sc != 200:
        print('establishing connection... tryout number {0}/{1}'.format(cts, max_cts))
        page = s.get(url)
        sc = page.status_code
        cts +=1

        # break if unable to connect
        if cts == max_cts:
            print('Unable to query NOAA database. Try again later')
            return None

    soup = BeautifulSoup(page.text, 'html.parser')
    fs = ['{0}{1}'.format(url, n.get('href')) for n in soup.find_all('a') if n.get('href').startswith(code)]

    # filter files by year
    if year_limits[0]:
        yy = [f for f in fs if str(year_limits[0]) in f][0]
        fs = fs[fs.index(yy):]
    if year_limits[1]:
        yy = [f for f in fs if str(year_limits[1]) in f][-1]
        fs = fs[:fs.index(yy)+1]

    # download files
    print('downloading files ')
    for remote in fs:

        fn = op.basename(remote)
        local = op.join(p_dl, fn)

        # skip if overwrite off
        if overwrite == False and op.isfile(local):
            continue

        # download file (with retries)
        ret = True
        while ret:

            # retry if bad status code
            fr = s.get(remote)
            if fr.status_code == 200:

               # write local file and stop retry
                with open(local, 'wb') as fl:
                    fl.write(fr.content)
                ret = False

        print(fn)
    print()

    # join files
    fjs = [op.join(p_dl, x) for x in sorted(os.listdir(p_dl)) if x.endswith('.nc')]
    ts = [d.split('.')[-2] for d in fjs]
    ts = [np.datetime64('{0}-{1}-{2}'.format(x[:4], x[4:], '01')) for x in ts]

    # get coordinates and attributes from downloaded files
    tmp_0 = xr.open_dataset(fjs[0]).squeeze(drop=True)
    tmp_1 = xr.open_dataset(fjs[-1]).squeeze(drop=True)

    # initialize output file
    out = xr.Dataset(coords=tmp_0.coords)
    out['time'] = ts  # update time attribute
    out.attrs = tmp_1.attrs
    out.attrs['id'] = code
    out.attrs['time_coverage_start'] = tmp_0.attrs['time_coverage_start']

    # initialize dataset variables
    sh_vs = tmp_0['sst'].shape + (len(ts),)
    dvs = {
        'sst': np.zeros(sh_vs)*np.nan,
        'ssta': np.zeros(sh_vs)*np.nan,
    }

    # read variables
    for c, k in enumerate(fjs):
        xk = xr.open_dataset(k)

        for vn in ['sst', 'ssta']:
            dvs[vn][:,:,c] = xk[vn].values[:]

    # assign variables
    for vn in ['sst', 'ssta']:
        out[vn] = (('lat', 'lon', 'time',), dvs[vn])

    # store output
    mf = op.join(p_store, '{0}.nc'.format(code))
    out.to_netcdf(mf)
    print('Complete. Data stored at: {0}'.format(mf))

    return out

