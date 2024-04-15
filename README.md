# GeospaCy


**GeospaCy** is a web application built in Python language used for extracting spatial relation entities (spatRE) from text and Geo-referenced them. 

## Installation
There are few Python packages that are needed to install for running the application

1. Install spacy for natural language processing (NLP) tasks 
```sh
pip install spacy
```
2. Install gensim library for data preprocessing
```sh
pip install gensim
```
3. Install streamit library for running web application 
```sh
pip install streamlit
```
4. Install spacy-streamlit for display named entities (spatRE) in the text 
```sh
pip install spacy-streamlit
```

5. Install GeoPandas
```sh
pip install geopandas
```
6.  Install folium library for manipulating your data in Python, then visualize it in a Leaflet map via folium.

```sh
pip install folium
```
7. Install streamlit-folium library to visualize Leaflet map in streamlit web application

```sh
pip install streamlit-folium
``` 

## How to run the web application

```sh
streamlit run 1_🏠_Parser.py
```

## [Cite this work](https://github.com/mehtab-alam/GeospaCy/)

```latex
@inproceedings{mehtab-alam-etal-2024-geospacy,
    title = "{G}eospa{C}y: A tool for extraction and geographical referencing of spatial expressions in textual data",
    author = "Mehtab Alam, Syed  and
      Arsevska, Elena  and
      Roche, Mathieu  and
      Teisseire, Maguelonne",
    editor = "Aletras, Nikolaos  and
      De Clercq, Orphee",
    booktitle = "Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics: System Demonstrations",
    month = mar,
    year = "2024",
    address = "St. Julians, Malta",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.eacl-demo.13",
    pages = "115--126",
}
```

