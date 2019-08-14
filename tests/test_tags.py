#!/usr/bin/env python3.8
"""Bricata API Client: Test Tags
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
from bricata_api_client.models import TagRequest


@pytest.mark.asyncio
async def test_get_tags():
    ts = time.perf_counter()

    bprint('Test: Get Tags')
    async with BricataApiClient(cfg=f'{getenv("CFG_HOME")}/bricata_api_client.toml') as bac:
        results = await bac.get_tags()

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_put_tag():
    ts = time.perf_counter()

    bprint('Test: Put Tag')
    async with BricataApiClient(cfg=f'{getenv("CFG_HOME")}/bricata_api_client.toml') as bac:
        tag = TagRequest(name='sea_test', color='#ff9800', icon='fas fa-grimace')

        results = await bac.put_tag(tag=tag)

        assert type(results) is Results
        assert not results.failure

        results = await bac.get_tags()

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tags = [t['name'] for t in results.success]
        assert 'sea_test' in tags  # Check if tag was created

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_delete_tag():
    ts = time.perf_counter()

    bprint('Test: Delete Tag')
    async with BricataApiClient(cfg=f'{getenv("CFG_HOME")}/bricata_api_client.toml') as bac:
        results = await bac.delete_tag(tag_name='sea_test')

        assert type(results) is Results
        assert not results.failure

        results = await bac.get_tags()

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tags = [t['name'] for t in results.success]
        assert 'sea_test' not in tags  # Check if tag was deleted

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
