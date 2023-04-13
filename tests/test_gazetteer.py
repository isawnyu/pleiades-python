#
# This file is part of pleiades_python
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2023 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
Test pleiades_python.gazetteer module
"""

from pleiades_python.gazetteer import Gazetteer, DEFAULT_USER_AGENT
from pathlib import Path
from pytest import raises
from requests.exceptions import HTTPError
from shutil import rmtree
from webiquette.webi import Webi


import logging

logger = logging.getLogger(__name__)

CACHE_DIR = "tests/data/cache/"


class TestGazetteerInit:
    @classmethod
    def setup_class(cls):
        Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)

    @classmethod
    def teardown_class(cls):
        # rmtree(Path(CACHE_DIR), ignore_errors=True)
        pass

    def test_init_defaults(self):
        g = Gazetteer(cache_dir=CACHE_DIR)
        h = g.headers
        assert isinstance(h, dict)
        assert len(h) == 1
        assert h["User-Agent"] == DEFAULT_USER_AGENT

    def test_init_user_agent(self):
        s = "SuperPleiadesFunBot/8675309"
        g = Gazetteer(user_agent=s, cache_dir=CACHE_DIR)
        assert g.headers["User-Agent"] == s

    def test_init_user_agent_in_header(self):
        s = "SuperPleiadesFunBot/8675309"
        g = Gazetteer(headers={"User-Agent": s}, cache_dir=CACHE_DIR)
        assert g.headers["User-Agent"] == s

    def test_init_user_agent_override(self):
        s = "SuperPleiadesFunBot/8675309"
        g = Gazetteer(
            user_agent=s,
            headers={"User-Agent": "PleiadesFishBot/42"},
            cache_dir=CACHE_DIR,
        )
        assert g.headers["User-Agent"] == s

    def test_init_custom_header(self):
        m = "marvin@end.universe.restaurant"
        g = Gazetteer(headers={"From": m}, cache_dir=CACHE_DIR)
        assert g.headers["From"] == m

    def test_init_suppress_unsupported_header(self):
        g = Gazetteer(headers={"Vorpal": "bunny"}, cache_dir=CACHE_DIR)
        with raises(KeyError):
            g.headers["Vorpal"]

    def test_init_webi(self):
        g = Gazetteer(cache_dir=CACHE_DIR)
        assert isinstance(g.webi, Webi)


class TestGazetteerMethods:
    @classmethod
    def setup_class(cls):
        Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)
        cls.g = Gazetteer(cache_dir=CACHE_DIR)

    @classmethod
    def teardown_class(cls):
        # rmtree(Path(CACHE_DIR), ignore_errors=True)
        pass

    def test_valid_pid_URI(self):
        pid = "https://pleiades.stoa.org/places/295374"
        uri = self.g.valid_pid(pid)
        assert uri == pid

    def test_invalid_pid_URI(self):
        pid = "https://pleiades.stoa.org/places/0"
        with raises(HTTPError):
            self.g.valid_pid(pid)

    def test_invalid_pid_URI_pid(self):
        pid = "https://pleiades.stoa.org/places/Zucchabar"
        with raises(ValueError):
            self.g.valid_pid(pid)

    def test_valid_pid_integer_string(self):
        pid = "295374"
        uri = self.g.valid_pid(pid)
        assert uri == f"https://pleiades.stoa.org/places/{pid}"

    def test_invalid_pid_noninteger_string(self):
        pid = "Zucchabar"
        with raises(ValueError):
            self.g.valid_pid(pid)

    def test_invalid_pid_integer_string(self):
        pid = "0"
        with raises(HTTPError):
            # format is valid, but there's no such place resource on the server
            self.g.valid_pid(pid)

    def test_redirect(self):
        pid = "https://pleiades.stoa.org/places/1001902"
        uri = self.g.valid_pid(pid)
        assert uri == "https://pleiades.stoa.org/places/991367"
