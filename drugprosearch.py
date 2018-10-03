# -*- coding: utf-8 -*-
"""
Make for Pro type
"""

import json
import re
from bs4 import BeautifulSoup


drugs = []
with open('drugs-pro.json') as x:
    for y in x:
        drugs.append(json.loads(y))


def drugsearchpro(pro):
    # Init dic, dose, dosings
    dictionary = {'name': pro['name']}
    dictionary['dosages'] = []
    dose = {'age_group': None, 'indication': None, 'special_condition': None, 'dosage': []}
    dosings = ['Adult', 'Geriatric', 'Pediatric']
    special = ['Adjustment for Toxicity', 'Obesity']
    remove = ['mcg', 'mg', 'minute', 'hour', 'Note:', 'with', 'without']
    # Loop through keys in PPA

    for section_title, section_content in pro["details"]["sections"].items():
        if 'Dosage and Administration' in section_title or 'DOSAGE AND ADMINISTRATION:' in section_title:
            break
    # Remove pointless paragraphs + tables
    soup = BeautifulSoup(section_content, 'lxml')
    # Remove tables
    for div in soup.find_all('table'):
        div.decompose()
    # Some with h3, some without???
    # findNext might be useful instead of next_sibling
    
    start = soup.find().find().find()
    next4 = start.find_next({'p','dd'})
    tag_name = next4.name
    while next4 and next4.name != 'h3':
        