# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 21:10:52 2018

@author: Timothy Low
"""

"""
Tasked to extract drug dosage data from drug JSON, sort by age_group, then by
indication or special_condition if applicable.  

Data has a lot of unnecessary components, only required to pull out "Dosing" and 
sort by age_group. 

3 types of data formats mentioned: 'ppa', 'monograph', 'pro'. Probably best to
cover the easier formats first, then move on to harder, supposedly 'pro', under
details.info_type.

Unused to text scraping, best to figure out how to sort and present text based
data neatly first. 

Initial inspection shows 300 drugs in JSON.
"""
import json
import re


drug = []
with open('drugs.json') as x:
    for y in x:
        drug.append(json.loads(y))
        
"""
Creates a database for parsing the JSON. Able to pull lines of drugs with its 
corresponding details using commands such as:

drug[1]["details"]["sections"]["Introduction"]

And so on. Must now attempt to pull out dosings based on detail type.

for x in drug:
    if x["name"] == "H.P. Acthar Gel":
        print(x["details"]["sections"]["H.P. Acthar Gel Dosage and Administration"])
        
Can find info_type using: drug[1]["details"]["info_type"] and adapting it.
Calcifediol is ppa type.
H.P. Acthar Gel is monograph.
Desoximetasone Topical Spray is pro.

Can look through these 3 for an idea of how the dictionary looks like.

Above gives me the Dosage and administration information for H.P.Acthar Gel.
However, section under dosage is incredibly messy. This is type Monograph.
Will check the other types see if they are easier to access.
"""

for y,x in enumerate(drug):
    if x["name"] == "Calcifediol":
        no = y
     
"""
Above gives me row number for the searched drug. Could be easier for indexing.
"""

drug[4]["details"]["sections"]["Dosing: Geriatric"]

"""
Above gives me dosing information for Calcifediol, PPA type. 
From this we know we can iterate on types of dosings for PPA type, to produce required
text information.

Write function for only PPA type first, can expand to other two types later.
"""

def drugsearchppa(D):
    Z = str(D)
    index = "A"
    dosings = ['Adult', 'Geriatric', 'Pediatric', 'Renal Impairment', 'Hepatic Impairment']
    
    for y,x in enumerate(drug):
        if x["name"] == Z:
            index = y
        
    if index == "A":
        print("Could not find drug.")
        return
    
    print("name:","Z")
        
    for j in range(0,2):    ##for adult to pediatric
        try:
            string = drug[index]["details"]["sections"]["".join(["Dosing: ", dosings[j]])]
            paragraph = re.compile('\<p\>(.*?)\<\/p\>').split(string)
            paragraph = list(filter(None, paragraph))
            for i in range(0,len(paragraph)):
                try:
                    print ("{")
                    print ("age_group:", dosings[j])
                    try:
                        print ("indications:",re.findall('\<b\>(.*?)\<\/b\>',string)[i])
                    except IndexError:
                        print ("indications:","null")
                    print ("special condition:", "null")
                    print ("dosage:", re.sub('\<b\>(.*?)\<\/b\>',"",paragraph[i]))
                    print ("}")
                except IndexError:
                    break
        except KeyError:
            exit
            
    for j in range(3,len(dosings)):    ##for renal to hepatic
        try:
            string = drug[index]["details"]["sections"]["".join(["Dosing: ", dosings[j]])]
            paragraph = re.compile('\<p\>(.*?)\<\/p\>').split(string)
            paragraph = list(filter(None, paragraph))
            print ("{")
            print ("age_group:", "Adult")
            print ("indications:","null")
            print ("special condition:", dosings[j])
            print ("dosage:", ("".join(paragraph)))
            print ("}")
        except KeyError:
            exit
        
            
        
"""
2 Hour time limit up. Created a function that was able to search and find PPA versions of drugs, and 
create a list of the dosages of the drugs for varying types.

Could not write up and sort for indication, as the PPA version seems to lack indicatiors.
Was able to label for age group.

Need to write up Monograph and Pro versions.
Need to learn how to manipulate HTML as to have a nicer looking output.
Need to better learn how to manipulate JSON.
Much to learn. 
"""
        
"""
Will attempt to use Regex to extract the required data out.
try/exit is not convention
Convert to print statements instead of storing memory
print (json.dumps(drug[4]["details"]["sections"], indent=4, sort_keys=True))
this prints the adequate parts
Use regex to extract out HTML bits

"""
dosings = ['Adult', 'Geriatric', 'Pediatric', 'Renal Impairment', 'Hepatic Impairment']
string = drug[4]["details"]["sections"]["".join(["Dosing: ", dosings[0]])]
paragraph = re.compile('\<p\>(.*?)\<\/p\>').split(string)
paragraph = list(filter(None, paragraph))

"""
Above is able to extract individual paragraphs with seperate indications
stored in paragraph
Need to produce output like appendix
Extract title as well
"""

    
"""
Function works, but Renal and Hepatic Impairment for PPA don't fit the initial
sorting method. Need to sort by CrCl(?) instead of by <p>, and impairment
instead of <p>.
"""

def drugsearchppa(D):
    Z = str(D)
    index = "A"
    dosings = ['Adult', 'Geriatric', 'Pediatric', 'Renal Impairment', 'Hepatic Impairment']
    
    for y,x in enumerate(drug):
        if x["name"] == Z:
            index = y
        
    if index == "A":
        print("Could not find drug.")
        return
    
    print("name:","Z")
        
    for j in range(0,2):    ##for adult to pediatric
        try:
            string = drug[index]["details"]["sections"]["".join(["Dosing: ", dosings[j]])]
            paragraph = re.compile('\<p\>(.*?)\<\/p\>').split(string)
            paragraph = list(filter(None, paragraph))
            for i in range(0,len(paragraph)):
                try:
                    print ("{")
                    print ("age_group:", dosings[j])
                    try:
                        print ("indications:",re.findall('\<b\>(.*?)\<\/b\>',string)[i])
                    except IndexError:
                        print ("indications:","null")
                    print ("special condition:", "null")
                    print ("dosage:", re.sub('\<b\>(.*?)\<\/b\>',"",paragraph[i]))
                    print ("}")
                except IndexError:
                    break
        except KeyError:
            exit
    for j in range(3,len(dosings)):    ##for renal to hepatic
        try:
            string = drug[index]["details"]["sections"]["".join(["Dosing: ", dosings[j]])]
            paragraph = re.compile('\<p\>(.*?)\<\/p\>').split(string)
            paragraph = list(filter(None, paragraph))
            print ("{")
            print ("age_group:", "Adult")
            print ("indications:","null")
            print ("special condition:", dosings[j])
            print ("dosage:", ("".join(paragraph)))
            print ("}")
        except KeyError:
            exit
        
"""
Edited our initial function to actually produce the required Appendix
result. Function does not look pythonic however, would like to
figure out a nicer way to put this.
"""