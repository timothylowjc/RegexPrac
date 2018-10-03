# -*- coding: utf-8 -*-
"""
Drugsearch for mono
No tilt.
"""

import json
import re
from bs4 import BeautifulSoup


drugs = []
with open('drugs-ppa.json') as x:
    for y in x:
        drugs.append(json.loads(y))


"""
Importing the above json as per usual
"""


def drugsearchppa(ppa):
    # Init dic, dose, dosings
    dictionary = {'name': ppa['name']}
    dictionary['dosages'] = []
    dose = {'age_group': None, 'indication': None, 'special_condition': None, 'dosage': []}
    dosings = ['Adult', 'Geriatric', 'Pediatric']
    special = ['Adjustment for Toxicity', 'Obesity']
    remove = ['mcg', 'mg', 'minute', 'hour', 'Note:', 'with', 'without']
    # Loop through keys in PPA
    for section_title, section_content in ppa["details"]["sections"].items():
        # Set up soup
        if 'Dosing:' in section_title:
            soup = BeautifulSoup(section_content, 'lxml')
            dose['age_group'] = section_title[8:]
            # Set up age_group with non-standard groups
            if dose['age_group'] in special:
                dose['special_condition'] = section_title[8:]
                dose['age_group'] = 'Adult'
                dose['dosage'] = soup.get_text()
                dictionary['dosages'].append(dose)
                dose = {'age_group': None, 'indication': None, 'special_condition': None, 'dosage': []}
                break
            if dose['age_group'] not in dosings:
                dose['special_condition'] = section_title[8:]
                dose['age_group'] = 'Adult'
            # Decompose tables
            for div in soup.find_all('div'):
                div.decompose()
            # Start of loop
            start = soup.p
            next4 = start.next_sibling
            if start.b and start.b.get_text() not in remove and start.b.get_text()[-1] in ':':
                dose['indication'] = start.b.get_text()
            else:
                dose['dosage'] += [start.get_text()]
            # Start while loop
            while next4:
                tag_name = next4.name
                # If bold exists and isn't rubbish, append on dosage
                if next4.b and next4.b.get_text() not in remove and next4.b.get_text()[-1] in ':':
                    dose['dosage'] = '\n '.join(dose['dosage'])
                    dictionary['dosages'].append(dose)
                    dose = {'age_group': section_title[8:], 'indication': next4.b.get_text(), 'special_condition': None, 'dosage': []}
                    if not [i for i in dosings if i in dose['age_group']]:
                        dose['special_condition'] = section_title[8:]
                        dose['age_group'] = 'Adult'
                # Add on to dosage
                if tag_name in ["i", "p"]:
                    dose['dosage'] += [next4.get_text()]
                    pass
                next4 = next4.next_sibling
            # end while
            if dose['dosage']:
                dose['dosage'] = '\n '.join(dose['dosage'])
                dictionary['dosages'].append(dose)
                dose = {'age_group': None, 'indication': None, 'special_condition': None, 'dosage': []}
                # end if
            # end for
        # end if

    return dictionary

for i, d in enumerate(drugs):
    D = drugsearchppa(d)
    for dose in D['dosages']:
            # for m in re.finditer(r'\((See.+?)\)', dose['dosage']):
            # print(m.group(1))
#         if (dose['special_condition']) == 'Obesity':
            # print(d['name'], i)
        print(dose['special_condition'])

# D = drugsearchppa(drugs[32])
# print(json.dumps(D, indent=4))
