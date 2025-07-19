"""Main module."""


import ipyleaflet


class Map(ipyleaflet.Map):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_control(ipyleaflet.LayersControl())

    def add_raster(self, raster_path):
        """Add a raster to the map."""
        raster = ipyleaflet.TileLayer(
            url=raster_path,
            name=raster_path,
            attribution="",
        )
        self.add_layer(raster)

        