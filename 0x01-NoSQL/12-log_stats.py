#!/usr/bin/env python3
"""
Python script that provides some stats about Nginx logs
"""
from pymongo import MongoClient


def log_stats():
    """
    provides some stats about Nginx logs stored in MongoDB
    """
    clientConnection = MongoClient('mongodb://localhost:27017/')
    
    database = clientConnection.logs
    nginx_collection = database.nginx
    
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")
    
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    
    status_checks = nginx_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_checks} status check")


if __name__ == "__main__":
    log_stats()
