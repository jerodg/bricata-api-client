#!/usr/bin/env python3.8
"""Bricata API Client: Models.Query
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
from typing import List, Optional, Union

from copy import deepcopy
from delorean import Delorean, parse

from base_api_client.models import Record, sort_dict


logger = logging.getLogger(__name__)


@dataclass
class Query(Record):
    """
    start_time: (Optional[Union[Delorean, str]])
    end_time: (Optional[Union[Delorean, str]])
    sort: (Optional[str])
    group: (Optional[str])
    limit: (Optional[int])
    offset: (Optional[int]); Which record number to start from"""
    start_time: Optional[Union[Delorean, str]] = None
    end_time: Optional[Union[Delorean, str]] = None
    sort: Optional[str] = None
    group: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


@dataclass
class AlertQuery(Query):
    tags: Optional[str] = None
    tags_op: Optional[str] = None
    # Extras
    id: Optional[str] = None

    def dict(self, cleanup: Optional[bool] = True, dct: Optional[dict] = None, sort_order: Optional[str] = 'asc') -> Union[dict, None]:
        """
        Args:
            cleanup (Optional[bool]):
            dct (Optional[dict]):
            sort_order (Optional[str]): ASC | DESC

        Returns:
            dict (dict):"""
        if self.id:
            return None

        if not dct:
            dct = deepcopy(self.__dict__)

        try:
            del dct['id']
        except KeyError:
            pass

        if cleanup:
            dct = {k: v for k, v in dct.items() if v is not None}

        if sort_order:
            dct = sort_dict(dct, reverse=True if sort_order.lower() == 'desc' else False)

        return dct

    @property
    def end_point(self):
        if self.id:
            return f'/alerts/{self.id}'

        return '/alerts/'

    @property
    def data_key(self):
        if self.id:
            return None

        return 'objects'
