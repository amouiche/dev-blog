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
    lat,long = text.split(",")
    lat = float(lat)
    long = float(long)
    return lat, long

parser = argparse.ArgumentParser()
parser.add_argument("-W", "--width", metavar="KM", default=10, type=int, help="Width of the Grid in km")
parser.add_argument("-H", "--height", metavar="KM", default=10, type=int, help="Height of the Grid in km")

parser.add_argument("CENTER_COORD", metavar="lat,long", type=CENTER_COORD_type, help="Center GPS of the grid (will be rounded to the nearest UTM 1km grid location)")

parser.add_argument("-o", "--output", metavar="FILE", help="Save result to this file")
parser.add_argument("-f", "--format", choices=["geojson", "kml"], help="File format (if not provided through filename extention)")
args = parser.parse_args()


[east, north, utm_zone, utm_letter] = utm.from_latlon(*args.CENTER_COORD)

print(f"UTM zone {utm_zone}{utm_letter}")

#print("center:", east, north)
# round to neareast km UTM grid location
e = int((east+500)/1000)
n = int((north+500)/1000)
#print("narrow:", east, north)

w = (args.width+1)//2
h = (args.height+1)//2
e_start = e - w
e_end = e + w
n_start = n - h
n_end = n + h
    

utm_track = []  # path to draw in 1km grid. each steps are spaced only 1km east or 1km north from previous step

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
gps_track = [] # (long, lat) points
for e,n in utm_track:
    e *= 1000
    n *= 1000
    lat, long = utm.to_latlon(e, n, utm_zone, utm_letter)
    gps_track.append((long, lat))



if args.output and (not args.format):
    ext = os.path.splitext(args.output)[1][1:].lower()
    if ext not in ["geojson", "kml"]:
        print(f"Don't know how to manage format {ext}. abort.")
        exit(1)
    args.format = ext
    
if not args.format:
    print("No format provided for output.")
    exit(1)



east_start = e_start * 1000
north_start = n_start * 1000

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
        print("geojson python module not installed.")
        exit(1)
    kml = simplekml.Kml()
    
    lin = kml.newlinestring(name=f"UTM {utm_zone}{utm_letter}", description=f"UTM Grid {utm_zone}{utm_letter}",
                        coords=gps_track)
                        
    lat, long = utm.to_latlon(east_start, north_start, utm_zone, utm_letter)
    kml.newpoint(name=f"{east_start} {north_start}", description=f"{east_start} {north_start}",
                   coords=[(long,lat)])
    
    if args.output:
        print(f"Write KML output to {args.output}")
        kml.save(args.output)
        
