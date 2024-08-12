#!/usr/bin/env python3
"""
Function that changes all topics of a school document based on the name.
"""
from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    """
    Updates the 'topics' field of a school document where 'name' matches.
    """
    mongo_collection.update_one(
        {'name': name},
        {'$set': {'topics': topics}}
    )
