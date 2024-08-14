#!/usr/bin/env python3
"""
This module provides a Cache class that interfaces with Redis
"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional, Any


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Wrapper function that increments call count then calls original method
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self):
        """
        Initialize the Cache class with a Redis client instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with random key and return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str, fn: Optional[Callable] = None) -> str:
        """
        Retrieve data from Redis and apply an optional conversion function.
        """
        value = self._redis.get(key)
        return fn(value) if fn is not None else value

    def get_str(self, value: str) -> str:
        """
        Retrieve a string value from Redis
        """
        return value.decode('utf-8', 'strict')

    def get_int(self, value: str) -> int:
        """
        Retrieve an integer value from Redis
        """
        return int(value)
