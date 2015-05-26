import logging
import sys
import argparse

from shapely.geometry import mapping, shape
from fiona import collection

def cleanPolys(inShp, outShp):
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    
    with collection(inShp, "r") as input:
        schema = input.schema.copy()
        with collection(
                outShp, "w", "ESRI Shapefile", schema
                ) as output:
            for f in input:
    
                try:
                    # Make a shapely object from the dict.
                    geom = shape(f['geometry'])
                    if not geom.is_valid:
    
                        # Use the 0-buffer polygon cleaning trick
                        clean = geom.buffer(0.0)
                        assert clean.geom_type == 'Polygon'
                        assert clean.is_valid
                        geom = clean
    
                    # Make a dict from the shapely object.
                    f['geometry'] = mapping(geom)
                    output.write(f)
    
                except Exception as e:
                    # Writing uncleanable features to a different shapefile
                    # is another option.
                    logging.exception("Error cleaning feature %s:", f['id'])
                
                
if __name__ == '__main__':
    """
    The command line user interface
    """
    parser = argparse.ArgumentParser(prog='cleanpolys.py',
                                    description='''Clean polygins by buffering by 0.0 using shapely.''')
    # Request the version number.
    parser.add_argument('-v', '--version', action='version', version='0.0.1 ')
    
    parser.add_argument('-i', '--input', type=str, required=True, help='''Input shapefile''')
    
    parser.add_argument('-o', '--output', type=str, required=True, help='''Output shapefile''')
    
    # Call the parser to parse the arguments.
    args = parser.parse_args()
    
    cleanPolys(args.input, args.output)
    