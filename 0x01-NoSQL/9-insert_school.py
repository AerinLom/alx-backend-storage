#!/usr/bin/env python3
"""
Function that inserts a new document in a collection,
based on kwargs.
"""
from pymongo import MongoClient

def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection.
    """
    insert_result = mongo_collection.insert_one(kwargs)
    return insert_result.inserted_id
