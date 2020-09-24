#!/usr/bin/env python -B
from watcher.github import organization
from watcher.curtain import analyze, rule
from loguru import logger


def main():
    logger.info("Who watches the watcher?")
    analyze(organization)
    # Turn grade into percentage
    grade = max( int(round(((rule.count - rule.grade - len(organization.error))/max(rule.count, 1)) * 100)), 0)

    if grade >= 80:
        logger.success('You have a passing grade: {}%', grade)
    elif grade >= 60:
        logger.warning('You have some work to do: {}%', grade)
    else:
        logger.error('You shame your family: {}%', grade)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
    except Exception:
        import traceback
        traceback.print_exc()
        raise SystemExit(1)
