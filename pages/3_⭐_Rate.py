#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 19:55:23 2022

@author: syed
"""
import streamlit as st
from PIL import Image
import base64
from streamlit_folium import folium_static
import folium
from utils import geoutil
from disambiguation import disambiguate
import spacy
from db import poly_db_util

#BASE_URL = "http://localhost:8080/"

geojson = ""
def set_header():
    LOGO_IMAGE = "tetis-1.png"

    st.markdown(
        """
        <style>
        .container {
            display: flex;
        }
        .logo-text {
            font-weight:700 !important;
            font-size:50px !important;
            color: #f9a01b !important;
            padding-left: 10px !important;
        }
        .logo-img {
            float:right;
            width: 28%;
            height: 28%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <div class="container">
            <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
            <p class="logo-text">GeOspaCy</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
def set_selected_entities(doc, types):
    gpe_selected=""
    loc_selected=""
    rse_selected=""
    if "g" in types:
        gpe_selected ="GPE"
    if "l" in types:
        gpe_selected ="LOC"
    if "r" in types:
        gpe_selected ="RSE"
    ents = [ent for ent in doc.ents if ent.label_ == gpe_selected or ent.label_ == loc_selected or ent.label_ == rse_selected]
    
    doc.ents = ents
    return doc

def extract_spatial_entities(model,text, types):
    nlp = spacy.load(model)
    nlp.add_pipe("spatial_pipeline", after="ner")
    
    doc = nlp(text)
    
    doc = set_selected_entities(doc, types)
    return doc


def view_polygon_menu():
    global geojson
    
    is_midmid = False
    midmid = False
    #if is_midmid == "midmidpoint":
    #    midmid = True
    
    params = st.experimental_get_query_params()
    ase = None
    level_1= None 
    level_2= None
    level_3= None
    if "entity" in params:
        ase, level_1, level_2, level_3 = geoutil.get_ent(params["entity"][0])
        md = "<span><b>ASE:</b>&emsp;"+ str(ase)+"&emsp;<b>Level 1:</b>&emsp;"+ str(level_1)+"&emsp;<b>Level 2:</b>&emsp;"+ str(level_2)+"&emsp;<b>Level 3:</b>&emsp;"+ str(level_3)+"</span>"
        st.write(md,  unsafe_allow_html=True)
    if "text" in params:
        #doc = extract_spatial_entities(params["model"][0],params["text"][0],params["type"][0])
        #geojson = disambiguate.dismabiguate_entities(doc, params["entity"][0],ase, level_1, level_2, level_3, midmid)
        draw_location(geojson)
   
            


def set_map_menu():
    st.sidebar.markdown("## Rate Polygon")
    #st.sidebar.markdown("Do you want to rate the **Polygon**?")
    
def set_user_menu():
    expertise = ['Spatial Data Analyst', 'Geographer', 'QGIS Expert', 'Other']
    tools_used = ['ArcGIS', 'QGIS', 'OSM', 'GeoNames', "Others"]
    
    name_selected = st.sidebar.text_input('Expert Name',value='Anonymous', placeholder="First_Name Last_Name")
    expertise_selected = st.sidebar.selectbox('Expertise',expertise, index=0)
    tools_selected = st.sidebar.multiselect('Tools Used',tools_used)
    rating_selected = st.sidebar.select_slider('Rate the Polygon', ["Unclear", "2", "3", "4", "Excellent"])
    rate_btn =  st.sidebar.button("Rate!")
    if(rate_btn):
        rating_selected = rating_selected.replace("Unclear", "1").replace("Excellent", "5")
        rate_poly(name_selected, expertise_selected, tools_selected, rating_selected)
    

def rate_poly(name, expertise, tools_selected, rating_selected):
    params = st.experimental_get_query_params()
    ase, level_1, level_2, level_3 = geoutil.get_ent(params["entity"][0])
    print(ase, level_1, level_2, level_3)
    #geojson = disambiguate.dismabiguate_entities(doc, params["entity"][0],ase, level_1, level_2, level_3, midmid)
        
    poly_db_util.apply_rating(name, expertise, tools_selected, 
                              rating_selected, ase, level_1, level_2, level_3, geojson)

def draw_location(geojson):
    #gj = json.load(geojson)
    centroid = geojson['features'][0]['properties']['centroid']
    centroid = (centroid[0],centroid[1])
    my_map = folium.Map(location=[centroid[1], centroid[0]],
                                    zoom_start =12)

    folium.GeoJson(geojson,
        smooth_factor=1,
        style_function = lambda x: {
            'fillColor': 'green',
            'color': 'blue',
            'weight': 1.5,
            'fillOpacity': 0.3
        },
    popup =True,
    name= geojson['features'][0]['id']).add_to(my_map)
    folium_static(my_map)




set_header()
params = st.experimental_get_query_params()
ase, level_1, level_2, level_3 = geoutil.get_ent(params["entity"][0])
doc = extract_spatial_entities(params["model"][0],params["text"][0],params["type"][0])
geojson = disambiguate.dismabiguate_entities(doc, params["entity"][0],ase, level_1, level_2, level_3, False)
        
view_polygon_menu()
set_map_menu()
set_user_menu()
#set_geojson_menu()

#displayGeoJson()
