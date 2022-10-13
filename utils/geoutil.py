#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 12:45:21 2022

@author: syed
"""

import math
import re
import regex_spatial
import quantities as pq
from math import radians, cos, sin, asin, sqrt
import quantities as pq



def get_kilometers(d, unit):
    q = float(d) * pq.CompoundUnit(unit)
    q.units = pq.km
    return q.magnitude

def ConvertToRadian(input):
    return input * math.pi / 180

def get_level1(ent):
    level_1 = re.search(regex_spatial.get_level1_regex(), ent)
    if level_1 is not None:
        return level_1.group()
    return None
def get_level2(ent):
    level_2 = re.search(regex_spatial.get_level2_regex(), ent)
    if level_2 is not None:
        return level_2.group()
    return None
def get_level3(ent):
    level_3 = re.search(regex_spatial.get_level3_regex(), ent)
    if level_3 is not None:
        return level_3.group()
    return None

def get_ase(ent):
    abs_sp = ent.split("_")
    return abs_sp[len(abs_sp)-1]

def get_ent(ent):
    return get_ase(ent), get_level1(ent), get_level2(ent), get_level3(ent)

def get_centroid(coordinates, centroid, mini, maxi):
    average = (mini + maxi)/2
    diff = []
    ind = 0
    for p in coordinates:
        diff.append(abs( p[2] - average))
   
    ind = diff.index(min(diff))    
   
    return midpoint(centroid[0], centroid[1], coordinates[ind][0], coordinates[ind][1], average)


def calculateArea(coordinates):
    area = 0
    if (len(coordinates) > 2):
        i = 0
        for i in range(len(coordinates) - 1):
            p1 = coordinates[i]
            p2 = coordinates[i + 1]
            area += math.radians(p2[0] - p1[0]) * (2 + math.sin(ConvertToRadian(p1[1])) + math.sin(math.radians(p2[0])))
        
        
        area = area * 6378137 * 6378137 / 1000000
    
    area = abs(round(area, 2)) + 2
    
    return area

def get_midmid_point(centroid, point1, point2, is_midmid):
    mid1 = midpoint(centroid[0], centroid[1], 
                            point1[0], point1[1]
                            , point1[2])
    mid2 = midpoint(centroid[0], centroid[1], 
                            point2[0], point2[1],
                            point2[2])
    midmid1 = midpoint(centroid[0], centroid[1], 
                            mid1[0], mid1[1]
                            , mid1[2])
    midmid2 = midpoint(centroid[0], centroid[1], 
                            mid2[0], mid2[1],
                            mid2[2])
    if is_midmid:
        return midmid1, midmid2
    else:
        return mid1, mid2

def getPointByDistanceAngle(lat, ln, angle, distanceInKm):

    R = 6378.1 #Radius of the Earth
    brng = angle * math.pi /180 #Bearing is 90 degrees converted to radians.
    d = distanceInKm #Distance in km
    
    #lat2  52.20444 - the lat result I'm hoping for
    #lon2  0.36056 - the long result I'm hoping for.
    
    lat1 = math.radians(lat) #Current lat point converted to radians
    lon1 = math.radians(ln) #Current long point converted to radians
    
    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
         math.cos(lat1)*math.sin(d/R)*math.cos(brng))
    
    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
                 math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
    
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    
    return [lon2, lat2, angle]

def midpoint(x1, y1, x2, y2, angle):
    
    lonA = math.radians(y1)
    lonB = math.radians(y2)
    latA = math.radians(x1)
    latB = math.radians(x2)

    dLon = lonB - lonA

    Bx = math.cos(latB) * math.cos(dLon)
    By = math.cos(latB) * math.sin(dLon)

    latC = math.atan2(math.sin(latA) + math.sin(latB),
                  math.sqrt((math.cos(latA) + Bx) * (math.cos(latA) + Bx) + By * By))
    lonC = lonA + math.atan2(By, math.cos(latA) + Bx)
    lonC = (lonC + 3 * math.pi) % (2 * math.pi) - math.pi
    latitude = round(math.degrees(latC), 8)
    longitude = round(math.degrees(lonC),8)
    return [latitude, longitude, angle]

def calculate_bearing(pointA, pointB):
  
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        return 400
    if (type(pointB[0]) != float) or (type(pointB[0]) != float):
        return 400
    
    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

  
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def getPointByDistanceAngle(lat, ln, angle, distance, unit):
    
    #distanceInKm = distance
    R = 6378.1 #Radius of the Earth
    brng = float(angle) * math.pi /180 #Bearing is 90 degrees converted to radians.
    d = get_kilometers(distance, unit) #Distance in km
    
    
    lat1 = math.radians(lat) #Current lat point converted to radians
    lon1 = math.radians(ln) #Current long point converted to radians
    
    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
         math.cos(lat1)*math.sin(d/R)*math.cos(brng))
    
    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
                 math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
    
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    
    return (round(lon2,8), round(lat2,8), angle)


def calculatePointByDistance(lat, ln, angle, distance, unit):
    coff = 100/(6378*1.56)
    kms = get_kilometers(distance, unit)
    
    d = kms * coff
    
    angle_x = math.cos( angle ) # * math.pi/180
    angle_y = math.sin( angle) # * math.pi/180
    lat_new =  lat + (d * angle_x) 
    ln_new =  ln + (d * angle_y) 

    return (round(ln_new,8), round(lat_new,8), angle)



def pointByAngle(lat, ln, angle, distance, unit):

    R = 6378.1 #Radius of the Earth
    brng = angle * math.pi /180 #Bearing is 90 degrees converted to radians.
    d = get_kilometers(distance, unit) #Distance in km
    
    #lat2  52.20444 - the lat result I'm hoping for
    #lon2  0.36056 - the long result I'm hoping for.
    
    lat1 = math.radians(lat) #Current lat point converted to radians
    lon1 = math.radians(ln) #Current long point converted to radians
    
    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
         math.cos(lat1)*math.sin(d/R)*math.cos(brng))
    
    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
                 math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
    
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    
    return (lon2, lat2, angle)


def getPointByDistance(lat, ln, angle, distance, unit):
    kms = get_kilometers(distance, unit)
    coef = kms / 111.32
    new_lat = lat + coef
    new_long = ln + coef / math.cos(lat * 0.01745)
    return (round(new_lat,8), round(new_long,8), angle)

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6371* c
    return km
    