#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 14:38:28 2022

@author: syed
"""

import mysql.connector as sql_db 
import json
#import mysql.connector

# Initialize connection.
# Uses st.experimental_singleton to only run once.
#@st.experimental_singleton
def init_connection():
    #return sql_db.connect(**st.secrets["mysql"])
#    return sql_db.connect(user='root', password='root1234', 
#                                   host='127.0.0.1',port=3306,
#                                   database='rsi_polygon_schema')
    return sql_db.connect(user='freedb_root_mehtab', password='b%9bYQ%5TsK%mAD', 
                                   host='sql.freedb.tech',port=3306,
                                   database='freedb_rsi_polygon_schema')






query_insert_rating = "insert into rating(shape_id,expert_id, ratings) values(%s,%s,%s)"

#query_update_rating = "update rating set ratings = %s where shape_id = %s and expert_id = %s"


query_insert_shape = "insert into shape(ase,level_1, level_2, level_3, geojson) values(%s,%s,%s,%s,%s)"

query_insert_expert = "insert into expert(name,expertise, tools_expert) values(%s,%s,%s)"


def update_rating_query(shape_id, expert_id, ratings):
    query_rating = "update rating set ratings = '"+str(ratings)+"' where" 
    query_rating += " shape_id = '"+str(shape_id)+"' and expert_id = '"+str(expert_id)+"'"
    return query_rating


def get_rating_query(shape_id, expert_id):
    query_rating = "select * from rating where "
    if shape_id is not None:
        query_rating += "shape_id = '"+str(shape_id)+"' "
    if expert_id is not None:
        query_rating += "and expert_id = '"+str(expert_id)+"' "
   
    return query_rating

def get_shape_query(ase, level_1, level_2, level_3):
    query_shape = "select * from shape where "
    if ase is not None:
        query_shape += "ase = '"+ase+"' "
    if level_1 is not None:
        query_shape += "and level_1 = '"+level_1+"' "
    if level_2 is not None:
        query_shape += "and level_2 = '"+level_2+"' "
    if level_3 is not None:
        query_shape += "and level_3 = '"+level_3+"'"
    return query_shape

def get_expert_query(name, expertise):
    query_expert = "select * from expert where "
    if name is not None:
        query_expert += "name = '"+name+"' "
    if expertise is not None:
        query_expert += "and expertise = '"+expertise+"' "
    return query_expert

def apply_rating(name, expertise, tools_selected, 
                              rating_selected, ase, level_1, level_2, level_3, geojson):
    connection = init_connection()
    cursor = connection.cursor(prepared=True)
    
    query_shape = get_shape_query(ase, level_1, level_2, level_3)

    #tuple_shape = (ase, level_1, level_2, level_3)
    tuple_expert = (name, expertise, str(tools_selected)[1:-1])
    cursor.execute(query_shape)
    record_shape = cursor.fetchone()
    print("Record Shape:", record_shape)
    print("Shape Select Query:", cursor.statement)
    if record_shape is None:
         tuple_insert_shape = (ase, level_1, level_2, level_3, json.dumps(geojson))
         print(len(geojson))
         cursor.execute(query_insert_shape, tuple_insert_shape)
         connection.commit()
         shape_id = cursor.lastrowid
         print(f"Insert query executed with id : {shape_id}")
    else:
        shape_id = record_shape[0]
    
    query_expert = get_expert_query(name, expertise)

    cursor.execute(query_expert)
    record_expert = cursor.fetchone()
    print("Expert Select Query:", cursor.statement)
    if record_expert is None:
        cursor.execute(query_insert_expert, tuple_expert)
        connection.commit()
        expert_id = cursor.lastrowid
    else:
        expert_id = record_expert[0]
    
    query_rating = get_rating_query(shape_id, expert_id)
    cursor.execute(query_rating)
    record_rating = cursor.fetchone()
    
    print("Ratings Select Query:", cursor.statement)
    
    
    print("Shape ID", shape_id, "...Expert ID", expert_id)
    tuple_rating = (shape_id, expert_id, rating_selected)
    if record_rating is None:
        cursor.execute(query_insert_rating, tuple_rating)
        connection.commit()
    else:
        cursor.execute(update_rating_query(shape_id, expert_id, rating_selected))
        connection.commit()
    
    
    
    
    
    
    
    
    
    
