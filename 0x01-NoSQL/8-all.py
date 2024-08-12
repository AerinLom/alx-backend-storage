#!/usr/bin/env python3
"""
"""
from pymongo import MongoClient


def list_all(mongo_collection):
    """
    Lists all documents in a collection.
    """
    docs = list(mongo_collection.find())
    return docs
