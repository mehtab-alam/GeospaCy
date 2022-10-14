import streamlit as st
from spacy import displacy
import spacy
import geospacy
from PIL import Image
import base64
import sys
import pandas as pd
import en_core_web_md

colors = {'GPE': "#43c6fc", "LOC": "#fd9720", "RSE":"#a6e22d"}
options = {"ents": ['GPE', 'LOC', "RSE"], "colors": colors}

HTML_WRAPPER = """<div style="overflow-x: auto; border: none solid #a6e22d; border-radius: 0.25rem; padding: 1rem">{}</div>"""
model = ""

gpe_selected = ""
loc_selected = ""
rse_selected = ""

types = ""

BASE_URL = "http://localhost:8080/"



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



def set_side_menu():
    
    global gpe_selected, loc_selected, rse_selected, model, types
    types =""
    params = st.experimental_get_query_params()
    st.sidebar.markdown("## Spacy Model")
    st.sidebar.markdown("You can **select** the values of the *spacy model* from Dropdown.")
    models = ['en_core_web_sm', 'en_core_web_md', 'en_core_web_lg', 'en_core_web_trf']
    if "model" in params:
        default_ix = models.index(params["model"][0])
    else:
        default_ix = models.index('en_core_web_sm')
    model = st.sidebar.selectbox('Spacy Model',models, index=default_ix)
   
    st.sidebar.markdown("## Spatial Entity Labels")
    st.sidebar.markdown("**Mark** the Spatial Entities you want to extract?")
    tpes = ""
    if "type" in params:
        tpes = params['type'][0]

    if "g" in tpes:
        gpe = st.sidebar.checkbox('GPE', value = True)
    else:
        gpe = st.sidebar.checkbox('GPE')
    
    if "l" in tpes:
        loc = st.sidebar.checkbox('LOC', value = True)
    else:
        loc = st.sidebar.checkbox('LOC')
    if "r" in tpes:
        rse = st.sidebar.checkbox('RSE', value = True)
    else:
        rse = st.sidebar.checkbox('RSE')
    if(gpe):
        gpe_selected ="GPE"
        types+="g"
        
    if(loc):
        loc_selected ="LOC"
        types+="l"
        
    if(rse):
        rse_selected ="RSE"
        types+="r"
        
    
    
def set_input():
    params = st.experimental_get_query_params()
    if "text" not in params:
        text = st.text_area("Enter the text to extract {Spatial Entities}", "")
    else: 
        text = st.text_area("Enter the text to extract {Spatial Entities}", params["text"][0])
    if(st.button("Extract")):
        return text

def set_selected_entities(doc):
    global gpe_selected, loc_selected, rse_selected, model
    
    ents = [ent for ent in doc.ents if ent.label_ == gpe_selected or ent.label_ == loc_selected or ent.label_ == rse_selected]
    
    doc.ents = ents
    return doc

def extract_spatial_entities(text):
    try:
        #nlp = spacy.load(model)
        nlp = en_core_web_md.load()
        nlp.add_pipe("spatial_pipeline", after="ner")
        
        doc = nlp(text)
        
        doc = set_selected_entities(doc)
       
        html = displacy.render(doc,style="ent", options = options)
        html = html.replace("\n","")
        st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)
        show_spatial_ent_table(doc, text)
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        st.markdown("No Model '"+model+"' found. Please install using command "+"**python -m spacy download "+model+"**")

def show_spatial_ent_table(doc, text):
    global types
    if(len(doc.ents) > 0):
        st.markdown("**______________________________________________________________________________________**")
        st.markdown("**Spatial Entities List**")
        df = pd.DataFrame(columns=['Sr.','entity','label', 'Map', 'GEOJson'])
        
        for ent in doc.ents:
            url_map = BASE_URL+"Tagger?map=true&type="+types+"&model="+model+"&text="+text+"&entity="+ent._.rse_id
            url_json = BASE_URL+"Tagger?geojson=true&type="+types+"&model="+model+"&text="+text+"&entity="+ent._.rse_id
        
            new_row = {'Sr.': df.shape[0]+1,'entity':ent.text, 'label':ent.label_, 
                       
                       'Map':f'<a target="_self" href="{url_map}">View</a>', 
                       'GEOJson':f'<a target="_self" href="{url_json}">View</a>'}
           
            df = df.append(new_row, ignore_index=True)
        
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        
        
def main():	
    global gpe_selected, loc_selected, rse_selected, model
    #print(displacy.templates.TPL_ENT)
    set_header()
    set_side_menu()
    
    
    text = set_input()
    if(text is not None):
        extract_spatial_entities(text)
    elif "text" in st.session_state:
        text = st.session_state.text
        extract_spatial_entities(text)
 
           
if __name__ == '__main__':
	main()	
    
    
    