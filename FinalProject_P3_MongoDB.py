#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 14:11:43 2017

@author: shubhambhardwaj
"""

def get_db():
    
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.openStreet
    return db

def make_pipeline():
    
    pipeline = [ ]
    #match = { "$match": { "$and": [ { "lon": { "$gt": 75, "$lt": 80 } }, { "country": "India" } ] } }
    match = {"$match" :{"created.user": {"$ne": None}}}
    #unwind ={"$unwind" : "$isPartOf"}
    group = {"$group" :{"_id":"$created.user", "count": {"$sum":1}}}
    sort = {"$sort" : {"count":-1}}
    limit = {"$limit":3}
    pipeline = [match,group,sort,limit]
    #print pipeline
    return pipeline

def aggregate1(db, pipeline):
    return [doc for doc in db.NewYork.aggregate(pipeline)]

if __name__ == "__main__":
    import pprint
    db = get_db() 
    print db
    print "Total number of records"
    print db.Chicago.find().count()
    print "Total number of public"
    print db.Chicago.find({"type":"public"}).count()
    print "Total number of multi-storey parking lots"
    print db.Chicago.find({"type":"multi-storey"}).count()
    print "Total number of nodes"
    print db.Chicago.find({"type":"node"}).count()
    print "Total number of ways"
    print db.Chicago.find({"type":"way"}).count()
    print "\n Total number of distinct users"
    distinct_user = db.Chicago.distinct("created.user")
    print (len(distinct_user))
    print "\n Number of distinct highways"
    pprint.pprint(db.Chicago.distinct("highway"))
    print "\n Number of records with user as None"
    result=db.Chicago.aggregate(
            [{"$match" :{"created.user": None}},{"$group": {"_id": "$created.user", "count":  {"$sum": 1}}}, 
             {"$sort": {"count": -1}}])
    for doc in result:
        pprint.pprint(doc)
    print "\n Top 3 contributors"
    pprint.pprint( aggregate1(db,make_pipeline()))
    print "\n Top 10 appearing amenities"
    
    result1=db.Chicago.aggregate(
            [{"$match" :{"amenity":{"$exists":1}}},{"$group":{"_id":"$amenity","count":{"$sum":1}}},
             {"$sort": {"count": -1}} , {"$limit" : 10}])
             
    for doc in result1:
        pprint.pprint(doc)
        
    print "\n Top  cusines"
    result2=db.Chicago.aggregate([
            {"$match":{"amenity":"restaurant"}}, {"$group":{"_id":"$cuisine", "count":{"$sum":1}}},
            {"$sort": {"count": -1}}, {"$limit":2}])
    for doc in result2:
        pprint.pprint(doc)   
    print "\n Top 10 restraunts"
    
    result3=db.Chicago.aggregate(
            [{"$match" :{"amenity":{"$exists":1}, "amenity" :'library', }},
             {"$group":{"_id":"$name","count":{"$sum":1}}},
             {"$sort": {"count": -1}} , {"$limit" : 10}])
              
    for doc in result3:
        pprint.pprint(doc)
        
    print "\n Top 3 schools"
    
    result4=db.Chicago.aggregate(
            [{"$match" :{"amenity":{"$exists":1}, "amenity" :'school', }},
             {"$group":{"_id":"$name","count":{"$sum":1}}},
             {"$sort": {"count": -1}} , {"$limit" : 3}])
              
    for doc in result4:
        pprint.pprint(doc)
                                                      
    
    