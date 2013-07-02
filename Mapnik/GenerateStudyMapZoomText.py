#!/usr/bin/env python

import mapnik


m = mapnik.Map(1000, 1000, '+init=epsg:4326') # create a map with a given width and height in pixels and projected in WGS 84.
m.background = mapnik.Color('#87CEFF') # set background colour.

ssStyles = mapnik.Style() # style object to hold rules for Study Site
ssRules = mapnik.Rule() # rule object to hold symbolizers for Study Site

citiesStyles = mapnik.Style() # style object to hold rules for Cities
citiesRules = mapnik.Rule() # rule object to hold symbolizers Cities

pStyles = mapnik.Style() # style object to hold rules for Peru
pRules = mapnik.Rule() # rule object to hold symbolizers Peru

studySiteDS = mapnik.Shapefile(file='StudySiteRegion.shp')
studySiteLyr = mapnik.Layer('Study Site', '+init=epsg:4326')
studySiteLyr.datasource = studySiteDS

peruDS = mapnik.Shapefile(file='GRC_adm1.shp')
peruLyr = mapnik.Layer('Peru', '+init=epsg:4326')
peruLyr.datasource = peruDS

cityNames = mapnik.Shapefile(file='places.shp')
citiesLyr = mapnik.Layer('Cities', '+init=epsg:4326')
citiesLyr.datasource = cityNames



#point_symbolizer_cities = mapnik.PointSymbolizer()#mapnik.Color('#000000'))
#citiesRules.symbols.append(point_symbolizer_cities)



t = mapnik.TextSymbolizer(mapnik.Expression('[name]'), 'DejaVu Sans Book', 12, mapnik.Color('#000000'))
#t.halo_fill = mapnik.Color('#FFFFFF')
t.fill = mapnik.Color('#000000')
t.avoid_edges = True
#t.halo_radius = 0.5
t.label_placement = mapnik.label_placement.POINT_PLACEMENT #is default
#dir(t)
citiesRules.symbols.append(t)
citiesStyles.rules.append(citiesRules)

# to fill a polygon we create a PolygonSymbolizer
polygon_symbolizer_peru = mapnik.PolygonSymbolizer(mapnik.Color('#F0FFF0'))
pRules.symbols.append(polygon_symbolizer_peru) # add the symbolizer to the rule object

# to add outlines to a polygon we create a LineSymbolizer
line_symbolizer_peru = mapnik.LineSymbolizer(mapnik.Color('#000000'),1)
pRules.symbols.append(line_symbolizer_peru) # add the symbolizer to the rule object
pStyles.rules.append(pRules) # now add the rule to the style and we're done



# to fill a polygon we create a PolygonSymbolizer
polygon_symbolizer_studysite = mapnik.PolygonSymbolizer(mapnik.Color('#FF0000'))
polygon_symbolizer_studysite.fill = mapnik.Color('#FF0000')
polygon_symbolizer_studysite.fill_opacity = 1
ssRules.symbols.append(polygon_symbolizer_studysite) # add the symbolizer to the rule object

# to add outlines to a polygon we create a LineSymbolizer
line_symbolizer_studysite = mapnik.LineSymbolizer(mapnik.Color('#000000'),1)
ssRules.symbols.append(line_symbolizer_studysite) # add the symbolizer to the rule object
ssStyles.rules.append(ssRules) # now add the rule to the style and we're done


m.append_style('StudySite Style',ssStyles) # Styles are given names only as they are applied to the map
m.append_style('Peru Style',pStyles) # Styles are given names only as they are applied to the map
m.append_style('Cities Style',citiesStyles) # Styles are given names only as they are applied to the map

studySiteLyr.styles.append('StudySite Style')
peruLyr.styles.append('Peru Style')
citiesLyr.styles.append('Cities Style')

m.layers.append(peruLyr)
m.layers.append(studySiteLyr)
m.layers.append(citiesLyr)

print "Study Site BBOX: ", studySiteLyr.envelope()

#m.zoom_all()
bbox = mapnik.Envelope(mapnik.Coord(21.0, 36), mapnik.Coord(26, 41))
#bbox = mapnik.Envelope(mapnik.Coord(15.0, 30), mapnik.Coord(32, 46))
m.zoom_to_box(bbox) 

page = mapnik.printing.PDFPrinter(pagesize=(0.15, 0.16), margin=0.0075, resolution=150, preserve_aspect=True, centering=5, is_latlon=False, use_ocg_layers=False)

page.render_map(m,"StudySiteMapZoom.pdf")
mapCTX = page.get_context()
page.render_on_map_scale(m)
#mapCTX.move_to(50,250)
#page.render_scale(m, ctx=mapCTX, width=0.05)
#page.render_legend(m)
#mapCTX.move_to(130,20)
#page.write_text(mapCTX, "Study Site within Greece", size=14, fill_color=(0.0, 0.0, 0.0), alignment=None)
page.finish()

#mapnik.render_to_file(m, "othermap.pdf", 'pdf')


