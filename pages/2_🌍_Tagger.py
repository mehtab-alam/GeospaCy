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


from streamlit.components.v1 import html

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

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
    st.sidebar.markdown("## View")
    #st.sidebar.markdown("Select the **format** to view coordinates")
    view = st.sidebar.radio(
     "Select the format to view coordinates",
     ('Map', 'GEOJson'), horizontal=True)
    st.sidebar.markdown("## Compute")
    is_midmid = st.sidebar.radio(
     "Do you Want to compute polygons with mid or midmid point",
     ('midpoint', 'midmidpoint'), horizontal=True)
    midmid = False
    if is_midmid == "midmidpoint":
        midmid = True
    
    params = st.experimental_get_query_params()
    ase = None
    level_1= None 
    level_2= None
    level_3= None
    if "entity" in params:
        ase, level_1, level_2, level_3 = geoutil.get_ent(params["entity"][0])
        md = "<span><b>ASE:</b>&emsp;"+ str(ase)+"&emsp;<b>Level 1:</b>&emsp;"+ str(level_1)+"&emsp;<b>Level 2:</b>&emsp;"+ str(level_2)+"&emsp;<b>Level 3:</b>&emsp;"+ str(level_3)+"</span>"
        st.write(md,  unsafe_allow_html=True)
    if view  == "Map":
        if "text" in params:
            doc = extract_spatial_entities(params["model"][0],params["text"][0],params["type"][0])
            geojson = disambiguate.dismabiguate_entities(doc, params["entity"][0],ase, level_1, level_2, level_3, midmid)
            draw_location(geojson)
    elif view  == "GEOJson":
        if "text" in params:
            doc = extract_spatial_entities(params["model"][0],params["text"][0],params["type"][0])
            geojson = disambiguate.dismabiguate_entities(doc, params["entity"][0],ase, level_1, level_2, level_3, midmid)
            displayGeoJson(geojson)
            
def set_geojson_menu():
    global geojson
    st.sidebar.markdown("## Export")
    st.sidebar.markdown("Do you want to Export **GEOJson**?")
    export = st.sidebar.button("Export")
    if(export):
        params = st.experimental_get_query_params()
        disambiguate.export(params["entity"][0],geojson)

def set_map_menu():
    st.sidebar.markdown("## Rate Polygon")
    #st.sidebar.markdown("Do you want to rate the **Polygon**?")
    rate = st.sidebar.radio(
     "Do you want to rate the Polygon?",
     ('Yes', 'No'), horizontal=True)
    rate_btn = st.sidebar.button("Rate")
    if rate_btn:
        if rate == "Yes":
            nav_page("Rate")
    
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

def displayGeoJson(geojson):
    #path = ent._.rse_id+".geojson"
    #with open(path) as f:
    #gj = json.load(geojson)
    st.json(geojson)


set_header()
view_polygon_menu()
set_map_menu()
set_geojson_menu()

#displayGeoJson()
