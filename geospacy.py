from spacy.tokens import Span
from spacy.tokens import Doc
from spacy.tokens import Token
import regex_spatial
from spacy.language import Language
import re

id =""
rse_id = "rse_id"
def set_extension():
     Span.set_extension(rse_id, default = "",force = True)
     Doc.set_extension(rse_id, default = "",force = True)
     Token.set_extension(rse_id, default = "",force = True)
     
def get_level1(doc, sentence, ent):
    return find_ent_by_regex(doc, sentence, ent, regex_spatial.get_level1_regex())

def get_level2(doc, sentence, ent):
  return find_ent_by_regex(doc, sentence, ent, regex_spatial.get_level2_regex()) 

def get_level3(doc, sentence, ent):
  return find_ent_by_regex(doc, sentence, ent, regex_spatial.get_level3_regex())


def find_ent_by_regex(doc, sentence, ent, regex):
  global id
  if id == "":
      id = ent.text
    
  for match in re.finditer(regex, doc.text):
        start, end = match.span()
        if(start>= sentence.start_char and start<= sentence.end_char):
          span = doc.char_span(start, end)
          if span is not None:
            id = span.text +"_"+ id
            
            if(start > ent.end_char):
              ent.end_char = end
            else:
              ent.start_char = start         
          return ent  
  return ent

def get_relative_entity(doc, sentence, ent):
  global id
  id = ""
  rel_entity = get_level1(doc, sentence, ent)
  
  rel_entity = get_level2(doc, sentence, rel_entity)
  rel_entity = get_level3(doc, sentence, rel_entity)
  
  if("_" in id):
    rel_entity = doc.char_span(rel_entity.start_char, rel_entity.end_char, "RSE")
    rel_entity._.rse_id = id
    return rel_entity
  rel_entity = doc.char_span(ent.start_char, ent.end_char, ent.label_)
  rel_entity._.rse_id = id
  return rel_entity 

@Language.component("spatial_pipeline")
def get_spatial_ent(doc):
  set_extension()
  new_ents = []
  ents = [ent for ent in doc.ents if ent.label_ == "GPE" or ent.label_ == "LOC"]
  end = None
  for ent in ents:
    
    if ent.end != len(doc):
        next_token = doc[ent.end + 1]
        if end is not None:
          start = end
        else: 
          start = ent.sent.start
        if next_token.text.lower() in regex_spatial.get_keywords():
          end = next_token.i
        else:
          end = ent.end
    else:
        start = ent.sent.start
        end = ent.end
    rsi_ent = get_relative_entity(doc,Span(doc, start, end), ent)
    print(rsi_ent.text, rsi_ent.label_, rsi_ent._.rse_id)
    new_ents.append(rsi_ent)  
    
  doc.ents = new_ents

  return doc