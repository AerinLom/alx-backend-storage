#!/usr/bin/env python3
"""
Python script that provides some stats about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    """
    Prints stats about Nginx request logs
    """
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = len(list(nginx_collection.find({'method': method})))
        print(f"\tmethod {method}: {count}")

    status_checks = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print(f"{status_checks} status check")


def run():
    """
    Provides some stats about Nginx logs stored in MongoDB
    """
    clientConnection = MongoClient('mongodb://localhost:27017')
    database = clientConnection.logs
    nginx_collection = database.nginx

    print_nginx_request_logs(nginx_collection)


if __name__ == "__main__":
    run()
