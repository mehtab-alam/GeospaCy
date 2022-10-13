#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 21:44:47 2022

@author: syed
"""
import sys




loc_dict = {"east":"This is east", "west": "This is west", "north":"This is north",
            "south":"This is south","up":"This is up","down":"This is down",
            "look":"This is the description", "quit": "To end the game"}

user_input = input("Enter your desired location")

def findLocation(input, loc_dict):
    if input == "quit":
        sys.exit(f"End of the game with code{input}!")
    else:
        print(loc_dict[input])
    
    
 
