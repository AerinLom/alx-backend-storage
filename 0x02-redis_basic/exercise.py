#!/usr/bin/env python3
"""
This module provides a Cache class that interfaces with Redis
"""
import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        """Initialize the Cache class with a Redis client instance."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with random key and return the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
