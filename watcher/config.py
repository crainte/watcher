import sys

from oslo_config import cfg

common_opts = [
    cfg.BoolOpt('debug', default=False,
                help='Enable debug behavior'),
    cfg.StrOpt('token', default='',
                help='GitHub personal access token'),
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
]

audit_group = cfg.OptGroup('audit', title='Audit Rules',
                           help='Rules to Audit Organizations')

audit_opts = [
    cfg.StrOpt('default_branch', default='master',
               help='Expected Default Branch Name'),
    cfg.BoolOpt('error_on_branch', default=False,
                help='If default_branch Check is an Error or Warning'),
    cfg.IntOpt('max_branches', default=10,
               help='Maximum Number of Branches'),
]

CONF = cfg.CONF
CONF.register_group(github_group)
CONF.register_group(audit_group)

CONF.register_opts(common_opts)
CONF.register_opts(github_opts, github_group)
CONF.register_opts(audit_opts, audit_group)

CONF(project='watcher')
