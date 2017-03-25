#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

EXCLUDE = ['import_uuid','wikipedia']

mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Rd" : "Road",
            "Rd.": "Road" 
            }

states = { "IN" : "INDIANA",
           "IL" : "ILLINOIS"
         }



def update_name(name, mapping):

    str = name.split(" ")
    i=1
    l = len(str)
    for a in mapping:
        while(i < l):
            if( a == str[i]):
                name =name.replace(str[i],mapping[a])       
            i +=1
        i=1
            
    #print name
    return name

def update_state(name, states):
    for a in states:
        if(name == a):
            name =states[a]      
            
    return name


def key_type(element, keys):
    if element.tag == "tag":
        #print element.tag
        attr_k = element.attrib['k']
        if (re.search(lower,attr_k)):
            keys['lower'] += 1
        elif (re.search(lower_colon,attr_k)):
            keys['lower_colon'] += 1
        elif (re.search(problemchars,attr_k)):
            keys['problemchars'] += 1 
        else:
            keys['other'] += 1
        
    return keys



def process_tags(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for event, element in ET.iterparse(filename):
        keys = key_type(element, keys)
        
    return keys



def shape_element(element,t):
    
    node = {}
    address={}
    gnis={}
    created={}
    pos=["",""]
    node_refs=[]
    if element.tag == "node" or element.tag == "way" :
        #print element.attrib
        node['type']=element.tag
        for attr in element.attrib:
            
            for attr in element.attrib:
                
                if( attr in CREATED):
                    created[attr]=element.attrib[attr]
                else:
                    if (attr == 'lat' or attr == 'lon'):
                        if(attr == 'lat' ):
                            pos[0]=element.attrib[attr]
                        elif(attr == 'lon'):
                            pos[1]=element.attrib[attr]
                    else:
                        node[attr]=element.attrib[attr]
        for tag in element.iter("tag"):
            
            str= (tag.attrib['k']).split(":")
            
            if(len(str) == 2):
                if(str[0]=='addr'):
                    if (str[1] == 'state'):
                        
                        address[str[1]]=update_state(tag.attrib['v'],states)
                    elif(str[1] == 'street'):
                        
                        address[str[1]]=update_name(tag.attrib['v'],mapping)
                    else:
                        
                        address[str[1]] = tag.attrib['v']
                if(str[0]=='gnis'):
                    gnis[str[1]]= tag.attrib['v']
                if(str[0] == 'census'):
                    population = (tag.attrib['v']).split(";")
                    node['population']=population[0]
            elif(len(str) < 2):   
                
                if tag.attrib['k'] not in EXCLUDE:
                    if tag.attrib['k'] == 'is_in':
                        
                        is_in = (tag.attrib['k']).split(",")
                        if (len(is_in) > 1):
                            address['state'] = is_in[1]
                            address['city'] = is_in[0]
                    if(tag.attrib['k'] == 'postal_code'):
                        if(re.match(r'^\d{5}$', tag.attrib['k'])):
                            address['postal_code'] = tag.attrib['v']
                    else:
                        node[tag.attrib['k']]=tag.attrib['v']
        for tag in element.iter("nd"):
           
            if(tag.attrib['ref'] != 'NULL' or tag.attrib['ref'] != ""):
                node_refs.append(tag.attrib['ref'])
                
    if gnis:
        node['gnis'] = gnis
    if created:
        node['created'] = created
    if address:
        node['address'] = address
    if (pos[0] != "" and pos[1] !=""):
        node['pos'] = pos
    if node_refs:
        node['node_refs'] = node_refs
        
    return node


def process_map(file_in, pretty = True):
    t=0
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for event, element in ET.iterparse(file_in):
            t +=1
            el = shape_element(element,t)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    keys = process_tags('/Users/shubhambhardwaj/Downloads/osm files/chicago_illinois_sample.osm')
    pprint.pprint(keys)
    data = process_map('/Users/shubhambhardwaj/Downloads/osm files/chicago_illinois_sample.osm', True)
    pprint.pprint(data[0])
    
    
if __name__ == "__main__":
    test()
