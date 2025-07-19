"""Main module."""

import ipyleaflet

class Map(ipyleaflet.Map):
    """This is the map class that inherits from ipyleaflet.Map.

    Args:
        ipyleaflet (Map): The ipyleaflet map class.
    """

    def __init__(self, center=[20, 0], zoom=2, **kwargs):
        """Initialize the map.

        Args:
            center (list, optional): Set the center of the map. Defaults to [20, 0].
            zoom (int, optional): Set the zoom level of the map. Defaults to 2.
        """

        super().__init__(center=center, zoom=zoom, **kwargs)

    def add_layer(self, layer) -> None:
        existing_layer = self.find_layer(layer.name)
        if existing_layer is not None:
            self.remove_layer(existing_layer)
        super().add(layer)

    def add_layer_control(self, position="topright") -> None:
        self.add(ipyleaflet.LayersControl(position=position))

    def add_basemap(self, basemap="HYBRID", show=True, **kwargs) -> None:
        """Adds a basemap layer to the map.

        Args:
            basemap (str or xyzservices.TileProvider, optional): The basemap to add. Can be a string
                representing a common basemap ("ROADMAP", "SATELLITE", "TERRAIN", "HYBRID") or a
                xyzservices.TileProvider object. Defaults to "HYBRID".
            show (bool, optional): Whether to show the basemap layer upon adding. Defaults to True.
            **kwargs: Additional keyword arguments to pass to the basemap layer.

        Raises:
            ValueError: If the basemap is not recognized or cannot be added.

        Returns:
            None
        """
        import xyzservices

        try:
            layer_names = self.get_layer_names()

            map_dict = {
                "ROADMAP": "Google Maps",
                "SATELLITE": "Google Satellite",
                "TERRAIN": "Google Terrain",
                "HYBRID": "Google Hybrid",
            }

            if isinstance(basemap, str):
                if basemap.upper() in map_dict:
                    layer = common.get_google_map(basemap.upper(), **kwargs)
                    layer.visible = show
                    self.add(layer)
                    return

            if isinstance(basemap, xyzservices.TileProvider):
                name = basemap.name
                url = basemap.build_url()
                attribution = basemap.attribution
                if "max_zoom" in basemap.keys():
                    max_zoom = basemap["max_zoom"]
                else:
                    max_zoom = 22
                layer = ipyleaflet.TileLayer(
                    url=url,
                    name=name,
                    max_zoom=max_zoom,
                    attribution=attribution,
                    visible=show,
                    **kwargs,
                )
                self.add(layer)
                common.arc_add_layer(url, name)
            elif basemap in basemaps and basemaps[basemap].name not in layer_names:
                self.add(basemap)
                self.layers[-1].visible = show
                for param in kwargs:
                    setattr(self.layers[-1], param, kwargs[param])
                common.arc_add_layer(basemaps[basemap].url, basemap)
            elif basemap in basemaps and basemaps[basemap].name in layer_names:
                print(f"{basemap} has been already added before.")
            else:
                print(
                    "Basemap can only be one of the following:\n  {}".format(
                        "\n  ".join(basemaps.keys())
                    )
                )

        except Exception as e:
            raise ValueError(
                "Basemap can only be one of the following:\n  {}".format(
                    "\n  ".join(basemaps.keys())
                )
            )

    def add_tile_layer(
        self,
        url,
        name,
        attribution,
        opacity=1.0,
        shown=True,
        layer_index=None,
        **kwargs,
    ) -> None:
        if "max_zoom" not in kwargs:
            kwargs["max_zoom"] = 30
        if "max_native_zoom" not in kwargs:
            kwargs["max_native_zoom"] = 30
        try:
            tile_layer = ipyleaflet.TileLayer(
                url=url,
                name=name,
                attribution=attribution,
                opacity=opacity,
                visible=shown,
                **kwargs,
            )
            self.add(tile_layer, index=layer_index)

            common.arc_add_layer(url, name, shown, opacity)

        except Exception as e:
            print("Failed to add the specified TileLayer.")
            raise Exception(e)

    def add_vector_tile(
        self,
        url,
        styles: Optional[dict] = {},
        layer_name: Optional[str] = "Vector Tile",
        **kwargs,
    ) -> None:
        if "vector_tile_layer_styles" in kwargs:
            styles = kwargs["vector_tile_layer_styles"]
            del kwargs["vector_tile_layer_styles"]
        try:
            vector_tile_layer = ipyleaflet.VectorTileLayer(
                url=url,
                vector_tile_layer_styles=styles,
                **kwargs,
            )
            vector_tile_layer.name = layer_name
            self.add(vector_tile_layer)

        except Exception as e:
            print("Failed to add the specified VectorTileLayer.")
            raise Exception(e)

    add_vector_tile_layer = add_vector_tile

    def add_pmtiles(
        self,
        url,
        style=None,
        name="PMTiles",
        show=True,
        zoom_to_layer=True,
        **kwargs,
    ) -> None:
      
        try:
            if "sources" in kwargs:
                del kwargs["sources"]

            if "version" in kwargs:
                del kwargs["version"]

            if style is None:
                style = common.pmtiles_style(url)

            layer = ipyleaflet.PMTilesLayer(
                url=url,
                style=style,
                name=name,
                visible=show,
                **kwargs,
            )
            self.add(layer)

            if zoom_to_layer:
                metadata = common.pmtiles_metadata(url)
                bounds = metadata["bounds"]
                self.zoom_to_bounds(bounds)
        except Exception as e:
            print(e)


        