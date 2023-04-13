#
# This file is part of pleiades_python
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2023 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
Define the Place class
"""

import logging
from validators import url as uri
from webiquette.webi import Webi

logger = logging.getLogger(__name__)


class Place:
    def __init__(self, webi: Webi = None, place_uri: str = ""):
        self.webi = webi
        self.data = None
        if place_uri:
            self.update(place_uri)

    def update(self, place_uri: str):
        r = self.webi.get(place_uri + "/json")
        self.data = r.json()
