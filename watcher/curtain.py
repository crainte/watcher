from loguru import logger

import json


# silly decorator to count all rules dynamically
class rule(object):

    count = 0
    grade = 0

    def __init__(self, func):
        self.__func = func

    def __call__(self, *args, **kwargs):
        type(self).count += 1

        # handle if user forgot to return cleanly
        value = self.__func(*args, **kwargs)
        if value is not None:
            type(self).grade += value
        return

def analyze(org):
    import watcher.rules as rules
    tests = []
    for func in dir(rules):
        item = getattr(rules, func)
        if callable(item) and func.startswith('test'):
            tests.append(item)

    for repo in org.active:
        for func in tests:
            func(org.active[repo])
