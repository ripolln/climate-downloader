# Climate Downloader

Climate data download toolbox.

## Main contents

- [csiro](./climate_downloader/csiro.py): Download csiro gridded and spec data from <http://data-cbr.csiro.au/>. 
  Can use a list of points [(lon1, lat1), ... (lonN, latN)] or a grid area limits (lon1, lat1, lon2, lat2) 
- [mjo](./climate_downloader/mjo.py): Download Madden Julian Oscillation from <http://www.bom.gov.au/climate/mjo/> 
- [noaa](./climate_downloader/noaa.py): Download IBTrACS (International Best Track Archive for Climate Stewardship) storms from <ftp://eclipse.ncdc.noaa.gov/pub/ibtracs>

## Documentation


## Install
- - -

The source code is currently hosted on GitLab at: [climate downloader](https://gitlab.com/geoocean/bluemath/climate-downloader)


### Install from sources

Install requirements. Navigate to the base root of [climate downloader](./) and execute:

```
   pip install -r requirements.txt

```

Then install climate downloader:

```
   python setup.py install

   # run pytest integration
   python setup.py test
```

### GEBCO and GSHHG databases

GEBCO global bathymetric database can be downloaded from [gebco.net](https://www.gebco.net/data_and_products/gridded_bathymetry_data/)

GSHHG global shorelines database can be downloaded from [noaa.gov](https://www.ngdc.noaa.gov/mgg/shorelines/)


## Examples:
- - -

### Download a set of points and an area from CSIRO database

```
import os
import os.path as op

# csiro module 
from climate_downloader import csiro

# area
lon1 = 168
lat1 = 8
lon2 = 170
lat2 = 10

# download area spec data
p_nc_spec = op.join(os.getcwd(), 'spec_area')
csiro.download_spec_area(p_nc_spec, lon1, lat1, lon2, lat2)

# download area gridded data
gc = 'glob_24m'
p_nc_grid = op.join(os.getcwd(), 'gridded_area')
csiro.download_gridded_area(p_nc_grid, lon1, lat1, lon2, lat2, gc)


# point list (lon, lat)
l_points = [(167.2, 9.6), (168, 9.2), (167.2, 8.4), (166.4, 9.2)]

# download point spec data
p_nc_spec = op.join(os.getcwd(), 'spec_points')
csiro.download_spec(p_nc_spec, l_points)

#download point gridded data
gc = 'glob_24m'
p_nc_grid = op.join(os.getcwd(), 'gridded_points')
csiro.download_gridded(p_nc_grid, l_points, gc)
```

### Download Madden-Julian Oscillation 

```
import os
import os.path as op

# mjo downloader
from climate_downloader import mjo

# Download MJO to .nc file 
y1 = '1979-01-01'
p_nc_mjo = op.join(os.getcwd(), 'mjo.nc')
mjo.download(p_nc_mjo, init_year=y1)
```

### Download IBTraCS 

```
import os
import os.path as op

# noaa downloader
from climate_downloader import noaa

# Download Allstorms.ibtracks_wmo to .nc file 
p_nc_ib = op.join(os.getcwd(), 'allstorms.ibtracks_wmo.nc')
noaa.download_ibtracs_all(p_nc_ib)
```


## Apps:
- - -

Currently an incomplete conceptual demonstration web app of this toolbox usage can be found at [herokuapp](https://climate-downloader.herokuapp.com/)


## Contributors:

Nicolas Ripoll Cabarga (ripolln@unican.es)


## Thanks also to:


## License

This project is licensed under the MIT License - see the [license](./LICENSE.txt) file for details

