#
# This file is part of pleiades_python
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2023 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
Define the Index class (an index of places by term)
"""

import logging
from pleiades_python.place import Place

logger = logging.getLogger(__name__)


class Index:
    def __init__(self, attribute_name: str):
        self.attribute_name = attribute_name
        self._terms2places = dict()
        self._uris2terms = dict()

    def lookup_term(self, term: str) -> dict:
        try:
            return set(self._terms2places[term].keys())
        except KeyError:
            return dict()

    def lookup_terms(self, terms: list, operator: str = "or") -> dict:
        valid = ["and", "or"]
        if operator not in valid:
            raise ValueError(
                f"Expected operator value from {valid}, but got '{operator}'"
            )
        place_sets = [set(self._terms2places(t).keys()) for t in terms]
        result = set()
        for ps in place_sets:
            if operator == "and":
                result = result.intersection(ps)
            elif operator == "or":
                result = result.union(ps)
        return result

    def remove(self, place: Place):
        """Remove all references to this place from the index"""
        try:
            terms = self._uris2terms[place.uri]
        except KeyError:
            pass
        else:
            for t in terms:
                del self._terms2places[t][place.uri]
            del self._uris2terms[place.uri]

    def update(self, place: Place):
        """Update the index with information about this place"""
        self.remove(place)
        values = getattr(place, self.attribute_name)
        if isinstance(values, str):
            self._update_term(values, place)
        elif isinstance(values, list):
            for v in values:
                self._update_term(v, place)

    def _update_term(self, term: str, place: Place):
        try:
            self._terms2places[term]
        except KeyError:
            self._terms2places[term] = dict()
        self._terms2places[term][place.uri] = place
        try:
            self._uris2terms[place.uri]
        except KeyError:
            self._uris2terms[place.uri] = set()
        self._uris2terms[place.uri].add(term)
