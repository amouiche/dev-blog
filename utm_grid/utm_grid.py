#!/usr/bin/env python3

"""
    This tool generate a UTM 1km grid around one GPS location.
    The output format is KLM or GeoJSON, making it easy to import in your
    favorite GPS maps application
    
    Copyright 2021 Arnaud Mouiche
    
    License MIT
    
"""

import argparse
import utm
import math
import os

def CENTER_COORD_type(text):
    # remove first char if this one is here to hide the first '-' is case of negative latitude
    if text[0:1] in "=/(,:_":
        text = text[1:]
    lat,long = text.split(",")
    lat = float(lat)
    long = float(long)
    return lat, long
    
    
def ZONE_type(text):
    z = int(text)
    if z < 1 or z > 60:
        raise ValueError("Zone must be an integer value between 1 and 60")
    return z
    
def KM_type(text):
    s = int(text)
    if s <= 0:
        raise ValueError("Invalid KM value")
    return s

parser = argparse.ArgumentParser()
parser.add_argument("CENTER_COORD", metavar="lat,long", type=CENTER_COORD_type, help="Center GPS of the grid (will be rounded to the nearest UTM 1km grid location). You can use '/' prefix if the latitude is negative (ex: /-45.0,1.0")
parser.add_argument("-W", "--width", metavar="KM", default=10, type=KM_type, help="Width of the Grid in km (default 10)")
parser.add_argument("-H", "--height", metavar="KM", default=10, type=KM_type, help="Height of the Grid in km (default 10)")
parser.add_argument("-q", "--square-size", metavar="KM", default=1, type=KM_type, help="size of each square in km (default 1)")

parser.add_argument("-z", "--zone", metavar="ZONE", type=ZONE_type, help="Force a specific UTM zone")

parser.add_argument("-p", "--display-period", metavar="PERIOD", type=int, default=10, help="Display UTM coords in the grid every PERIOD km")

parser.add_argument("-m", "--meridien", action="store_true", help="Draw one meridien going through CENTER_COORD")


parser.add_argument("-o", "--output", metavar="FILE", help="Save result to this file")
parser.add_argument("-f", "--format", choices=["geojson", "kml"], help="File format (if not provided through filename extention)")
args = parser.parse_args()

lat, long = args.CENTER_COORD
[east, north, utm_zone, utm_letter] = utm.from_latlon(lat, long, force_zone_number=args.zone)





print(f"UTM zone {utm_zone}{utm_letter}")

print("Provided center:", int(east), int(north))
# round to neareast km UTM grid location
q = args.square_size
e = int((east+500*q)/(1000*q))
n = int((north+500*q)/(1000*q))
print("Grid center:    ", e*q*1000, n*q*1000)

w = (args.width+q)//(2*q)
h = (args.height+q)//(2*q)
e_start = e - w
e_end = e + w
n_start = n - h
n_end = n + h
    

utm_track = []  # path to draw in 'q' km grid. each steps are spaced only 'q'km east or 'q'km north from previous step

def goto(e,n):
    """
        Move pointer on utm_track to east, north location (1km grid)
        Don't go directly, but 1km per 1km since UTM lines will be curved once reported to a GPS map
    """
    global utm_track
    if not utm_track:
        utm_track.append((e,n))
        return
    ce, cn = utm_track[-1]  # current pointer
    while ce != e:
        if ce < e:
            ce += 1
        else:
            ce += -1
        utm_track.append((ce,cn))
    while cn != n:
        if cn < n:
            cn += 1
        else:
            cn += -1
        utm_track.append((ce,cn))
    


# draw the grid with Z shape to limit the number of points. First, draw vertical lines
# ┌─┐ ┌
# │ │ │...
# ╵ └─┘
for e in range(e_start, e_end+1):
    if e & 1:
        goto(e, n_start)
        goto(e, n_end)
    else:
        goto(e, n_end)
        goto(e, n_start)
       
# then draw the horizontal lines
# ╶─┐
# ┌─┘
# └─┐
# ...
for n in range(n_start, n_end+1):
    if n & 1:
        goto(e_start, n)
        goto(e_end, n)
    else:
        goto(e_end, n)
        goto(e_start, n)


# convert UTM 1km grid track to GPS coords track

gps_track = [] # (lat, long) points
for e,n in utm_track:
    e *= 1000 * q
    n *= 1000 * q
    lat, long = utm.to_latlon(e, n, utm_zone, utm_letter)
    gps_track.append((lat, long))

lat_min = min([lat for lat, long in gps_track])
lat_max = max([lat for lat, long in gps_track])


if args.output and (not args.format):
    ext = os.path.splitext(args.output)[1][1:].lower()
    if ext not in ["geojson", "kml"]:
        print(f"Don't know how to manage format {ext}. abort.")
        exit(1)
    args.format = ext
    
if not args.format:
    print("No format provided for output.")
    exit(1)



if args.format == "geojson":
    try:
        import geojson
    except ModuleNotFoundError:
        print("geojson python module not installed.")
        exit(1)
    
    lat1, long1 = gps_track[0]
    
    geo_items = []
    for (lat2, long2) in gps_track[1:]:
        geo_items.append(geojson.LineString([(long1, lat1), (long2, lat2)]))
        lat1, long1 = lat2, long2
        
    if args.meridien:
        lat, long = args.CENTER_COORD
        geo_items.append(geojson.LineString([(long, lat_max), (long, lat_min)]))

    geo_collection = geojson.GeometryCollection(geo_items)
    if args.output:
        print(f"Write GEOJSON output to {args.output}")
        geojson.dump(geo_collection, open(args.output, "w"))
    else:
        print(geojson.dumps(geo_collection))

if args.format == "kml":
    try:
        import simplekml
    except ModuleNotFoundError:
        print("simplekml python module not installed.")
        exit(1)
    kml = simplekml.Kml()
    
    lin = kml.newlinestring(name=f"UTM {utm_zone}{utm_letter}", description=f"UTM Grid {utm_zone}{utm_letter}",
                        coords=[(long, lat) for lat,long in gps_track])
                        
    if args.meridien:
        lat, long = args.CENTER_COORD
        kml.newlinestring(name="Meridien", description="Meridien", 
            coords=[(long, lat_max), (long, lat_min)])


                        
    for i in range(0, w*2+1, args.display_period):
        for j in range(0, h*2+1, args.display_period):
            lat, long = utm.to_latlon((e_start+i)*1000*q, (n_start+j)*1000*q, utm_zone, utm_letter)
            kml.newpoint(name=f"{utm_zone}{utm_letter} {(e_start+i)*q} {(n_start+j)*q} ", description=f"{utm_zone}{utm_letter} {(e_start+i)*q} {(n_start+j)*q}",
                         coords=[(long,lat)])
    
    if args.output:
        print(f"Write KML output to {args.output}")
        kml.save(args.output)
        
