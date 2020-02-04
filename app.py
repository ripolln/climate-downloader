import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px

import os.path as op
import numpy as np
import pandas as pd
import xarray as xr
import datetime
from datetime import datetime as dt
import pathlib



# TODO: full refactor
l_grid = ['pac_4m', 'pac_10m', 'aus_4m', 'aus_10m', 'glob_24m']

url_catalog = \
'http://data-cbr.csiro.au/thredds/catalog/catch_all/CMAR_CAWCR-Wave_archive/CAWCR_Wave_Hindcast_aggregate/catalog.html'

# TODO: get first and last files from catalog
dt_1 = dt(1979,1,1)
dt_2 = dt(2019,11,1)


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server
app.config.suppress_callback_exceptions = True

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()


# TODO: necesario?
ASSETS_PATH = BASE_PATH.joinpath("assets").resolve()
assets_grid_coords = op.join(ASSETS_PATH, "gridded_coords")


## AUX.

def get_grid_info(sel_grid):
    """
    :param: sel_grid: grid selection.

    :return: selected grid coordinates (pandas.DataFrame) and attributes
    """

    # use xaray
    xx = xr.open_dataset(op.join(assets_grid_coords, '{0}.nc'.format(sel_grid)))

    # lon lat meshgrid and apply mask
    lon, lat = xx.longitude.values[:], xx.latitude.values[:]
    mask = xx.mask.values[:]
    lon_mg, lat_mg = np.meshgrid(lon, lat)
    lon_pts, lat_pts = lon_mg[mask].flatten(), lat_mg[mask].flatten()

    coords = pd.DataFrame({'lon': lon_pts, 'lat': lat_pts})  # to pandas

    # attributes (metadata)
    attrs_filter = ['start_date', 'stop_date', 'date_created', 'product_name']

    attrs = xx.attrs
    [attrs.pop(k,None) for k in attrs_filter]

    return coords, attrs



## DASH COMPONENTS

def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H3("Climate Downloader (*DEMO APP*)"),
            html.H5("CSIRO Wave Hindcast Aggregate"),

            # TODO: make it clickable
            dcc.Location(id='url', refresh=False),
            dcc.Link('Opendap Catalog', href=url_catalog),

            html.Div(
                id="intro",
                children="Explore available CSIRO Wave Hindcast Databases. \
                Select grid, time interval, and points to download. Data \
                attributes are collected from original netCDF4 files.",
            ),
        ],
    )

def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    sw = 350

    return html.Div(
        id="control-card",
        children=[
            html.P("Select Grid"),
            dcc.Dropdown(
                id="grid-select",
                options=[{"label": i, "value": i} for i in l_grid],
                value=l_grid[0],
            ),
            html.Br(),
            html.P("Select Start -> End Time"),
            html.Div(
                dcc.DatePickerRange(
                    id="date-picker-select",
                    start_date = dt_1,
                    end_date = dt_2,
                    min_date_allowed = dt_1,
                    max_date_allowed = dt_2,
                    #initial_visible_month=dt(2014, 1, 1),  # TODO ??
                ),
                className='row',
            ),
            html.Br(),
            html.Br(),
            html.P("Download Points"),
            html.Div(
                id="reset-btn-outer",
                children=html.Button(id="reset-btn", children="Reset", n_clicks=0),
                style={'width': '43%', 'display': 'inline-block'},
            ),
            html.Div(
                id="download-btn-outer",
                children=html.Button(id="download-btn", children="Download", n_clicks=0),
                style={'width': '50%', 'display': 'inline-block'},
            ),
            html.Br(),
            html.Br(),
            html.Div(
                dash_table.DataTable(
                    id='table-points',
                    columns=[{'name':x, 'id':x} for x in ['longitude', 'latitude']],
                    data=[],
                    style_cell={
                        'textAlign': 'left',
                        'maxWidth': 0, 'maxHeight': 0,
                        'overflowY': 'scroll',
                        'font_size': '12px',
                    },
                    row_deletable=True
                ),
            style={'width':sw},
            ),
        ],
    )

def generate_data_map(sel_grid):
    """
    :param: sel_grid: grid selection.

    :return: climate data location world map
    """

    # obtain coords to plot
    grid_coords, _ = get_grid_info(sel_grid)

    # map
    # TODO: acelerar
    fig = px.scatter_mapbox(
        grid_coords,
        lat="lat", lon="lon",
        #hover_name="City", hover_data=["State", "Population"],
        color_discrete_sequence=["red"],
        zoom=2, #height=700
    )
    # traces
    fig.update_traces(
        marker = {
            'size': 5,
            #'opacity':0.7,
        }
    )
    # figure layout
    fig.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ],
            #"opacity": 0.1,
        }
      ]
    )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

def generate_table_metadata(ats):
    """
    :ats: metadata atribute-description dictionary

    :return: DataTable with netCDF4 metadata
    """
    dt = dash_table.DataTable(
        id='table',
        columns=[{'name':x, 'id':x} for x in ['attribute', 'description']],
        data=[{'attribute': k, 'description':ats[k]} for k in ats.keys()],
        style_cell={
            'textAlign': 'left',
            'maxWidth': 0,
            'overflowX': 'scroll',
        },
    )

    return dt


## APP LAYOUT

app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[
                html.Img(src=app.get_asset_url("plotly_logo.png")),
                html.Img(src=app.get_asset_url("logo_bm.png")),
                html.Img(src=app.get_asset_url("logo_go.jpg")),
            ],
        ),

        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
            style={'width':370},
        ),

        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                # griid coordinates map
                html.Div(
                    id="map_card",
                    children=[
                        html.B("Grid Coordinates Map"),
                        html.Hr(),
                        dcc.Graph(id="grid_coords_map"),
                    ],
                ),
                # metadata table 
                html.Div(
                    id="attributes_card",
                    children=[
                        html.B("Opendap netCDF4 files attributes"),
                        html.Hr(),
                        html.Div(id="metadata_table"),   #children=initialize_table()),
                    ],
                ),
            ],
        ),
        html.Div(id='hidden-div', style={'display':'none'}) # null output
    ],
)


## CALLBACKS

@app.callback(
    [
        Output("grid_coords_map", "figure"),
        Output("metadata_table", "children"),
    ],
    [
        Input("grid-select", "value"),
    ],
)
def update_grid_map_metadata(sel_grid):

    # TODO: RESET TABLE POINTS

    # obtain coords to plot and attributes
    grid_coords, attrs = get_grid_info(sel_grid)

    # return grid coords map and table with .nc metadata
    return generate_data_map(sel_grid), generate_table_metadata(attrs)

@app.callback(
    Output('table-points', 'data'),
    [Input('grid_coords_map', 'clickData'), Input('reset-btn', 'n_clicks'),
     Input('grid-select','value')],
    [State('table-points', 'data')]
)
def handle_row(clickData, reset_click, grid_dropdown, rows):

    # Find if reset click 
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id in["reset-btn", "grid-select"]:
            return []

    # add point
    if clickData != None:

        # get input point
        lon_p = clickData['points'][0]['lon']
        lat_p = clickData['points'][0]['lat']

        # append to table 
        if rows == []:
            rows = [{'longitude': lon_p, 'latitude':lat_p}]
        else:
            nr = {'longitude': lon_p, 'latitude': lat_p}
            if not nr in rows:
                rows.append(nr)

    return rows

@app.callback(
    Output('hidden-div', 'children'),
    [Input('table-points', 'data'), Input('download-btn', 'n_clicks'),
     Input('date-picker-select', 'start_date'),
     Input('date-picker-select', 'end_date'),
     Input('grid-select','value')],
)
def download_data(rows, down_click, start_date, end_date, grid_sel):

    # Find if download click 
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "download-btn":

            # TODO connect csiro downloader
            print()
            print('download {0}  -> {1} from {2}'.format(
                start_date, end_date, grid_sel))

            print(rows)
            return []


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True, port='8060', host='127.0.0.1')

