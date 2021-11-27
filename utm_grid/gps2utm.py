#!/usr/bin/env python3

"""
    convert GPS to UTM
    
    Copyright 2021 Arnaud Mouiche
    
    License MIT
    
"""

import argparse
import utm

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
    
parser = argparse.ArgumentParser()
parser.add_argument("CENTER_COORD", metavar="lat,long", type=CENTER_COORD_type, help="Center GPS of the grid (will be rounded to the nearest UTM 1km grid location). You can use '/' prefix if the latitude is negative (ex: /-45.0,1.0")
parser.add_argument("-z", "--zone", metavar="ZONE", type=ZONE_type, help="Force a specific UTM zone")
args = parser.parse_args()

lat, long = args.CENTER_COORD
[east, north, utm_zone, utm_letter] = utm.from_latlon(lat, long, force_zone_number=args.zone)
east=int(east)
north=int(north)

print(f"UTM zone {utm_zone} {utm_letter}")
print(f"E  {east//1000:4d} {east%1000:03d}")
print(f"N  {north//1000:4d} {north%1000:03d}")
