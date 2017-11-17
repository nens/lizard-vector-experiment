from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import View
from graphene_django.views import GraphQLView


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass


class TilesView(View):
    def get(self, request, organisation, tileset_id, z, x, y):
        if not request.user.is_authenticated():
            raise PermissionDenied

        response = HttpResponse()
        response.status_code = 200
        response['X-Accel-Redirect'] = "/tiles/{organisation}/{tileset_id}/{z}/{x}/{y}.pbf".format(
            organisation=organisation,
            tileset_id=tileset_id,
            z=z,
            x=x,
            y=y,
        )

        # All these headers are cleared-out, so nginx can serve it's own,
        # based on served file
        del response['Content-Type']
        del response['Content-Disposition']
        del response['Accept-Ranges']
        del response['Set-Cookie']
        del response['Cache-Control']
        del response['Expires']
        return response


class ClientView(View):
    def get(self, request):

        # The mapStyle dict should be generated based on permissions/auth.
        # Especially the sources/layers.
        # For anonoymous users, only return open data.
        # For auth'd users, check their organisation and tileset permissions...

        baseUrl = 'http://' + str(request.get_host()) + ':8080'

        mapStyle = {
            "version": 8,
            "name": "Lizard Basic",
            "id": "ciwf4zbsv007y2pmt2rspc1dc",
            "owner": "Nelen & Schuurmans",
            "center": [
                4.93791,
                52.49533
            ],
            "zoom": 12.241790506353492,
            "bearing": 0,
            "pitch": 0,
            "sprite": baseUrl + "/static/icons/lizard",
            "glyphs": "https://free.tilehosting.com/fonts/{fontstack}/{range}.pbf?key=sEpG4RWfd5iIz8gs1lbY",
            "sources": {
                "brt_achtergrond_source": {
                    "type": "vector",
                    "url": "http://test.geodata.nationaalgeoregister.nl/vector-viewer/style/tilejson.json"
                },
                "openmaptiles": {
                  "type": "vector",
                  "url": "https://free.tilehosting.com/data/v3.json?key=sEpG4RWfd5iIz8gs1lbY"
                },
                "purmerend-manholes": {
                  "type": "vector",
                  "tiles": [
                    baseUrl + "/vectortiles/purmerend/manholes/{z}/{x}/{y}.pbf"
                  ],
                  "minZoom": 0,
                  "maxZoom": 20
                },
                "purmerend-pipes": {
                  "type": "vector",
                  "tiles": [
                    baseUrl + "/vectortiles/purmerend/pipes/{z}/{x}/{y}.pbf"
                  ],
                  "minZoom": 0,
                  "maxZoom": 20
                },
                "purmerend-pumpstations": {
                  "type": "vector",
                  "tiles": [
                    baseUrl + "/vectortiles/purmerend/pumpstations/{z}/{x}/{y}.pbf"
                  ],
                  "minZoom": 0,
                  "maxZoom": 20
                },
                "almere-manholes": {
                  "type": "vector",
                  "tiles": [
                    baseUrl + "/vectortiles/almere/manholes/{z}/{x}/{y}.pbf"
                  ],
                  "minZoom": 0,
                  "maxZoom": 20
                },
                "almere-pipes": {
                  "type": "vector",
                  "tiles": [
                    baseUrl + "/vectortiles/almere/pipes/{z}/{x}/{y}.pbf"
                  ],
                  "minZoom": 0,
                  "maxZoom": 20
                },
                "almere-pumpstations": {
                  "type": "vector",
                  "tiles": [
                    baseUrl + "/vectortiles/almere/pumpstations/{z}/{x}/{y}.pbf"
                  ],
                  "minZoom": 0,
                  "maxZoom": 20
                },
            },
            "layers": [
                {
                  "id": "background",
                  "type": "background",
                  "paint": {
                    "background-color": "hsl(47, 26%, 88%)"
                  }
                },
                {
                    "id": "registratiefgebiedvlak_leeg",
                    "type": "fill",
                    "source": "brt_achtergrond_source",
                    "source-layer": "registratiefgebiedvlak",
                    "maxzoom": 20,
                    "minzoom": 0,
                    "filter": ["==", "viscode", "18080"],
                    "paint": {
                        "fill-opacity": 1,
                        "fill-color": "#D6F1E9"
                    }
                },
                {
                    "id": "registratiefgebiedvlak",
                    "type": "fill",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "registratiefgebiedvlak",
                    "maxzoom": 20,
                    "minzoom": 0,
                    "filter": ["==", "viscode", "18081"],
                    "paint": {
                        "fill-opacity": 1,
                        "fill-color":"#80BDE3"
                    }
                },
                {
                    "id": "terreinvlak_leeg",
                    "type": "fill",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "terreinvlak",
                    "maxzoom": 20,
                    "minzoom": 6,
                    "filter": ["==", "type_landgebruik", ""],
                    "paint": {
                        "fill-opacity": 1,
                        "fill-color": "#C3DBB5",
                        "fill-outline-color": "#C3DBB5"
                    }
                },
                {
                    "id": "terreinvlak_leeg_z2",
                    "type": "fill",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "terreinvlak",
                    "maxzoom": 20,
                    "minzoom": 10,
                    "filter": ["==", "viscode", "11010"],
                    "paint": {
                        "fill-opacity": 1,
                        "fill-color": "#E2DBE6",
                        "fill-outline-color": "#E2DBE6"
                    }
                },
                {
                    "id": "terreinvlak_bos",
                    "type": "fill",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "terreinvlak",
                    "maxzoom": 20,
                    "minzoom": 6,
                    "filter": ["in", "type_landgebruik", "bos: griend","bos: gemengd bos", "bos: loofbos", "bos: naaldbos"],
                    "paint": {
                        "fill-opacity": 1,
                        "fill-color": "#C3DBB8",
                        "fill-outline-color": "#C3DBB5"
                    }
                },
                {
                    "id": "terreinvlak_heide",
                    "type": "fill",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "terreinvlak",
                    "maxzoom": 20,
                    "minzoom": 8,
                    "filter": ["==", "type_landgebruik", "heide"],
                    "paint": {
                        "fill-opacity": 1,
                        "fill-color": "#FEE5E5",
                        "fill-outline-color": "#FEE5E5"
                    }
                },
                {
                    "id": "terreinvlak_zand",
                    "type": "fill",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "terreinvlak",
                    "maxzoom": 20,
                    "minzoom": 8,
                    "filter": ["==", "type_landgebruik", "zand"],
                    "paint": {
                        "fill-opacity": 1,
                        "fill-color": "#FCF5BB",
                        "fill-outline-color": "#FCF5BB"
                    }
                },
                {
                    "id": "terreinvlak_steen",
                    "type": "fill",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "terreinvlak",
                    "maxzoom": 20,
                    "minzoom": 8,
                    "filter": ["==", "type_landgebruik", "basaltblokken, steenglooiing"],
                    "paint": {
                        "fill-opacity": 1,
                        "fill-color": "#A4A4A4",
                        "fill-outline-color": "#A4A4A4"
                    }
                },
                {
                    "id": "Waterdeelvlak_alles",
                    "type": "fill",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "waterdeelvlak",
                    "maxzoom": 20,
                    "minzoom": 0,
                    "paint": {
                        "fill-opacity": 1,
                        "fill-color": "#80BDE3",
                        "fill-outline-color": "#80BDE3"
                    }
                },
                {
                    "id": "Waterdeellijn",
                    "type": "line",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "waterdeellijn",
                    "maxzoom": 20,
                    "minzoom": 8,
                    "line-cap": "round",
                    "line-join": "miter",
                    "line-miter-limit": 2,
                    "paint": {
                        "line-opacity": 1,
                        "line-color": "#80BDE3",
                        "line-width": 2
                    }
                },
                {
                    "id": "wegdeellijn_snelweg_achter",
                    "type": "line",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "wegdeellijn",
                    "maxzoom": 20,
                    "minzoom": 7,
                    "line-cap": "butt",
                    "line-join": "miter",
                    "line-miter-limit": 2,
                    "filter": ["==", "type_weg", "autosnelweg"],
                    "paint": {
                        "line-opacity": 1,
                        "line-color": "#E69800",
                        "line-width": 4
                    }
                },
                {
                    "id": "wegdeellijn_snelweg_voor",
                    "type": "line",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "wegdeellijn",
                    "maxzoom": 20,
                    "minzoom": 7,
                    "line-cap": "butt",
                    "line-join": "miter",
                    "line-miter-limit": 2,
                    "filter": ["==", "type_weg", "autosnelweg"],
                    "paint": {
                        "line-opacity": 1,
                        "line-color": "#FCEF84",
                        "line-width": 2
                    }
                },
                {
                    "id": "hoofdweg_achter",
                    "type": "line",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "wegdeellijn",
                    "maxzoom": 10,
                    "minzoom": 7,
                    "line-cap": "butt",
                    "line-join": "miter",
                    "line-miter-limit": 2,
                    "filter": ["==", "type_weg", "hoofdweg"],
                    "paint": {
                        "line-opacity": 1,
                        "line-color": "#D2D0CD",
                        "line-width": 2
                    }
                },
                {
                    "id": "hoofdweg_voor",
                    "type": "line",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "wegdeellijn",
                    "maxzoom": 10,
                    "minzoom": 7,
                    "line-cap": "butt",
                    "line-join": "miter",
                    "line-miter-limit": 2,
                    "filter": ["==", "type_weg", "hoofdweg"],
                    "paint": {
                        "line-opacity": 1,
                        "line-color": "#FBEE84",
                        "line-width": 1
                    }
                },
                {
                    "id": "hoofdweg_achter_z2",
                    "type": "line",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "wegdeellijn",
                    "maxzoom": 20,
                    "minzoom": 11,
                    "line-cap": "butt",
                    "line-join": "miter",
                    "line-miter-limit": 2,
                    "filter": ["==", "type_weg", "hoofdweg"],
                    "paint": {
                        "line-opacity": 1,
                        "line-color": "#D2D0CD",
                        "line-width": 6
                    }
                },
                {
                    "id": "hoofdweg_voor_z2",
                    "type": "line",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "wegdeellijn",
                    "maxzoom": 20,
                    "minzoom": 11,
                    "line-cap": "butt",
                    "line-join": "miter",
                    "line-miter-limit": 2,
                    "filter": ["==", "type_weg", "hoofdweg"],
                    "paint": {
                        "line-opacity": 1,
                        "line-color": "#FBEE84",
                        "line-width": 3
                    }
                },
                {
                    "id": "Wegdeellijn_mid_a",
                    "type": "line",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "wegdeellijn",
                    "maxzoom": 20,
                    "minzoom": 10,
                    "line-cap": "butt",
                    "line-join": "miter",
                    "line-miter-limit": 2,
                    "filter": ["==", "type_weg", "regionale weg"],
                    "paint": {
                        "line-opacity": 1,
                        "line-color": "#D2D0CD",
                        "line-width": 4
                    }
                },
                {
                    "id": "Wegdeellijn_mid_v",
                    "type": "line",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "wegdeellijn",
                    "maxzoom": 20,
                    "minzoom": 8,
                    "line-cap": "butt",
                    "line-join": "miter",
                    "line-miter-limit": 2,
                    "filter": ["==", "type_weg", "regionale weg"],
                    "paint": {
                        "line-opacity": 1,
                        "line-color": "#FDFCBD",
                        "line-width": 2
                    }
                },
                {
                    "id": "Wegdeellijn_lokaal_enkel",
                    "type": "line",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "wegdeellijn",
                    "maxzoom": 20,
                    "minzoom": 9,
                    "line-cap": "butt",
                    "line-join": "miter",
                    "line-miter-limit": 2,
                    "filter": ["in", "type_weg","lokale weg"],
                    "paint": {
                        "line-opacity": 1,
                        "line-color": "#D8D4D4",
                        "line-width": 1
                    }
                },
                {
                    "id": "Wegdeellijn_lokaal_achter",
                    "type": "line",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "wegdeellijn",
                    "maxzoom": 20,
                    "minzoom": 11,
                    "line-cap": "butt",
                    "line-join": "miter",
                    "line-miter-limit": 2,
                    "filter": ["in", "type_weg","lokale weg"],
                    "paint": {
                        "line-opacity": 1,
                        "line-color": "#D8D4D4",
                        "line-width": 3
                    }
                },
                {
                    "id": "Wegdeellijn_lokaal_voor",
                    "type": "line",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "wegdeellijn",
                    "maxzoom": 20,
                    "minzoom": 11,
                    "line-cap": "butt",
                    "line-join": "miter",
                    "line-miter-limit": 2,
                    "filter": ["in", "type_weg","lokale weg"],
                    "paint": {
                        "line-opacity": 1,
                        "line-color": "#FEFEFE",
                        "line-width": 1.5
                    }
                },
                {
                    "id": "Wegdeellijn_klein_achter",
                    "type": "line",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "wegdeellijn",
                    "maxzoom": 20,
                    "minzoom": 14,
                    "line-cap": "butt",
                    "line-join": "miter",
                    "line-miter-limit": 2,
                    "filter": ["in", "type_weg", "straat", "veerverbinding"],
                    "paint": {
                        "line-opacity": 1,
                        "line-color": "#FEFEFE",
                        "line-width": 1.5
                    }
                },
                        {
                    "id": "Wegdeellijn_klein_voor",
                    "type": "line",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "wegdeellijn",
                    "maxzoom": 20,
                    "minzoom": 14,
                    "line-cap": "butt",
                    "line-join": "miter",
                    "line-miter-limit": 2,
                    "filter": ["in", "type_weg", "straat", "overig", "veerverbinding"],
                    "paint": {
                        "line-opacity": 1,
                        "line-color": "#FFFFFF",
                        "line-width": 1
                    }
                },
                {
                    "id": "Gebouwvlak",
                    "type": "fill",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "gebouwvlak",
                    "maxzoom": 20,
                    "minzoom": 8,
                    "paint": {
                        "fill-opacity": 1,
                        "fill-color": "#D1D1D1",
                        "fill-outline-color": "#D1D1D1"
                    }
                },
                {
                    "id": "spoorbaanlijn_achter",
                    "type": "line",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "spoorbaanlijn",
                    "maxzoom": 20,
                    "minzoom": 12,
                    "line-cap": "round",
                    "line-join": "miter",
                    "line-miter-limit": 2,
                    "paint": {
                        "line-opacity": 1,
                        "line-color": "#A4A4A4",
                        "line-width": 3
                    }
                },
                {
                    "id": "spoorbaanlijn_voor",
                    "type": "line",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "spoorbaanlijn",
                    "maxzoom": 20,
                    "minzoom": 12,
                    "line-cap": "round",
                    "line-join": "miter",
                    "line-miter-limit": 2,
                    "paint": {
                        "line-opacity": 1,
                        "line-color": "#FFFFFF",
                        "line-width": 1.5,
                        "line-dasharray": [10.0, 10.0]
                    }
                },
                {
                    "id": "straatnamen",
                    "type": "symbol",
                    "source": "brt_achtergrond_source",
                    "source-layer" : "wegdeellijn",
                    "maxzoom": 20,
                    "minzoom": 10,
                    "line-cap": "butt",
                    "line-join": "miter",
                    "line-miter-limit": 2,
                    "symbol-placement": "line",
                    "symbol-spacing" : 2,
                    "text-field":"nederlandse_straatnaam",
                    "text-font": "Open Sans Regular",
                    "text-size":12,
                    "text-max-widht": 10,
                    "text-line-height": 1.5,
                    "paint": {
                        "text-opacity": 1,
                        "text-color": "rgb(0,0,0)",
                        "text-halo-color": "rgb(0,0,0)",
                        "text-halo-width": 2,
                        "text-halo-blur":2
                    }
                },
                {
                  "id": "purmerend-pipes",
                  "type": "line",
                  "source": "purmerend-pipes",
                  "source-layer": "pipespurmerend",
                  "minzoom": 14,
                  "layout": {
                    "line-cap": "round",
                    "line-join": "bevel"
                  },
                  "paint": {
                      "line-width": 5,
                      "line-color": {
                          "property": "type",
                          "type": "categorical",
                          "default": "#007FB5",
                          "stops": [
                              ["00", "#007FB5"],
                              ["01", "#BA6337"],
                              ["02", "#C6312D"]
                          ]
                      }
                  }
                },
                {
                  "id": "purmerend-manholes",
                  "type": "symbol",
                  "source": "purmerend-manholes",
                  "source-layer": "manholespurmerend",
                  "minzoom": 14,
                  "maxzoom": 24,
                  "layout": {
                    "icon-image": "manhole",
                    "icon-size": 1,
                    "text-field": ""
                  },
                  "paint": {}
                },
                {
                  "id": "purmerend-pumpstations",
                  "type": "symbol",
                  "source": "purmerend-pumpstations",
                  "source-layer": "pumpstationspurmerend",
                  "minzoom": 14,
                  "layout": {
                    "symbol-placement": "point",
                    "icon-image": "pumpstation-diesel"
                  },
                  "paint": {}
                },
                {
                  "id": "almere-pipes",
                  "type": "line",
                  "source": "almere-pipes",
                  "source-layer": "pipesalmere",
                  "minzoom": 14,
                  "layout": {
                    "line-cap": "round",
                    "line-join": "bevel"
                  },
                  "paint": {
                      "line-width": 5,
                      "line-color": {
                          "property": "type",
                          "type": "categorical",
                          "default": "#007FB5",
                          "stops": [
                              ["00", "#007FB5"],
                              ["01", "#BA6337"],
                              ["02", "#C6312D"]
                          ]
                      }
                  }
                },
                {
                  "id": "almere-manholes",
                  "type": "symbol",
                  "source": "almere-manholes",
                  "source-layer": "manholesalmere",
                  "minzoom": 14,
                  "maxzoom": 24,
                  "layout": {
                    "icon-image": "manhole",
                    "icon-size": 1,
                    "text-field": ""
                  }
                },
                {
                  "id": "almere-pumpstations",
                  "type": "symbol",
                  "source": "almere-pumpstations",
                  "source-layer": "pumpstationsalmere",
                  "minzoom": 14,
                  "layout": {
                    "symbol-placement": "point",
                    "icon-image": "pumpstation-diesel"
                  }
                },
                {
                  "id": "road_major_label",
                  "type": "symbol",
                  "source": "openmaptiles",
                  "source-layer": "transportation_name",
                  "filter": [
                    "==",
                    "$type",
                    "LineString"
                  ],
                  "layout": {
                    "symbol-placement": "line",
                    "text-field": "{name}",
                    "text-font": [
                      "Klokantech Noto Sans Regular",
                      "Klokantech Noto Sans CJK Regular"
                    ],
                    "text-transform": "uppercase",
                    "text-letter-spacing": 0.1,
                    "text-size": {
                      "base": 1.4,
                      "stops": [
                        [
                          10,
                          8
                        ],
                        [
                          20,
                          14
                        ]
                      ]
                    },
                    "text-rotation-alignment": "map"
                  },
                  "paint": {
                    "text-color": "#000",
                    "text-halo-color": "hsl(0, 0%, 100%)",
                    "text-halo-width": 2
                  }
                },
            ],
        }
        return HttpResponse(render_to_string('client.html',
                                             {'mapStyle': mapStyle}))
