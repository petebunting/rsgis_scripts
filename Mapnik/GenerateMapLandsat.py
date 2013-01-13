#!/usr/bin/env python

import mapnik


m = mapnik.Map(1000,1000, '+init=epsg:32718') # create a map with a given width and height in pixels
# note: m.srs will default to '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
# the 'map.srs' is the target projection of the map and can be whatever you wish 
m.background = mapnik.Color('transparent') # set background colour to 'steelblue'.

s = mapnik.Style() # style object to hold rules
r = mapnik.Rule() # rule object to hold symbolizers

landsatDS = mapnik.Gdal(file='L5TM_086S772W_20090628_TOARefl_RGB_Strd.tif')
landsatLyr = mapnik.Layer('Landsat', '+init=epsg:32718')
landsatLyr.datasource = landsatDS

r.symbols.append(mapnik.RasterSymbolizer())
s.rules.append(r)

m.append_style('My Style',s) # Styles are given names only as they are applied to the map

landsatLyr.styles.append('My Style')

m.layers.append(landsatLyr)

m.zoom_all()
#bbox = mapnik.Envelope(mapnik.Coord(220000.0, 8960000), mapnik.Coord(260000, 9000000))
#m.zoom_to_box(bbox) 

page = mapnik.printing.PDFPrinter(pagesize=(0.20, 0.20), margin=0.0075, resolution=150, preserve_aspect=True, centering=5, is_latlon=False, use_ocg_layers=True)

page.render_map(m,"Map2009Landsat.pdf")
page.render_on_map_scale(m)
#page.render_legend(m)
ctx = page.get_context()
ctx.move_to(210,30)
page.write_text(ctx, "Landsat 5 TM from 2009", size=14, fill_color=(0.0, 0.0, 0.0), alignment=None)
page.finish()


