from loguru import logger

# silly decorator to count all rules dynamically
class rule(object):

    count = 0
    grade = 0
    skip = False

    def __init__(self, *args, **kwargs):
        self.skip = False
        # This could be done better...
        if len(args) > 0:
            type(self).skip = args[0]
        if 'skip' in kwargs:
            type(self).skip = kwargs['skip']

    def __call__(self, func):
        if type(self).skip:
            logger.warning('Skipping {}', func.__name__)
            return

        def wrapper(*args, **kwargs):
            type(self).count += 1

            # handle if user forgot to return cleanly
            value = func(*args, **kwargs)
            if value is not None:
                type(self).grade += value
            return
        return wrapper

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
