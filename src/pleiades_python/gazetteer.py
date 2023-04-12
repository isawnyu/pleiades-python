#
# This file is part of pleiades_python
# by Tom Elliott for the Institute for the Study of the Ancient World
# (c) Copyright 2023 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
Defines Gazetteer class, which wraps all interaction with the web application
"""

from importlib.metadata import version
import logging
from webiquette.webi import Webi

logger = logging.getLogger(__name__)

DEFAULT_USER_AGENT = f"PleiadesPython/{version('pleiades_python')}"


class Gazetteer:
    def __init__(self, user_agent: str = DEFAULT_USER_AGENT, headers: dict = {}):
        self.headers = self._validate_headers(headers)
        ua = user_agent
        if not ua or ua == DEFAULT_USER_AGENT:
            try:
                ua = self.headers["User-Agent"]
            except KeyError:
                pass
        self.headers["User-Agent"] = self._validate_user_agent(ua)

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
