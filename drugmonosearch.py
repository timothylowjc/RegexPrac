# -*- coding: utf-8 -*-
"""
Drugsearch for mono
No tilt.
"""

import json
import re
from bs4 import BeautifulSoup
import pprint

drugs = []
with open('drugs-mono.json') as f:
    drugs = [json.loads(line) for line in f]


def bs4mono():
    for d in drugs:
        # Y = drug[k]["name"].split()
        for section_key, content in d["details"]["sections"].items():
            m = re.search('Dosage and Administration', section_key)
            if m:
                # m = re.match(f'(({Y[0]}))(.*?)(Dosage and Administration)',section_key).group()
                soup = BeautifulSoup(content, 'lxml')
                for table in soup.find_all('table'):
                    tr = table.find('tr')
                    head = [td.get_text().strip() for td in tr.find_all(['th', 'td'])]
                    print(head)
                # end for
        # end for
    # end for


def drugsearchmonobs4(mono):
    # Initialise for dosings
    dosings = ['Adult', 'Geriatric', 'Pediatric']

    # We find the dosage part if mono is not empty
    for section_title, section_content in mono["details"]["sections"].items():
        if 'Dosage and Administration' in section_title:
            break

    # Remove pointless paragraphs + tables
    soup = BeautifulSoup(section_content, 'lxml')
    # Remove tables
    for div in soup.find_all('div'):
        div.decompose()

    # Remove Admin/Limits
    DOSAGE_SECTIONS = ['Dosage', 'Special Populations']
    for h3 in soup.find_all(lambda tag: tag.name == 'h3' and tag.get_text() not in DOSAGE_SECTIONS):
        next3 = h3.next_sibling
        if not next3:
            continue
        while next3 and (next3.name != 'h3' or next3.get_text() not in DOSAGE_SECTIONS):
            next3.decompose()
            next3 = h3.next_sibling
        h3.decompose()
    # end for

    # Try to extract using bs4, and arrange like in a dict
    # Construct dictionary to print first
    dictionary = {'name': mono['name']}
    dictionary['dosages'] = []
    # Construct dose dictionary to use
    dose = {'age_group': None, 'indication': None, 'special_condition': None, 'dosage': []}

    for title in soup.find_all({'h4', 'h3'}):
        next4 = title.next_sibling
        if not next4:
            continue

        dose['age_group'] = title.get_text()
        if dose['age_group'] in ['Dosage', 'Special Populations']:
            dose['age_group'] = None
        if not [i for i in dosings if i in title.get_text()]:
            dose['age_group'] = 'Adults'
            dose['special_condition'] = title.get_text()
        if dose['special_condition'] in ['Dosage', 'Special Populations']:
            dose['special_condition'] = None

        indicator = None
        while next4 and next4.name != 'h4':
            tag_name = next4.name
            if tag_name == "h5":
                if indicator:
                    dose['dosage'] = '\n '.join(dose['dosage'])
                    if dose['indication'] and 'Administration' in dose['indication']:
                        dose['indication'] = None
                    if dose['special_condition'] in ['Dosage', 'Special Populations']:
                        dose['special_condition'] = None
                    dictionary['dosages'].append(dose)
                    dose = {'age_group': title.get_text(), 'indication': None, 'special_condition': None, 'dosage': []}
                    if not [i for i in dosings if i in title.get_text()]:
                        dose['age_group'] = 'Adults'
                        dose['special_condition'] = title.get_text()
                dose['indication'] = next4.get_text()
                indicator = next4.get_text()
            if tag_name in ["h6", "p"]:
                dose['dosage'] += [next4.get_text()]
            next4 = next4.next_sibling
        # end while
        if dose['dosage']:
            if indicator in ['Oral']:
                dose['dosage'] += indicator
                dose['indication'] = None
            dose['dosage'] = '\n '.join(dose['dosage'])
            if dose['indication'] and 'Administration' in dose['indication']:
                dose['indication'] = None
            if dose['special_condition'] in ['Dosage', 'Special Populations']:
                dose['special_condition'] = None
            if not [i for i in dosings if i in title.get_text()]:
                dose['age_group'] = 'Adults'
                dose['special_condition'] = title.get_text()
            dictionary['dosages'].append(dose)
            dose = {'age_group': None, 'indication': None, 'special_condition': None, 'dosage': []}
        # end if
    return dictionary
# end def

# for i, d in enumerate(drugs):
#     D = drugsearchmonobs4(d)
#     for dose in D['dosages']:
#         # for m in re.finditer(r'\((See.+?)\)', dose['dosage']):
# #             print(m.group(1))
#         print(dose['special_condition'])
#     # print(json.dumps(D, indent=4))
#         # if (dose['indication']) == 'Dosage & Administration':
        #     print(i)
# 260 and 372
# drugsearchmonobs4(drugs[260])
# # 105,207,327, 231, 293,246,294,214
D = drugsearchmonobs4(drugs[231])
print(json.dumps(D, indent=4))
# print(drugs[1327]['url'])
# 1327
