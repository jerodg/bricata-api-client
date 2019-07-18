#!/usr/bin/env python3.8
"""Bricata API Client: Test Login
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
import time

import pytest
from os import getenv

from base_api_client import bprint, Results, tprint
from bricata_api_client import BricataApiClient


@pytest.mark.asyncio
async def test_logout():
    ts = time.perf_counter()

    bprint('Test: Logout')
    with BricataApiClient(cfg=f'{getenv("HOME")}/.config/bricata_api_client.toml') as bac:
        await bac.login()
        print('Header after login:', bac.header)

        results = await bac.logout()

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure

        print('Header after logout:', bac.header)

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
