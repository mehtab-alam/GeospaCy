#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 13:11:36 2022

@author: syed
"""
import requests
import urllib3
import json
from geocoder import geo_level1
from geocoder import geo_level2
from geocoder import geo_level3
from utils import geoutil
import re
import regex_spatial
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)




def dismabiguate_entities(doc, ent, ase, level_1, level_2, level_3, midmid):
    return get_coordinates(ent, ase, level_1, level_2, level_3, midmid)
    

def get_coordinates(ent, ase, level_1, level_2, level_3, midmid):
    request_url = 'https://nominatim.openstreetmap.org/search.php?q='+ase+'&polygon_geojson=1&accept-language=en&format=jsonv2'
    page = requests.get(request_url, verify=False)
    print(request_url)
    json_content = json.loads(page.content)
    all_coordinates = json_content[0]['geojson']['coordinates'][0]
    centroid = (float(json_content[0]['lon']), float(json_content[0]['lat']))
    for p in all_coordinates:
        p2 = (p[0], p[1])
        angle = geoutil.calculate_bearing(centroid, p2)
        p.append(angle)
    mid1 = None
    mid2 = None
    coordinates = all_coordinates
    if level_1 is not None:
        all_coordinates, centroid, mid1, mid2 = geo_level1.get_level1_coordinates(all_coordinates, centroid, level_1, midmid)
        
    if level_2 is not None:
        if level_1 is not None and level_1.lower() not in geo_level1.center:
            all_coordinates, centroid = geo_level2.get_level2_coordinates(coordinates, centroid, level_2, level_1)
        else:
            print ("Else executed")
            all_coordinates, centroid = geo_level2.get_level2_coordinates(all_coordinates, centroid, level_2, level_1)
        
    if level_3 is not None:
        all_coordinates, centroid = geo_level3.get_level3_coordinates(coordinates, centroid, level_3, level_1)
    
    geojson = get_geojson(ent, all_coordinates, centroid)
    
    return geojson 

def get_geojson(ent, arr, centroid):
    poly_json = {}
    poly_json['type'] = 'FeatureCollection'
    poly_json['features'] = []
    coordinates= []
    coordinates.append(arr)
    poly_json['features'].append({
    'type':'Feature',
    'id': ent,
    'properties': {
        'centroid': centroid
        },
    'geometry': {
        'type':'Polygon',
        'coordinates': coordinates     
        }
    })
    return poly_json
    
def export(ent, poly_json):
    with open(ent+'.geojson', 'w') as outfile:
        json.dump(poly_json, outfile)
    
    