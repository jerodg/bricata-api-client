#!/usr/bin/env python3.8
"""Base API Client: Models.Alerts
Copyright © 2019 Jerod Gawne <https://github.com/jerodg/>

This program is free software: you can redistribute it and/or modify
it under the terms of the Server Side Public License (SSPL) as
published by MongoDB, Inc., either version 1 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
SSPL for more details.

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

You should have received a copy of the SSPL along with this program.
If not, see <https://www.mongodb.com/licensing/server-side-public-license>."""

import datetime as dt
import logging
from dataclasses import dataclass
from typing import Union

from delorean import parse

logger = logging.getLogger(__name__)


@dataclass
class AlertsFilter:
    """
    Attributes:
        start_time (Optional[Union[str, delorean.Delorean, datetime.timedelta]]): RFC 3339 date
        end_time (Optional[Union[str, delorean.Delorean, datetime.timedelta]]): RFC 3339 date
        sort (Optional[str]):
        tags (Optional[str]):
        tags_op (Optional[str]):
        json_filter (Optional[str]):
        group (Optional[str]):
        limit (Optional[int]):
        offset (Optional[int]):

    References:
        https://tools.ietf.org/html/rfc3339
    """
    start_time: Union[dt.datetime, str] = None
    end_time: Union[dt.datetime, str] = None
    sort: str = None
    tags: str = None
    tags_op: str = None
    json_filter: str = None
    group: str = None
    limit: int = None
    offset: int = None

    def __post_init__(self):
        if self.start_time:
            if type(self.start_time) is str:
                self.start_time = parse(self.start_time).datetime

            if type(self.start_time) is dt.datetime:
                self.start_time = self.start_time.strftime(fmt='%Y-%m-%dT%H:%M:%S.%f%z')

        if self.end_time:
            if type(self.end_time) is str:
                self.end_time = parse(self.end_time).datetime

            if type(self.end_time) is dt.datetime:
                self.end_time = self.end_time.strftime(fmt='%Y-%m-%dT%H:%M:%S.%f%z')

    @property
    def dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}
