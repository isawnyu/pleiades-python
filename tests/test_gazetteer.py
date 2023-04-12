#
# This file is part of pleiades_python
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2023 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
Test pleiades_python.gazetteer module
"""

from datetime import datetime
from pleiades_python.gazetteer import Gazetteer
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

    def test_init(self):
        pass
