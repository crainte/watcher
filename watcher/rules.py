from loguru import logger
from watcher.curtain import rule
from watcher.config import cfg

import json


CONF = cfg.CONF

# Place your rules for validating here
# * You MUST start the function name with 'test'
# * If you want your rule graded return 0 for success, 1 for failure

@rule()
def test_active_branch_count(repo):
    if len(repo['branches']) > CONF.audit.max_branches:
        if CONF.enforce.max_branches:
            logger.error('{} exceeds max branches limit {} > {}', repo['name'], len(repo['branches']), CONF.audit.max_branches)
            return 1
        else:
            logger.warning('{} exceeds max branches limit {} > {}', repo['name'], len(repo['branches']), CONF.audit.max_branches)
            return
    logger.info('{} has {} branches', repo['name'], len(repo['branches']))

@rule()
def test_default_branch_name(repo):
    if repo['default_branch'] != CONF.audit.default_branch:
        if CONF.enforce.default_branch:
            logger.error('{} has an invalid default branch: {}', repo['name'], repo['default_branch'])
            return 1
        else:
            logger.warning('{} has an unexpected default branch: {}', repo['name'], repo['default_branch'])
            return
    logger.success('{} has the expected default branch: {}', repo['name'], repo['default_branch'])

@rule()
def test_require_status_checks(repo):
    if 'required_status_checks' not in repo['protections']:
        if CONF.enforce.checks:
            logger.error('{} has no required status checks', repo['name'])
            return 1
        else:
            logger.warning('{} has no required status checks', repo['name'])
            return
    logger.success('{} requires status checks', repo['name'])

@rule()
def test_require_strict_status_checks(repo):
    if 'required_status_checks' not in repo['protections'] or not repo['protections']['required_status_checks']['strict']:
        if CONF.enforce.strict_checks:
            logger.error('{} does not strictly require checks', repo['name'])
            return 1
        else:
            logger.warning('{} does not strictly require checks', repo['name'])
            return
    logger.success('{} strictly requires status checks', repo['name'])

@rule()
def test_require_pull_request_reviews(repo):
    if 'required_pull_request_reviews' not in repo['protections']:
        if CONF.enforce.reviews:
            logger.error('{} has no required pull request review rules', repo['name'])
            return 1
        else:
            logger.warning('{} has no required pull request review rules', repo['name'])
            return
    logger.success('{} requires pull request reviews', repo['name'])

@rule()
def test_require_code_owner_reviews(repo):
    if 'required_pull_request_reviews' not in repo['protections'] or not repo['protections']['required_pull_request_reviews']['require_code_owner_reviews']:
        if CONF.enforce.code_owners:
            logger.error('{} does not require code owner reviews', repo['name'])
            return 1
        else:
            logger.warning('{} does not require code owner reviews', repo['name'])
            return
    logger.success('{} requires code owner reviews', repo['name'])

@rule()
def test_dismiss_stale_reviews(repo):
    if 'required_pull_request_reviews' not in repo['protections'] or not repo['protections']['required_pull_request_reviews']['dismiss_stale_reviews']:
        if CONF.enforce.stale_reviews:
            logger.error('{} does not dismiss stale reviews', repo['name'])
            return 1
        else:
            logger.warning('{} does not dismiss stale reviews', repo['name'])
            return
    logger.success('{} dismisses stale reviews', repo['name'])

@rule()
def test_enforce_admins(repo):
    if not repo['protections']['enforce_admins']['enabled']:
        if CONF.enforce.admin:
            logger.error('{} does not force administrators', repo['name'])
            return 1
        else:
            logger.warning('{} does not force administrators', repo['name'])
            return
    logger.success('{} forces administrators', repo['name'])

@rule()
def test_require_linear_history(repo):
    if not repo['protections']['required_linear_history']['enabled']:
        if CONF.enforce.linear_history:
            logger.error('{} does not require linear history', repo['name'])
            return 1
        else:
            logger.warning('{} does not require linear history', repo['name'])
            return
    logger.success('{} requires linear history', repo['name'])

@rule()
def test_allow_force_push(repo):
    if repo['protections']['allow_force_pushes']['enabled']:
        if CONF.enforce.force_push:
            logger.error('{} allows force pushes', repo['name'])
            return 1
        else:
            logger.warning('{} allows force pushes', repo['name'])
            return
    logger.success('{} does not allow force pushes', repo['name'])

@rule()
def test_allow_deletions(repo):
    if repo['protections']['allow_deletions']['enabled']:
        if CONF.enforce.delete:
            logger.error('{} allows deletions', repo['name'])
            return 1
        else:
            logger.warning('{} allows deletions', repo['name'])
            return
    logger.success('{} does not allow deletions', repo['name'])

# opposite of the feature flag so we don't need this rule when disabled
@rule(not CONF.github.deep_branch)
def test_stale_branches(repo):
    from datetime import datetime
    now = datetime.now()
    for b in repo['branches']:
        commit = datetime.strptime(repo['branches'][b]['commit']['commit']['committer']['date'], '%Y-%m-%dT%H:%M:%SZ')
        since = now - commit
        if since.days > CONF.audit.branch_days_stale:
            if CONF.enforce.branch_days_stale:
                logger.error('{} branch {} is {} days old', repo['name'], b, since.days)
                return 1
            else:
                logger.warning('{} branch {} is {} days old', repo['name'], b, since.days)
                return
        logger.success('{} branch {} is {} days old', repo['name'], b, since.days)

@rule(not CONF.github.deep_repo)
def test_delete_head(repo):
    if not repo['delete_branch_on_merge']:
        if CONF.enforce.delete_branch_on_merge:
            logger.error('{} does not delete HEAD branch on merge', repo['name'])
            return 1
        else:
            logger.warning('{} does not delete HEAD branch on merge', repo['name'])
            return
    logger.success('{} deletes HEAD branch on merge', repo['name'])
