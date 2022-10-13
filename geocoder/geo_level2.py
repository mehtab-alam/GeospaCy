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
from shapely.geometry import Polygon, MultiPoint
from shapely.geometry.base import geom_factory
from shapely.geos import lgeos
from geocoder import geo_level1

#def get_common_coordinates(coordinates, level2):
    #gdp.

def get_near(level2):
    near = re.search(regex_spatial.get_near_regex(), level2)
    if near is not None:
        return near.group()
    return None 

def get_surrounding(level2):
    surrounding = re.search(regex_spatial.get_surrounding_regex(), level2)
    if surrounding is not None:
        return surrounding.group()
    return None 

    
def sort_west(coords1, poly2, centroid):
    #coords1 = mapping(poly1)["features"][0]["geometry"]["coordinates"]
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

def get_directional_coordinates_by_angle(coordinates, centroid, direction, minimum, maximum):
    direction_coordinates = []
    for p in coordinates:
        angle = geoutil.calculate_bearing(centroid, p)
        if direction in geo_level1.east:
            if angle >= minimum or angle <= maximum:
                direction_coordinates.append(p)
                
        else:
             if angle >= minimum and angle <= maximum:
                direction_coordinates.append(p)
    #if(direction in geo_level1.west):
    #    direction_coordinates.sort(key=lambda k: k[2], reverse=True)
   
    return direction_coordinates 

def get_direction_coordinates(coordinates, centroid, level1):
    min_max = geo_level1.get_min_max(level1)
    if min_max is not None:
        coord = get_directional_coordinates_by_angle(coordinates, centroid, level1, min_max[0], min_max[1])
        return coord
    return coordinates


def get_level2_coordinates(coordinates, centroid, level_2, level_1):
    near = get_near(level_2)   
    surrounding = get_surrounding(level_2)
    
    
    poly1 = Polygon(coordinates)
    polygon1 = gpd.GeoSeries(poly1)
    if near is not None:
        poly2 = polygon1.buffer(0.0095, join_style=2)
    if surrounding is not None:
        poly2 = polygon1.buffer(0.012, join_style=2)
    
    poly = poly2.difference(polygon1)
    coords = mapping(poly)["features"][0]["geometry"]["coordinates"]
    
    coord = []
    for c in coords:
        pol = list(c[::-1])
        coord.extend(pol)
        
    if level_1 is not None and level_1.lower() not in geo_level1.center:
        coord = get_direction_coordinates(coord, centroid, level_1)
        if level_1 in geo_level1.west:
            coord = sort_west(coordinates,poly2, centroid)
    
    print("Level 2 Coordinates")
    for idx, p in enumerate(coord):
        print(idx, p)
    
    return coord, centroid


      