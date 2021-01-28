from watcher import __version__
from watcher.github import organization
from oslo_config import cfg
from oslo_config import fixture as config

import pytest

class MockResponse:
    @staticmethod
    def generateAuthHeader():
        return

    def get_repo(self):
        return '{"name": "test"}'

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Remove requests.sessions.Session.request for all tests."""
    monkeypatch.delattr("requests.sessions.Session.request")

def test_version():
    assert __version__ == '0.4.0'

def test_github_client():
    conf = cfg.ConfigOpts()
    config_fixture = config.Config(conf)
    config_fixture.setUp()
    config_fixture.register_opt(cfg.StrOpt(
        'testing_option', default='initial_value'))
    config_fixture.register_opt(cfg.IntOpt(
        'test2', min=0, default=5))
    config_fixture.register_opt(cfg.StrOpt(
        'test3', choices=['a', 'b'], default='a'))

    assert f.conf.get('testing_option') == 'ok'
    assert len(organization.active) == 1
