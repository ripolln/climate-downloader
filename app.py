import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.express as px
import plotly.graph_objects as go

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
    external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"],
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

def dropdown_grid():
    """
    :return: A dcc.Dropdown containing controls for chosing a grid.
    """

    return dcc.Dropdown(
        id="grid-select",
        options=[{"label": i, "value": i} for i in l_grid],
        value=l_grid[0],
    )


tabs_div_h = '225px'

def input_point_list():
    """
    :return: A html.Div containing controls for point list selection
    """

    return html.Div(
        id='input-point-list',
        children=[
            html.Plaintext(
                'Lon',
                style={'width': '19%', 'display': 'inline-block'},
            ),

            dcc.Input(
                id='input-point-lon',
                type = 'number',
                placeholder = '0.00',
                style={'width': '30%', 'display': 'inline-block'},
            ),

            html.Plaintext(
                'Lat',
                style={'width': '19%', 'display': 'inline-block',
                       'margin-left':'2%'},
            ),

            dcc.Input(
                id='input-point-lat',
                type = 'number',
                placeholder = '0.00',
                style={'width': '30%', 'display': 'inline-block'},
            ),

            dash_table.DataTable(
                id='input-point-table',
                columns=[{'name':x, 'id':x} for x in ['longitude', 'latitude']],
                data=[],
                style_cell={
                    'textAlign': 'left',
                    'maxWidth': 0, 'maxHeight': 0,
                    'overflowY': 'scroll',
                    'font_size': '12px',
                },
                style_table={
                    'height': '160px',
                    'overflowY': 'scroll'
                },
                row_deletable=True,
            ),
        ],
        style={
            'height': tabs_div_h,
        },
    )

def input_bounding_box():
    """
    :return: A html.Div containing controls for bounding box selection
    """

    return html.Div(
        id='input-bounding-box',
        children = [
            html.Plaintext(
                'N',
                style={
                    'width': '14%', 'display': 'inline-block',
                    'margin-left':'30%', 'margin-top':'10%',
                },
            ),

            dcc.Input(
                id='input-bb-N',
                type = 'number',
                placeholder = '0.00',
                style={
                    'width': '30%', 'display': 'inline-block',
                    'margin-right':'25%'
                },
            ),

            html.Plaintext(
                'W',
                style={
                    'width': '14%', 'display': 'inline-block',
                    'margin-left': '5%'
                },
            ),

            dcc.Input(
                id='input-bb-W',
                type = 'number',
                placeholder = '0.00',
                style={'width': '30%', 'display': 'inline-block'},
            ),

            html.Plaintext(
                'E',
                style={
                    'width': '14%', 'display': 'inline-block',
                    'margin-left': '7%',
                },
            ),

            dcc.Input(
                id='input-bb-E',
                type = 'number',
                placeholder = '0.00',
                style={'width': '30%', 'display': 'inline-block'},
            ),

            html.Plaintext(
                'S',
                style={
                    'width': '14%', 'display': 'inline-block',
                    'margin-left':'30%'
                },
            ),

            dcc.Input(
                id='input-bb-S',
                type = 'number',
                placeholder = '0.00',
                style={'width': '30%', 'display': 'inline-block'},
            ),

        ],
        style={
            'height': tabs_div_h,
        },
    )

def tabs_subset_sel():
    """
    :return: A html.Div containing controls for chosing a subset (points/bbox).
    """

    return html.Div(
        children=[
            dcc.Tabs(
                id='tabs-subset-select',
                value='tab-1',
                children = [
                    dcc.Tab(
                        label = 'Point List',
                        value = 'tab-1',
                        children = [input_point_list()],
                    ),
                    dcc.Tab(
                        label = 'Bounding Box',
                        value = 'tab-2',
                        children = [input_bounding_box()],
                    ),
                ]
            ),
            dcc.ConfirmDialogProvider(
                id='reset-btn',
                children = [
                    html.Button(
                        children="Reset", n_clicks=0,
                        style={'width': '50%', 'display': 'inline-block',
                            'margin-left':'50%'},
                    ),
                ],
                message = 'Reset subset selection?',
            ),
        ],
    )

def date_picker():
    """
    :return: A html.Div containing a date range picker
    """

    return html.Div(
        dcc.DatePickerRange(
            id="date-picker-select",
            start_date = dt_1,
            end_date = dt_2,
            min_date_allowed = dt_1,
            max_date_allowed = dt_2,
            style={'width': '100%', 'display': 'inline-block'},
        ),
    )

def download_menu():
    """
    :return: A html.Div containing download menu
    """

    return html.Div(
        children = [
            dcc.Input(
                id='input-download-folder',
                placeholder = './climate_downloader/',
                style={'width': '100%' },
            ),
            dcc.ConfirmDialogProvider(
                id="download-btn",
                children = [
                    html.Button(
                        children="Download", n_clicks=0,
                        style={
                            'width': '50%', 'display': 'inline-block',
                            'margin-left': '50%',
                        },
                    ),
                ],
            ),
        ],
    )


def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """

    return html.Div(
        id="control-card",
        children=[
            html.P("1. Select Hindcast Grid"),
            dropdown_grid(),
            html.Br(),

            html.P("2. Select Points / Bounding Box"),
            tabs_subset_sel(),
            html.Br(),

            html.P("3. Select Timi Limits"),
            date_picker(),
            html.Br(),

            html.P("4. Download Data"),
            download_menu(),
            html.Br(),
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
    fig = go.Figure(data=go.Scattermapbox(
        lon = grid_coords['lon'].values,
        lat = grid_coords['lat'].values,
        mode = 'markers',
        marker = dict(
            color='red',
            size=5,
        ),
        #selected = dict(
        #    marker={'color':'yellow'},
        #),
    )
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

def top_banner():
    """
    :return: A Div containing dashboard title & descriptions.
    """

    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Img(src=app.get_asset_url("plotly_logo.png")),
            html.Img(src=app.get_asset_url("logo_bm.png")),
            html.Img(src=app.get_asset_url("logo_go.jpg")),
            html.H3("Climate Downloader (*INCOMPLETE DEMO APP*)"),
        ],
    )

## APP LAYOUT

app.layout = html.Div(
    id="app-container",
    children=[
        # Top banner
        top_banner(),

        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), generate_control_card()],
            #+ [
            #    html.Div(
            #        ["initial child"], id="output-clientside", style={"display": "none"}
            #    )
            #],
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
                        html.Div(id="metadata_table"),
                    ],
                ),
            ],
        ),
        html.Div(id='hidden-div', style={'display':'none'}), # null output
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
    Output('input-point-table', 'data'),
    [Input('grid_coords_map', 'clickData'), Input('reset-btn', 'submit_n_clicks'),
     Input('grid-select','value')],
    [State('input-point-table', 'data')]
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
    [Output('input-bb-N', 'value'), Output('input-bb-S', 'value'),
     Output('input-bb-W', 'value'), Output('input-bb-E', 'value')],
    [Input('grid_coords_map', 'selectedData'), Input('reset-btn', 'submit_n_clicks')])
def display_bbox_data(selectedData, reset_click):
    lon_W, lon_E = 0, 0
    lat_S, lat_N = 0, 0

    # Find if reset click 
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id in ["reset-btn", "grid-select"]:
            return [lat_N, lat_S, lon_W, lon_E]

    if selectedData != None:
        sdata = selectedData['range']['mapbox']
        lons = [sdata[0][0], sdata[1][0]]
        lats = [sdata[0][1], sdata[1][1]]
        lon_W, lon_E = np.min(lons), np.max(lons)
        lat_S, lat_N = np.min(lats), np.max(lats)

    return [lat_N, lat_S, lon_W, lon_E]



@app.callback(
    Output('hidden-div', 'children'),
    [Input('download-btn', 'submit_n_clicks'),
     Input('tabs-subset-select','value'),
     Input('input-point-table', 'data'),
     Input('input-bb-N', 'value'), Input('input-bb-S', 'value'),
     Input('input-bb-W', 'value'), Input('input-bb-E', 'value'),
     Input('date-picker-select', 'start_date'),
     Input('date-picker-select', 'end_date'),
     Input('grid-select','value')],
)
def download_data(
    down_click, tab_val,
    points_rows,
    bbox_N, bbox_S, bbox_W, bbox_E,
    start_date, end_date, grid_sel):

    # Find if download click 
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "download-btn":

            # TODO connect csiro downloader
            if tab_val == 'tab-1':
                print('Point List')
                print(points_rows)
            elif tab_val == 'tab-2':
                print('Bounding Box')
                print(bbox_N, bbox_S, bbox_W, bbox_E)

            print()
            print('time: {0}  -> {1}        grid: {2}'.format(
                start_date, end_date, grid_sel))

            return []


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True, port='8060', host='127.0.0.1')

