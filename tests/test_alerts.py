#!/usr/bin/env python3.8
"""Bricata API Client: Test Alerts
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
from random import choice

from base_api_client import bprint, Results, tprint
from bricata_api_client import BricataApiClient
from bricata_api_client.models import AlertsFilter


@pytest.mark.asyncio
async def test_get_alerts():
    ts = time.perf_counter()

    bprint('Test: Get Alerts')
    async with BricataApiClient(cfg=f'{getenv("CFG_HOME")}/bricata_api_client.toml') as bac:
        results = await bac.get_alerts()

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_alerts_filtered():
    ts = time.perf_counter()

    bprint('Test: Get Alerts, Filtered')
    async with BricataApiClient(cfg=f'{getenv("CFG_HOME")}/bricata_api_client.toml') as bac:
        af = AlertsFilter(tags='Drop')
        results = await bac.get_alerts(af)

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        tprint(results, top=5)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_get_alert():
    ts = time.perf_counter()

    bprint('Test: Get Alert')
    async with BricataApiClient(cfg=f'{getenv("CFG_HOME")}/bricata_api_client.toml') as bac:
        results = await bac.get_alerts()  # Get some alerts

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        uid = choice(results.success)['uuid']  # Choose one at random
        results = await bac.get_alert(uuid=uid)

        assert type(results) is Results
        assert len(results.success) == 1
        assert not results.failure

        tprint(results)

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')


@pytest.mark.asyncio
async def test_tag_untag_alert():
    ts = time.perf_counter()

    bprint('Test: Tag Alert')
    async with BricataApiClient(cfg=f'{getenv("CFG_HOME")}/bricata_api_client.toml') as bac:
        results = await bac.get_alerts()  # Get some alerts

        assert type(results) is Results
        assert len(results.success) >= 1
        assert not results.failure

        print('results:', results.success)

        try:
            alert = choice(results.success)  # Choose one at random
            uid = alert['uuid']
            print(f'Tagging: {uid}')
            print('Alert Tags Before:', alert['data']['bricata']['tag'])
            assert 'Testing' not in results.success[0]['data']['bricata']['tag']
        except KeyError:
            print('Alert has no tags')

        results = await bac.tag_alert(uuid=uid, tag='Testing')  # Tag alert
        assert not results.failure

        results = await bac.get_alert(uuid=uid)  # Verify alert is tagged
        print('Alert tags after tag:', results.success[0]['data']['bricata']['tag'])
        assert 'Testing' in results.success[0]['data']['bricata']['tag']

        results = await bac.untag_alert(uuid=uid, tag='Testing')  # Untag alert
        assert not results.failure

        results = await bac.get_alert(uuid=uid)  # Verify Alert is no longer tagged
        print('Alert tags after untag:', results.success[0]['data']['bricata']['tag'])
        assert 'Testing' not in results.success[0]['data']['bricata']['tag']

    bprint(f'-> Completed in {(time.perf_counter() - ts):f} seconds.')
