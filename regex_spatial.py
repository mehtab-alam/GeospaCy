#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 14:57:18 2022

@author: syed
"""

from quantities import units as u


one_plus = "+"
zero_plus = "*"


def get_quantities_regex():
  myList = [unit for unit in dir(u.length) 
            if type(getattr(u.length, unit)) is u.UnitLength ]
  units = [ x for x in myList if "_" not in x ]
  units_regex = '|'.join(units)
  return "["+units_regex+"]"
def get_number_regex():
  regex = "[0-9]"
  return regex
def get_space_regex():
  regex = "\s"
  return regex

def get_directional_regex():
  cardinals_kwds = "north|south|east|west"
  ordinals_kwds = "north-east|north-west|south-east|south-west|north east|north west|south east|south west|northeast|northwest|southeast|southwest"
  symbols_kwds = "N'|S'|E'|W'|NE'|NW'|SE'|SW'"
  return ordinals_kwds+"|"+symbols_kwds+"|"+cardinals_kwds

def get_center_regex():
  center_kwds = "center|central|downtown|midtown"
  return center_kwds

def get_near_regex():
  near_kwds = "nearby|near|vicinity|close|beside|next|adjacent|immediate|border"
  return near_kwds

def get_surrounding_regex():
  surrounding_kwds = "surrounding|neigbourhood|proximity|territory|locality"
  return surrounding_kwds
def get_level1_regex():
  level_1_regex = "(?i)("+get_directional_regex()+"|"+get_center_regex()+")"
  return level_1_regex

def get_level2_regex():
  level_2_regex = "(?i)("+get_near_regex()+"|"+get_surrounding_regex()+")"
  return level_2_regex

def get_level3_regex():
  level_3_regex = "(?i)("+get_number_regex()+one_plus+get_space_regex()+zero_plus+get_quantities_regex()+one_plus+")"
  return level_3_regex



def get_keywords():
   keywords = []
   keywords = get_directional_regex().split("|")
   keywords.extend(get_near_regex().split("|"))
   keywords.extend(get_surrounding_regex().split("|"))
   keywords.extend(get_center_regex().split("|"))
   keywords.append(",")
   keywords.append("and")
   keywords.append(".")
   
   return keywords
