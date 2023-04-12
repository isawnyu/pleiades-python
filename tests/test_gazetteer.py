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
from shutil import rmtree

import logging

logger = logging.getLogger(__name__)

CACHE_DIR = "tests/data/cache/"
TEMP_DIR = "tests/data/temp/"


class TestGazetteer:
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_init_defaults(self):
        g = Gazetteer()
        h = g.headers
        assert isinstance(h, dict)
        assert len(h) == 1
        assert h["User-Agent"] == DEFAULT_USER_AGENT

    def test_init_user_agent(self):
        s = "SuperPleiadesFunBot/8675309"
        g = Gazetteer(user_agent=s)
        assert g.headers["User-Agent"] == s

    def test_init_user_agent_in_header(self):
        s = "SuperPleiadesFunBot/8675309"
        g = Gazetteer(headers={"User-Agent": s})
        assert g.headers["User-Agent"] == s

    def test_init_user_agent_override(self):
        s = "SuperPleiadesFunBot/8675309"
        g = Gazetteer(user_agent=s, headers={"User-Agent": "PleiadesFishBot/42"})
        assert g.headers["User-Agent"] == s

    def test_init_custom_header(self):
        m = "marvin@end.universe.restaurant"
        g = Gazetteer(headers={"From": m})
        assert g.headers["From"] == m

    def test_init_suppress_unsupported_header(self):
        g = Gazetteer(headers={"Vorpal": "bunny"})
        with raises(KeyError):
            g.headers["Vorpal"]
