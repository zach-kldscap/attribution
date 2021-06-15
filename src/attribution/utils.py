from functools import wraps
import time

from tycho.config import logger

def profile(debug):
    def _profile(func):
        if not debug: return func

        @wraps(func)
        def wrapper(*args, **kargs):
            tok = time.time()
            res = func(*args, **kargs)
            logger.profile("%s: %s", func.__name__.ljust(30), time.time() - tok)
            return res
        return wrapper
    return _profile
