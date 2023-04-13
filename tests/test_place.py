#
# This file is part of pleiades_python
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2023 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
Test pleiades_python.place module
"""

import logging
from pathlib import Path
from pleiades_python.gazetteer import Gazetteer
from pleiades_python.place import Place
from pytest import raises
from requests.exceptions import HTTPError
from shutil import rmtree

logger = logging.getLogger(__name__)

CACHE_DIR = "tests/data/cache/"


class TestPlaceInit:
    @classmethod
    def setup_class(cls):
        Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)
        cls.g = Gazetteer(cache_dir=CACHE_DIR)

    @classmethod
    def teardown_class(cls):
        # rmtree(Path(CACHE_DIR), ignore_errors=True)
        pass

    def test_init_defaults(self):
        place_uri = "https://pleiades.stoa.org/places/295374"
        p = Place(self.g.webi, place_uri)
        assert p.title == "Zucchabar"
        assert p.uri == place_uri

    def test_init_empty(self):
        p = Place()
        assert p.webi is None
        assert p.data is None
