from agithub.GitHub import GitHub
from watcher.config import cfg
from loguru import logger


CONF = cfg.CONF


class Organization():

    active = {}
    error = {}
    archived = {}
    protected = {}

    def __init__(self):
        logger.debug('Loading Organization: {}', CONF.github.organization)
        self.client = GitHub(token=CONF.github.token, paginate=CONF.github.paginate)
        self.client.generateAuthHeader()
        self._build()

    def _validateCall(self, resource, status, body):
        if status not in [200]:
            logger.error('Unable to load {}: HTTP {} {}', resource, status, body)
            raise Exception

    def _build(self):
        logger.debug('Requesting repositories')
        status, repos = self.client.orgs[CONF.github.organization].repos.get()
        self._validateCall('repositories', status, repos)
        logger.debug('Found {} repos', len(repos))

        for repo in repos:
            # alias full name for easier everything below
            full_name = repo['full_name']
            default_branch = repo['default_branch']

            if repo['archived']:
                self.archived[full_name] = repo
                logger.debug('{} is archived', full_name)
                continue
            # start loading datasource
            self.active[full_name] = repo
            logger.debug('Requesting branches for repo: {}', full_name)
            status, branches = self.client.repos[full_name].branches.get()
            self._validateCall('branches', status, branches)
            self.active[full_name]['branches'] = branches

            # for each branch, if protected == true / this saves an api call at the cost of a nested for
            self.protected = [b for b in branches if b["protected"]]

            logger.debug('Requesting protections for {} default_branch: {}', full_name, default_branch)
            try:
                # TODO handle this better, default branch not protected
                status, protections = self.client.repos[full_name].branches[default_branch].protection.get()
                self._validateCall('protections', status, protections)
                self.active[full_name]['protections'] = protections
            except:
                # Unable to pull protections, we can't run checks against it
                self.error[full_name] = self.active[full_name]
                self.error[full_name]['protections'] = protections
                del self.active[full_name]
            # TODO allow deep branch inspection for stale branches


organization = Organization()
