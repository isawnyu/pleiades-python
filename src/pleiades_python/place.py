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
from webiquette.webi import Webi

logger = logging.getLogger(__name__)


class Place:
    def __init__(self, webi: Webi = None, place_uri: str = ""):
        self.webi = webi
        self.data = None
        if place_uri:
            self.update(place_uri)

    def update(self, place_uri: str, bypass_cache: bool = False) -> str:
        """fetch JSON from server and parse"""
        r = self.webi.get(place_uri + "/json", bypass_cache=bypass_cache)
        self.data = r.json()
        self.title = self.data["title"]
        self.uri = self.data["uri"]
        return self.uri
