
import shapefile
from folium import Map

INDIA_COORDS = (21., 80.)
MAX_ZOOM = 5

def drawmap():
    f = Map(location=INDIA_COORDS, zoom_start=MAX_ZOOM)


def shape2json(fname, outfile="states.json"):
    reader = shapefile.Reader(fname)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]

    data = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        data.append(dict(type="Feature", geometry=geom, properties=atr))
            
    keys = ['abbrev', 'name', 'name_alt']
    for b in data:
        for key in keys:
            b['properties'][key] = b['properties'][key].decode('latin-1')

    with open(outfile, "w") as geojson:
        geojson.write(dumps({"type": "FeatureCollection",
                             "features": data}, indent=2) + "\n")
