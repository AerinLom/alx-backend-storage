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


def call_history(method: Callable) -> Callable:
    """
    Decorator to store history of inputs and outputs for a particular function
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Wrapper function that stores input arguments and output in Redis lists
        """
        if isinstance(self._redis, redis.Redis):
            input_k = f"{method.__qualname__}:inputs"
            output_k = f"{method.__qualname__}:outputs"
            self._redis.rpush(input_k, str(args))
            output_result = method(self, *args, **kwargs)
            self._redis.rpush(output_k, output_result)

            return output_result
    return wrapper


def replay(fn: Callable) -> None:
    """
    Display the history of calls of a particular function
    """
    if fn is None or not hasattr(fn, '__self__'):
        return

    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return

    fxn_name = fn.__qualname__
    input_k = '{}:inputs'.format(fxn_name)
    output_k = '{}:outputs'.format(fxn_name)

    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))

    print('{} was called {} times:'.format(fxn_name, fxn_call_count))

    inputs = redis_store.lrange(input_k, 0, -1)
    outputs = redis_store.lrange(output_k, 0, -1)

    for inp, out in zip(inputs, outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            inp.decode('utf-8'),
            out.decode('utf-8')
        ))


class Cache:
    def __init__(self):
        """
        Initialize the Cache class with a Redis client instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with random key and return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
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
