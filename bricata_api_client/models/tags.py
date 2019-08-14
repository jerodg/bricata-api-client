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

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TagRequest:
    """
    Attributes:
        name(str): Anything you'd like
        color(str): HTML HEX Color Code e.g. #4472D9
        icon(str): Font Awesome Icon

    References:
        https://fontawesome.com
    """
    name: str
    color: str = None
    icon: str = None

    def __post_init__(self):
        pass

    @property
    def dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}
