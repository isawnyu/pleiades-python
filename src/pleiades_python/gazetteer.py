#
# This file is part of pleiades_python
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2023 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
Defines Gazetteer class, which wraps all interaction with the web application
"""

from datetime import timedelta
from importlib.metadata import metadata
import logging
from platformdirs import user_cache_dir
from pleiades_python.place import Place
from pleiades_python.index import Index
from pleiades_search_api.search import Query, SearchInterface
from urllib.parse import urlparse
from validators import url as uri
from webiquette.webi import Webi

logger = logging.getLogger(__name__)

package_metadata = metadata("pleiades_python")

DEFAULT_CACHE_CONTROL = False
DEFAULT_CACHE_DIR = user_cache_dir(package_metadata["Name"]) + "/webi_cache/"
DEFAULT_EXPIRE_AFTER = timedelta(days=1)
DEFAULT_RESPECT_ROBOTS_TXT = True
DEFAULT_USER_AGENT = f"PleiadesPython/{package_metadata['Version']}"


class Gazetteer:
    def __init__(
        self,
        user_agent: str = DEFAULT_USER_AGENT,
        headers: dict = {},
        respect_robots_txt: bool = DEFAULT_RESPECT_ROBOTS_TXT,
        cache_control: bool = DEFAULT_CACHE_CONTROL,
        expire_after: timedelta = DEFAULT_EXPIRE_AFTER,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ):
        self.headers = self._validate_headers(headers)
        ua = user_agent
        if not ua or ua == DEFAULT_USER_AGENT:
            try:
                ua = self.headers["User-Agent"]
            except KeyError:
                pass
        self.headers["User-Agent"] = self._validate_user_agent(ua)
        self.webi = Webi(
            "pleiades.stoa.org",
            headers=self.headers,
            respect_robots_txt=respect_robots_txt,
            cache_control=cache_control,
            expire_after=expire_after,
            cache_dir=cache_dir,
        )
        self.places = dict()
        self._indexes = {"titles": Index("title")}

    def get_place(
        self, pid: str, reload: bool = False, bypass_cache: bool = False
    ) -> str:
        place_uri = self.valid_pid(pid)
        do_load = reload
        try:
            p = self.places[place_uri]
        except KeyError:
            do_load = True
        if do_load:
            p = Place(self.webi, place_uri=place_uri)
            self.places[place_uri] = p
            self.reindex(p)
        return p

    def lookup(self, index_name: str, terms: list | str, operator: bool = "or") -> set:
        if isinstance(terms, str):
            return self._indexes[index_name].lookup_term(terms)
        else:
            return self._indexes[index_name].lookup_terms(terms, operator=operator)

    def reindex(self, place: Place):
        for idx in self._indexes.values():
            idx.update(place)

    def search(self, query: Query):
        try:
            si = self.search_interface
        except AttributeError:
            self.search_interface = SearchInterface(webi=self.webi)
            si = self.search_interface
        return si.search(query)

    def valid_pid(self, pid: str, bypass_cache: bool = False) -> str:
        """
        Determine if place ID is valid
        - Checks for format (either integer or full Pleiades place URI
            - If bad, raises ValueError
        - Issues an HTTP HEAD request
            - If 200, returns URI
            - If redirect, follows and returns final URI
            - If error, raises error from Requests package
        """
        if not uri(pid):
            try:
                int(pid)
            except:
                raise
            else:
                place_uri = f"https://pleiades.stoa.org/places/{pid}"
        else:
            parts = urlparse(pid)
            path_parts = parts.path.split("/")
            if (
                parts.netloc == "pleiades.stoa.org"
                and len(path_parts) == 3
                and path_parts[0] == ""
                and path_parts[1] == "places"
            ):
                try:
                    int(path_parts[2])
                except:
                    raise
                else:
                    place_uri = pid
            else:
                raise ValueError(pid)
        r = self.webi.head(place_uri, allow_redirects=True)
        return r.url

    def _validate_headers(self, headers: dict) -> dict:
        """Validate any custom headers added by the user"""
        clean_headers = dict()
        for k, v in headers.items():
            if k not in ["From", "Referer", "User-Agent"]:
                logger.error(f"Unsupported HTTP request header '{k}' suppressed.")
                continue
            if not isinstance(v, str):
                raise TypeError(
                    f"Unexpected type for custom HTTP request header '{k}'."
                    f"Expected str, got {type(v)}"
                )
            value = v.strip()
            if not value:
                raise KeyError(
                    "Unacceptable key for custom HTTP request header "
                    f"'{k}'. Expected a non-zero-length string, got ''."
                )
            clean_headers[k] = value
        return clean_headers

    def _validate_user_agent(self, user_agent: str) -> str:
        """Ensure the user agent is a non-zero-length string"""
        if not isinstance(user_agent, str):
            raise TypeError(
                "Unexpected type for user_agent parameter. Expected str, "
                f"got {type(user_agent)}"
            )
        ua = user_agent.strip()
        if ua == DEFAULT_USER_AGENT:
            logger.warning(
                f"Using default user-agent ({user_agent}) for all requests "
                "to the Pleiades gazetteer website. We strongly prefer you "
                "define your own unique user-agent string and pass it to "
                "the Gazetteer class at instantiation."
            )
        elif not ua:
            raise ValueError(
                f"Unacceptable value for user_agent parameter. Expected a "
                "non-zero-length string, got ''."
            )
        return ua
