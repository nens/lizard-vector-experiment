# LIZARD-VECTOR

## Description

This is a testbed for new visualisation techniques to be considered for new
versions of Lizard using Vector Tiles.

### Lizard 6: PNG and UTFGrid

The current version, Lizard 6, uses dynamically rendered and cached PNG tiles
with a UTFGrid layer on top for interactivity.

This works well and has the advantage of being lightweight to render in the
browser, as it's just bitmap data and some text making up a click-grid.

But UTFGrid has its limitations. For example, there can only be one UTFGrid
at a time. It's not possible to dynamically toggle layers.

Another limitation is that it's impossible to style map features dynamically based
on data.

Technically, serving these two grids dynamically requires lots of moving parts.
For example, the grids need to be generated based on permissions by TileStache.
They need to be cached by Redis. They need server-side styling using CartoCSS which generates Mapnik's XML format.

Another downside is that each tile needs to be transferred twice: PNG and Grid.
This doubles the number of HTTP requests.

### Exploring: Vector tiles

Vector tiles are another way of rendering geo data in the browser.

Employed properly, they can have several advantages:

- Styling of the map happens in the client and can be data-driven.
- Fractional zooming, rotation and tilting.
- Lightweight - only the geodata is transfered, not the rendered bitmaps/grids.
- Layers can be displayed independently.
- Because of their flexibility and small filesize, pre-seeding is possible.



# Intentions

This project intends to:

- Enable authn/authz for tiles per organisation
- Dynamically generate the map style object
- Enable on-disk pre-seeding of tiles


A python script will dynamically generate the sources and the layers associated with these sources.

Sources are vector endpoints. Some are open/public, others require authentication and belonging to an organisation.


On load, the front-end will ask for a dynamically generated map-style file.
"Dynamic" here means it's generated based on the level of authorisation of the user.

- If it's an anonymous user, the map style file contains only 'open data' sources.

- If the user is authenticated, sources{} will contain the data-sources that he/she is entitled to view.
  (By default, this means data which belongs to the organisation(s) this user is a member of)

The layers[] array will also be generated server-side.
Layers depend on sources, and thus a layer will only be added if it has a corresponding source.


Once the client receives this dynamic configuration object, it can begin requesting vector tiles for its sources.


Tiles such as `/vectortiles/{organisation-id}/{tile-label}/{z}/{x}/{y}.pbf` are being passed through Nginx.
Nginx will check if the user has permission to request tiles for {organisation-id} and {tile-label}.


This is done via the Nginx X-Accel-Redirect directive.

Then, if the tile exists, it will be sent to the client. This is done using the try_files Nginx directive.

If the tile does not exist, the 'tile seeder' will be asked to produce the tile on-the-fly.

The 'tile seeder' is a Django app which uses mercantile and a PG connection to request the data and write it an MVT tile
using ST_AsMVT(). This tile is then immediately sent over the wire.

Note: This tile seeder should generate the tiles every night or so.


Refs:

- https://www.zimmi.cz/posts/2017/serving-mapbox-vector-tiles-with-postgis-nginx-and-python-backend/
- See https://postgis.net/docs/ST_AsSVG.html for creating SVG tiles




### Combination with D3

It's still perfectly possible to draw SVG on top of the map canvas. D3.js can be used for this purpose, as can SVG wrapped in React components.

This is an example:
- http://dev.jorditost.com/mapboxgl-d3-playground/05-toggle-views.html




### API: GraphQL and REST

In addition to vector tiles, this project also explores the use of GraphQL as a second API that's more geared towards client-side use. The idea is that a GraphQL endpoint will coexist with Django REST Framework.

This project uses Django-Graphene for handling GraphQL.


# Installation

This project uses Docker and docker-compose, so make sure to have those up and running.

In the root of this project, execute:

```bash
$ docker-compose build
```

Or to build and run in one go, execute:

```bash
$ docker-compose up
```

This will build three Docker containers:

- Nginx: Static file and tile serving, and proxies to the Django application. See 'nginx/'.
- PostgreSQL: Database with PostGIS 2.4 extension. Uses `pgdata/` for persistence.
- Web: Django for application code. See `web/`.



## Notes

To execute one-off Django commands, attach to the shell in the running web container. In the root of the project, with a running project:

```bash
$ docker-compose run --rm web /bin/sh
```

This allows you to run Django commands as such:

```bash
$ python3 manage.py --help
```

It can also be used to run `psql`:

```bash
$ psql -Ulizard -dlizard -hpostgres -W
```
The password is 'lizard'.



# Cartographic styling

## Styling with Maputnik
---------------------
In the root of the project, run a webserver:

```
$ python -mSimpleHTTPServer
```

Visit http://localhost:8000/maputnik/

You can load, edit and export the map style with this app.


## Generating sprite from SVGs
---------------------------

Instal `spritezero-cli`:

```bash
$ npm install -g @mapbox/spritezero-cli
```

In `icons/`, execute:

$ spritezero lizard svg/
$ spritezero lizard@2x svg/ --retina

This will generate a spritemap `lizard.json` and `lizard@2x.json` for use in the MapboxGL style object.






# Errors

- Uncaught Error: Unimplemented type: 4
This means the tiles are not being gzipped...



# Front-end

Todo. See `mapviewer/`.



# TODO

## Back-end

- Combine tile types into one tile (all asset types into one tile, per organisation)

- Management command for writing tiles per organisation

- Import/transform script for data from Lizard 6

- GraphQL schema with authorization / Flexible organisation permission system

- Nginx tile caching?

- Front-end for Map, Dashboard (using react-mozaik?)

- Release and deployment of Docker images

- Create models for organisations, assets

- Make a can_view/can_edit permission structure

- DashboardView(View): (bi.lizard.net)

- RasterView(View): (rasters.lizard.net)

- MapConfigView(View): (maps.lizard.net)

- Geocoder

- Search

- Geotrellis for rasters?

- Timescale extension?

- TileDB?

- Geo filtering in GraphQL?


## Front-end

- Context menu like iD editor?

- Adapt the mgmt screens
