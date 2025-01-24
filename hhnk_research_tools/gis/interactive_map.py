"""
Create some basis interactive map from geodataframe,

Author: Wouter van Esse
Date: 24 - 01 - 2025

"""

# %%
import branca.colormap as cm
import folium


def create_interactive_map(
    gdf,
    datacolumn: str,
    colormap_name: str = "plasma",
    colormap_steps: int = None,
    output_path: str = None,
    title: str = "Title",
    legend_label: str = "Label",
    quantiles: list = None,
    tooltip_columns: list[str] = None,
    tooltip_aliases: list[str] = None,
    show: bool = True,
):
    """Create basic interactive map based on one numeric column in a geodataframe.

    See https://python-visualization.github.io/folium/latest/advanced_guide/colormaps.html for more options

    Parameters
    ----

    gdf : pandas GeoDataFrame
        pandas GeoDataFrame containing polygon geometry and data column <column_name>
    datacolumn : str
        Name of the column containing data for visualization
    colormap_name : str
        Name of the colormap
        Use 'cm.linear' to see available colormaps
    colormap_steps : int
        Number of steps to split the colormap, not sure this works over 5 steps
        If None colormap is linear
    output_path : str,
        Output location including map name and extension '.html'
    title : str,
        Map title
    legend_label : str,
        Legend label
    quantiles : list
        Specify quantiles for non-linear colormap, i.e. [0, 0.5, 0.8, 1] or expelling
        outliers i.e. [0.05, 0.5, 0.8, 0.95]
    tooltip_columns : list[str]
        List of column names to appear in tooltip
    tooltip_aliases : list[str]
        List of column aliases to be used in tooltip
    show : bool = True
        Return figure as output of function

    Remarks
    ----
    * Removes geometries when data column equals nan
    * Rounds values in datacolumn to 2 decimals in tooltip

    ----

    """
    # filter nan values
    gdf.dropna(subset=[datacolumn], inplace=True)

    # round values
    gdf = gdf.round(2)

    # get min max range for colormap
    data_min = gdf[datacolumn].min()
    data_max = gdf[datacolumn].max()

    # Use getattr to dynamically access the colormap
    colormap = getattr(cm.linear, colormap_name)
    colormap = colormap.scale(data_min, data_max)

    # Convert colormap to quantiles
    if isinstance(quantiles, list):
        colormap = colormap.to_step(
            data=gdf[datacolumn],
            quantiles=quantiles,
        )

    # Convert colormaps to steps
    if isinstance(colormap_steps, int):
        colormap = colormap.to_step(colormap_steps)

    # Handle tooltip settings
    if isinstance(tooltip_columns, list):
        gdf = gdf[["geometry"] + tooltip_columns]
        fields = tooltip_columns
    else:
        gdf = gdf[["geometry", datacolumn]]
        fields = [datacolumn]

    if isinstance(tooltip_aliases, list):
        aliases = tooltip_aliases
    else:
        aliases = [legend_label]

    # Create the map
    # background maps at: https://leaflet-extras.github.io/leaflet-providers/preview/
    m = folium.Map(location=[52.8, 4.9], tiles="nlmaps.luchtfoto", zoom_start=10)

    # Add the water layer
    folium.TileLayer("nlmaps.water").add_to(m)

    # Add the GeoJson layer Gemeente
    folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            "fillColor": colormap(feature["properties"][datacolumn]),
            "color": "white",
            "fillOpacity": 0.8,
            "weight": 1,
        },
        name=legend_label,
        tooltip=folium.GeoJsonTooltip(
            fields=fields,
            aliases=aliases,
        ),
    ).add_to(m)

    # Add the scale bar
    colormap.caption = legend_label
    m.add_child(colormap)

    # Turn on layercontrol
    folium.LayerControl().add_to(m)

    # Add title to map
    title_html = f'<h1 style="position:absolute;z-index:100000;bottom:1vw;background-color:rgba(255, 255, 255, 0.8);padding:10px;border-radius:5px;" >{title}</h1>'
    m.get_root().html.add_child(folium.Element(title_html))

    if isinstance(output_path, str):
        # Save the map
        m.save(output_path)

    if show:
        return m


# %% Code test
import geopandas as gpd

gdf = gpd.read_file(
    r"\\srv57d1\geo_info\02_Werkplaatsen\06_HYD\Projecten\HKC24001 Verantwoord investeren in stedelijk gebied\data_actueel\02_output\gemeente_statistiek.gpkg"
)
datacolumn = "dem_mean"
colormap_name = "viridis"
output_path = None
title = "Maaiveldhoogte"
legend_label = "Hoogte [m NAP]"
tooltip_columns = ["gemeentenaam", "dem_mean"]
tooltip_aliases = ["Gemeente", "Hoogte"]

v = create_interactive_map(
    gdf=gdf,
    datacolumn=datacolumn,
    colormap_name=colormap_name,
    output_path=output_path,
    title=title,
    legend_label=legend_label,
    quantiles=[0, 0.5, 0.8, 1],
    tooltip_columns=tooltip_columns,
    tooltip_aliases=tooltip_aliases,
)

# %%
v
