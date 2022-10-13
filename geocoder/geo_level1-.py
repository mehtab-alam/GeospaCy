#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 12:38:31 2022

@author: syed
"""
import regex_spatial
from utils import geoutil


north = ["north", "N'", "North", "NORTH"]
south = ["south", "S'", "South", "SOUTH"]
east = ["east", "E'", "East", "EAST"]
west = ["west", "W'", "West", "WEST"]
northeast = ["north-east", "NE'", "north east", "NORTH-EAST", "North East", "NORTH EAST"]
southeast = ["south-east", "SE'", "south east", "SOUTH-EAST", "South East", "SOUTH EAST"]
northwest = ["north-west", "NW'", "north west", "NORTH-WEST", "North West", "NORTH WEST"]
southwest = ["south-west", "SW'", "south west", "SOUTH-WEST", "South West", "SOUTH WEST"]
center = ["center","central", "downtown","midtown"]
def get_min_max(direction):
    regex = regex_spatial.get_directional_regex()
    direction_list = regex.split("|")
    if direction in direction_list:
        if direction in north:
            return (337, 22)
        if direction in northeast:
            return (22, 67)
        if direction in east:
            return (67, 112)
        if direction in southeast:
            return (112, 157)
        if direction in south:
            return (157, 202)
        if direction in southwest:
            return (202, 247)
        if direction in west:
            return (247, 292)
        if direction in northwest:
            return (292, 337)
        
    return None   
        

def get_directional_coordinates_by_angle(coordinates, direction, minimum, maximum):
    direction_coordinates = []
    for p in coordinates:
        if direction in north:
            if p[2] >= minimum or p[2] <= maximum:
                direction_coordinates.append(p)
                
        else:
             if p[2] >= minimum and p[2] <= maximum:
                direction_coordinates.append(p)
    return direction_coordinates 
   
def get_directional_coordinates(coordinates, direction, centroid , minimum, maximum, is_midmid):
    direction_coordinates = get_directional_coordinates_by_angle(coordinates, direction, minimum, maximum)
    
    midmid1, midmid2= geoutil.get_midmid_point(centroid, direction_coordinates[0],direction_coordinates[-1], is_midmid) 
    if direction in south:
          maxi = max(p[2] for p in direction_coordinates)
          mini = min(p[2] for p in direction_coordinates)
          index_mini = 0
          index_maxi = 0
          for idx,p in enumerate(direction_coordinates):
              if p[2] == mini:
                  index_mini = idx
              if p[2] == maxi:
                  index_maxi = idx
          
          direction_coordinates.insert(index_maxi+1, midmid2)
          direction_coordinates.insert(index_mini+1, midmid1)
    else:
        direction_coordinates.append(midmid2)
        direction_coordinates.append(midmid1)
    
    return direction_coordinates, midmid1, midmid2

def get_level1_coordinates(coordinates, centroid, direction, is_midmid):
        min_max = get_min_max(direction)
        if min_max is not None:
           coordinates, mid1, mid2 = get_directional_coordinates(coordinates, direction, centroid,
                                              min_max[0], min_max[1],is_midmid) 
           #centroid = geoutil.get_centroid(coordinates, centroid,min_max[0], min_max[1])
           return coordinates, centroid, mid1, mid2
        elif direction.lower() in center:
            return  get_central(coordinates, centroid, direction, is_midmid), centroid, None, None
        else :
            return coordinates, centroid, None, None
def get_central(coordinates, centroid, direction, is_midmid):
   
    n_min_max = get_min_max("north")
    n_coordinates=get_directional_coordinates_by_angle(coordinates, "north", n_min_max[0], n_min_max[1])
    n_mid1, n_mid2 = geoutil.get_midmid_point(centroid,n_coordinates[0],n_coordinates[-1], is_midmid)
    
    ne_min_max = get_min_max("north east")
    ne_coordinates=get_directional_coordinates_by_angle(coordinates, "north east", ne_min_max[0], ne_min_max[1])
    ne_mid1, ne_mid2 = geoutil.get_midmid_point(centroid,ne_coordinates[0],ne_coordinates[-1], is_midmid)
    
    e_min_max = get_min_max("east")
    e_coordinates=get_directional_coordinates_by_angle(coordinates, "east", e_min_max[0], e_min_max[1])
    e_mid1, e_mid2 = geoutil.get_midmid_point(centroid,e_coordinates[0],e_coordinates[-1], is_midmid)

    se_min_max = get_min_max("south east")
    se_coordinates=get_directional_coordinates_by_angle(coordinates, "south east", se_min_max[0], se_min_max[1])
    se_mid1, se_mid2 = geoutil.get_midmid_point(centroid,se_coordinates[0],se_coordinates[-1], is_midmid)

    s_min_max = get_min_max("south")
    s_coordinates=get_directional_coordinates_by_angle(coordinates, "south", s_min_max[0], s_min_max[1])
    s_mid1, s_mid2 = geoutil.get_midmid_point(centroid,s_coordinates[0],s_coordinates[-1], is_midmid)

    sw_min_max = get_min_max("south west")
    sw_coordinates=get_directional_coordinates_by_angle(coordinates, "south west", sw_min_max[0], sw_min_max[1])
    sw_mid1, sw_mid2 = geoutil.get_midmid_point(centroid,sw_coordinates[0],sw_coordinates[-1], is_midmid)

    w_min_max = get_min_max("west")
    w_coordinates=get_directional_coordinates_by_angle(coordinates, "west", w_min_max[0], w_min_max[1])
    w_mid1, w_mid2 = geoutil.get_midmid_point(centroid,w_coordinates[0],w_coordinates[-1], is_midmid)
    
    nw_min_max = get_min_max("north west")
    nw_coordinates=get_directional_coordinates_by_angle(coordinates, "north west", nw_min_max[0], nw_min_max[1])
    nw_mid1, nw_mid2 = geoutil.get_midmid_point(centroid,nw_coordinates[0],nw_coordinates[-1], is_midmid)

    central_coordindates =[n_mid1, n_mid2, ne_mid1, ne_mid2, e_mid1, e_mid2,
                           se_mid1, se_mid2, s_mid1, s_mid2, sw_mid1, sw_mid2,
                           w_mid1, w_mid2, nw_mid1, nw_mid2]
    return central_coordindates        
    
    