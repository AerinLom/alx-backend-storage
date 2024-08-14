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

    def get(self,
            key: str, fn: Optional[Callable] = None) -> str:
        """
        Retrieve data from Redis and apply an optional conversion function.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, value: str) -> Optional[str]:
        """Retrieve a string value from Redis."""
        return value.decode('utf-8', 'strict')

    def get_int(self, value: str) -> Optional[int]:
        """Retrieve an integer value from Redis."""
        return int(value)
