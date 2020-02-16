# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 22:24:55 2020

@author: verma
"""


from flask import Flask, request
from flasgger import Swagger
from flask import jsonify
import mypackage.constants as cs

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/predict_file', methods=["POST"])
def predict_iris_file():
    """Example file endpoint returning a prediction of iris
    ---
    parameters:
      - name: fieldNameHere
        in: formData
        type: file
        required: true
    """
    data = (request.files.get("fieldNameHere")).read().decode()
    entity = extract_entity_sections(data)
    return jsonify(entity)
if __name__ == '__main__':
    #nlp = spacy.load('en_core_web_sm')
    app.run()
   
def extract_entity_sections(text):
    '''
    Helper function to extract all the raw text from sections of resume

    :param text: Raw text of resume
    :return: dictionary of entities
    '''
    text_split = [i.strip() for i in text.split('\n')]
    # sections_in_resume = [i for i in text_split if i.lower() in sections]
    entities = {}
    key = False
    for phrase in text_split:
        if len(phrase) == 1:
            p_key = phrase
        else:
            p_key = set(phrase.lower().split()) & set(cs.RESUME_SECTIONS)
        try:
            p_key = list(p_key)[0]
        except IndexError:
            pass
        if p_key in cs.RESUME_SECTIONS:
            entities[p_key] = []
            key = p_key
        elif key and phrase.strip():
            entities[key].append(phrase)
    
    # entity_key = False
    # for entity in entities.keys():
    #     sub_entities = {}
    #     for entry in entities[entity]:
    #         if u'\u2022' not in entry:
    #             sub_entities[entry] = []
    #             entity_key = entry
    #         elif entity_key:
    #             sub_entities[entity_key].append(entry)
    #     entities[entity] = sub_entities

    # pprint.pprint(entities)

    # make entities that are not found None
    # for entity in cs.RESUME_SECTIONS:
    #     if entity not in entities.keys():
    #         entities[entity] = None 
    return entities
    
