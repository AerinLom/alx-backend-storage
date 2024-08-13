#!/usr/bin/env python3
"""
Function that returns the list of schools having a specific topic.
"""
from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
    """
    Returns a list of schools that have the specified topic.
    """
    return list(mongo_collection.find({'topics': topic}))
