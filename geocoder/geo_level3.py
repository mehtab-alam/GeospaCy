#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 12:38:31 2022

@author: syed
"""
import regex_spatial
from utils import geoutil
import geopandas as gpd
import pandas as pd
import re
from shapely.geometry import Polygon,mapping
import numpy as np
from shapely.geometry import Polygon, MultiPoint, LineString
from shapely.geometry.base import geom_factory
from shapely.geos import lgeos
from geocoder import geo_level1



def get_level3(level3):
    digits = re.findall('[0-9]+', level3)[0]
    unit = re.findall('[A-Za-z]+', level3)[0]
    return digits, unit


def get_directional_coordinates_by_angle(coordinates, centroid, direction, minimum, maximum):
    direction_coordinates = []
    for p in coordinates:
        angle = geoutil.calculate_bearing(centroid, p)
        p2= (p[0],p[1],angle)
        if direction in geo_level1.east:
            if angle >= minimum or angle <= maximum:
                direction_coordinates.append(p2)
                
        else:
             if angle >= minimum and angle <= maximum:
                direction_coordinates.append(p2)
    #print(type(direction_coordinates[0])) 
    #if(direction in geo_level1.west):
    #    direction_coordinates.sort(key=lambda k: k[2], reverse=True)
   
    return direction_coordinates 

def sort_west(poly1, poly2, centroid):
    coords1 = mapping(poly1)["features"][0]["geometry"]["coordinates"]
    coords2 = mapping(poly2)["features"][0]["geometry"]["coordinates"]
    coord1 = []
    coord2 = []
    coord = []
    for c in coords1:
        pol = list(c[::-1])
        coord1.extend(pol)
    for c in coords2:
        pol = list(c[::-1])
        coord2.extend(pol)
    coo1 = []
    coo2 = []
    for p in coord1:
        angle = geoutil.calculate_bearing(centroid, p)
        if angle >= 157 and angle <= 202:
            coo1.append((p[0], p[1], angle))
    for p in coord2:
        angle = geoutil.calculate_bearing(centroid, p)
        if angle >= 157 and angle <= 202:
            coo2.append((p[0], p[1], angle))
    coo1.extend(coo2)
    return coo1
    
def get_direction_coordinates(coordinates, centroid, level1):
    min_max = geo_level1.get_min_max(level1)
    if min_max is not None:
        coord = get_directional_coordinates_by_angle(coordinates, centroid, level1, min_max[0], min_max[1])
        return coord
    return coordinates
    
def get_level3_coordinates(coordinates, centroid, level_3, level1):
    distance, unit = get_level3(level_3)
    
    kms = geoutil.get_kilometers(distance, unit)
    print(distance, unit, kms)
    
    coord = []
    
    poly1 = Polygon(coordinates)
    polygon1 = gpd.GeoSeries(poly1)
    poly2 = polygon1.buffer(0.0095*kms, join_style=2)
    poly3 = polygon1.buffer(0.013*kms, join_style=2)
    poly = poly3.difference(poly2)
    coords = mapping(poly)["features"][0]["geometry"]["coordinates"]
    
    
    
    for c in coords:
        pol = list(c[::-1])
        coord.extend(pol)
    if level1 is not None:
        coord = get_direction_coordinates(coord, centroid, level1)
        if level1 in geo_level1.west:
            coord = sort_west(poly3, poly2, centroid)
    print("Level 3 Coordinates")
    for idx, p in enumerate(coord):
        print(idx, p)
    return coord, centroid



