import sys

from oslo_config import cfg

common_opts = [
    cfg.BoolOpt('debug', default=False,
               help='Enable debug behavior'),
]

github_group = cfg.OptGroup('github', title='GitHub Options',
                            help='GitHub Configuration Options & Values')

github_opts = [
    cfg.StrOpt('token', default='',
               help='Personal Access Token'),
    cfg.StrOpt('organization', default='',
               help='Organization to scan'),
    cfg.BoolOpt('paginate', default=False,
               help='Paginate responses'),
    cfg.BoolOpt('deep_branch', default=False,
               help='Enable deep branch population'),
]

audit_group = cfg.OptGroup('audit', title='Audit Settings',
                           help='Configure the audit rules')

audit_opts = [
    cfg.StrOpt('default_branch', default='master',
               help='Expected Default Branch Name'),
    cfg.IntOpt('max_branches', default=10,
               help='Maximum Number of Branches'),
    cfg.IntOpt('branch_days_stale', default=30,
               help='Days until considered stale'),
]

enforce_group = cfg.OptGroup('enforce', title='Enforce Rules',
                             help='Error or Warn on rules')

enforce_opts = [
    cfg.BoolOpt('default_branch', default=False,
               help='Enforce default branch name'),
    cfg.BoolOpt('max_branches', default=False,
               help='Enforce maximum branch count'),
    cfg.BoolOpt('branch_days_stale', default=False,
               help='Enforce no stale branches'),
    cfg.BoolOpt('admin', default=False,
               help='Enforce administrator to branch protection'),
    cfg.BoolOpt('linear_history', default=False,
               help='Enforce linear history'),
    cfg.BoolOpt('checks', default=False,
               help='Enforce status checks'),
    cfg.BoolOpt('strict_checks', default=False,
               help='Enforce strict status checks'),
    cfg.BoolOpt('reviews', default=False,
               help='Enforce PR reviews'),
    cfg.BoolOpt('code_owners', default=False,
               help='Enforce code owner reviews'),
    cfg.BoolOpt('stale_reviews', default=False,
               help='Enforce dismissal of stale reviews'),
    cfg.BoolOpt('force_push', default=False,
               help='Enforce force push rules'),
    cfg.BoolOpt('delete', default=False,
               help='Enforce deletion rules'),
]

CONF = cfg.CONF
CONF.register_group(github_group)
CONF.register_group(audit_group)
CONF.register_group(enforce_group)

CONF.register_opts(common_opts)
CONF.register_opts(github_opts, github_group)
CONF.register_opts(audit_opts, audit_group)
CONF.register_opts(enforce_opts, enforce_group)

CONF(project='watcher')
