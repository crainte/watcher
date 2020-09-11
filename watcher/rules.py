from loguru import logger
from watcher.curtain import rule
from watcher.config import cfg

import json


CONF = cfg.CONF

# Place your rules for validating here
# * You MUST start the function name with 'test'
# * If you want your rule graded return 0 for success, 1 for failure

@rule
def test_active_branch_count(repo):
    if len(repo['branches']) > CONF.audit.max_branches:
        logger.error('{} exceeds max branches limit {} > {}', repo['name'], len(repo['branches']), CONF.audit.max_branches)
        return 1
    logger.info('{} has {} branches', repo['name'], len(repo['branches']))

@rule
def test_default_branch_name(repo):
    if repo['default_branch'] != CONF.audit.default_branch:
        if CONF.audit.error_on_branch:
            logger.error('{} has an invalid default branch: {}', repo['name'], repo['default_branch'])
            return 1
        else:
            logger.warning('{} has an unexpected default branch: {}', repo['name'], repo['default_branch'])
    logger.success('{} has the expected default branch: {}', repo['name'], repo['default_branch'])

@rule
def test_require_status_checks(repo):
    if 'required_status_checks' not in repo['protections']:
        logger.error('{} has no required status checks', repo['name'])
        return 2
    if not repo['protections']['required_status_checks']['strict']:
        logger.error('{} does not strictly require checks', repo['name'])
        return 1
    logger.success('{} strictly requires status checks', repo['name'])

@rule
def test_require_pull_request_reviews(repo):
    if not repo['protections']['required_pull_request_reviews']['require_code_owner_reviews']:
        logger.error('{} does not require code owner reviews', repo['name'])
        return 1
    logger.success('{} requires code owner reviews', repo['name'])

@rule
def test_dismiss_stale_reviews(repo):
    if not repo['protections']['required_pull_request_reviews']['dismiss_stale_reviews']:
        logger.error('{} does not dismiss stale reviews', repo['name'])
        return 1
    logger.success('{} dismisses stale rewviews', repo['name'])

@rule
def test_enforce_admins(repo):
    if not repo['protections']['enforce_admins']['enabled']:
        logger.error('{} does not force administrators', repo['name'])
        return 1
    logger.success('{} forces administrators', repo['name'])

@rule
def test_require_linear_history(repo):
    if not repo['protections']['required_linear_history']['enabled']:
        logger.error('{} does not require linear history', repo['name'])
        return 1
    logger.success('{} requires linear history', repo['name'])

@rule
def test_allow_force_push(repo):
    if repo['protections']['allow_force_pushes']['enabled']:
        logger.error('{} allows force pushes', repo['name'])
        return 1
    logger.success('{} does not allow force pushes', repo['name'])

@rule
def test_allow_deletions(repo):
    if repo['protections']['allow_deletions']['enabled']:
        logger.error('{} allows deletions', repo['name'])
        return 1
    logger.success('{} does not allow deletions', repo['name'])
