#!/usr/bin/env python
# coding: utf-8
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

from requests import Response, Session

from .constants import DAY_END, DAY_START, DEFAULT_DAY, DEFAULT_YEAR, URL_PATTERN, YEAR_END, YEAR_START
from .io import get_session_cookie


class AoCSession(Session):
    def __init__(self, *args, **kwargs) -> None:
        super(AoCSession, self).__init__(*args, **kwargs)
        self.headers.update({"User-Agent": "aoc_utils/0.1.0"})
        self.cookies.update(get_session_cookie(raise_on_missing=False))

    def request(
        self, method: str, url: str, *args, raise_for_status: bool = False, **kwargs
    ) -> Response:
        # validate url
        year, day = URL_PATTERN.match(url).groups()
        year = int(year)
        day = int(day)

        # check for year
        if not YEAR_START <= year <= YEAR_END:
            raise ValueError(
                f"Invalid year: {year}. Must be between {YEAR_START} and {YEAR_END}."
            )
        # check for day
        if not DAY_START <= day <= DAY_END:
            raise ValueError(
                f"Invalid day: {day}. Must be between {DAY_START} and {DAY_END}."
            )
        if year == DEFAULT_YEAR:
            if day > DEFAULT_DAY:
                raise ValueError(f"Invalid day: {day} for year {year}. Must be between 1 and {DEFAULT_DAY}.")
            elif day == DEFAULT_DAY and datetime.utcnow().hour - 5 < 0:
                raise ValueError(f"Invalid day: {day} for year {year}. Must be between 1 and {DEFAULT_DAY-1}.")

        resp = super(AoCSession, self).request(method, url, *args, **kwargs)
        if raise_for_status:
            resp.raise_for_status()
        return resp

    def get(self, url: str, raise_for_status: bool = False, **kwargs) -> Response:
        kwargs.setdefault("allow_redirects", True)
        return self.request("GET", url, raise_for_status=raise_for_status, **kwargs)

    def post(
        self,
        url: str,
        data: Optional[Union[Dict[str, str], List[Tuple], bytes]] = None,
        json: Optional[Dict[str, str]] = None,
        raise_for_status: bool = False,
        **kwargs,
    ):
        return self.request(
            "POST",
            url,
            data=data,
            json=json,
            raise_for_status=raise_for_status,
            **kwargs,
        )


# initialize Session
session = AoCSession()
