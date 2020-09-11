#!/usr/bin/env python -B
from watcher.github import organization
from watcher.config import cfg
from watcher.curtain import analyze, rule
from loguru import logger

import json
import backoff
import argparse


CONF = cfg.CONF


def main():
    logger.info("Who watches the watcher?")
    analyze(organization)
    logger.warning('ACTIVE: {} COUNT: {} GRADE: {}', len(organization.active), rule.count, rule.grade)
    # Turn grade into percentage
    grade = int(round( ( (rule.count - rule.grade - len(organization.error))/rule.count ) * 100))

    if grade >= 80:
        logger.success('You have a passing grade: {}', grade)
    elif grade >= 60:
        logger.warning('You have some work to do: {}', grade)
    else:
        logger.error('You shame your family: {}', grade)


if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
    except Exception:
        import traceback
        traceback.print_exc()
        raise SystemExit(1)
