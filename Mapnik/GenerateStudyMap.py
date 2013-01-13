#!/usr/bin/env python

import mapnik


m = mapnik.Map(1000, 1000, '+init=epsg:4326') # create a map with a given width and height in pixels and projected in WGS 84.
m.background = mapnik.Color('#87CEFF') # set background colour.

ssStyles = mapnik.Style() # style object to hold rules for Study Site
ssRules = mapnik.Rule() # rule object to hold symbolizers for Study Site

cStyles = mapnik.Style() # style object to hold rules for Countries
cRules = mapnik.Rule() # rule object to hold symbolizers Countries

pStyles = mapnik.Style() # style object to hold rules for Peru
pRules = mapnik.Rule() # rule object to hold symbolizers Peru

studySiteDS = mapnik.Shapefile(file='StudySite_latlong.shp')
studySiteLyr = mapnik.Layer('Study Site', '+init=epsg:4326')
studySiteLyr.datasource = studySiteDS

countriesDS = mapnik.Shapefile(file='continent.shp')
countriesLyr = mapnik.Layer('Countries', '+init=epsg:4326')
countriesLyr.datasource = countriesDS

peruDS = mapnik.Shapefile(file='PER_adm1.shp')
peruLyr = mapnik.Layer('Peru', '+init=epsg:4326')
peruLyr.datasource = peruDS

# to fill a polygon we create a PolygonSymbolizer
polygon_symbolizer_countries = mapnik.PolygonSymbolizer(mapnik.Color('#DCDCDC'))
cRules.symbols.append(polygon_symbolizer_countries) # add the symbolizer to the rule object

# to add outlines to a polygon we create a LineSymbolizer
line_symbolizer_countries = mapnik.LineSymbolizer(mapnik.Color('#000000'),1)
cRules.symbols.append(line_symbolizer_countries) # add the symbolizer to the rule object
cStyles.rules.append(cRules) # now add the rule to the style and we're done

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


m.append_style('Countries Style',cStyles) # Styles are given names only as they are applied to the map
m.append_style('StudySite Style',ssStyles) # Styles are given names only as they are applied to the map
m.append_style('Peru Style',pStyles) # Styles are given names only as they are applied to the map

countriesLyr.styles.append('Countries Style')
studySiteLyr.styles.append('StudySite Style')
peruLyr.styles.append('Peru Style')

m.layers.append(countriesLyr)
m.layers.append(peruLyr)
m.layers.append(studySiteLyr)

print "Study Site BBOX: ", studySiteLyr.envelope()

#m.zoom_all()
bbox = mapnik.Envelope(mapnik.Coord(-85.0, -20), mapnik.Coord(-65, 0))
m.zoom_to_box(bbox) 

page = mapnik.printing.PDFPrinter(pagesize=(0.15, 0.16), margin=0.0075, resolution=150, preserve_aspect=True, centering=5, is_latlon=False, use_ocg_layers=False)

page.render_map(m,"StudySiteMap.pdf")
mapCTX = page.get_context()
page.render_on_map_scale(m)
#mapCTX.move_to(50,250)
#page.render_scale(m, ctx=mapCTX, width=0.05)
#page.render_legend(m)
mapCTX.move_to(150,10)
page.write_text(mapCTX, "Study Site within Peru", size=14, fill_color=(0.0, 0.0, 0.0), alignment=None)
page.finish()

#mapnik.render_to_file(m, "othermap.pdf", 'pdf')


