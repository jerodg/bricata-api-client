#!/usr/bin/env python3.8
"""Bricata API Client
Copyright © 2019. Jerod Gawne <https://github.com/jerodg/>

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
import asyncio
import logging
from typing import NoReturn, Optional, Union

import aiohttp as aio
import ujson

from base_api_client import BaseApiClient, Results
from bricata_api_client.models import TagRequest

logger = logging.getLogger(__name__)


class BricataApiClient(BaseApiClient):
    """Bricata API Client"""
    SEM: int = 5  # This defines the number of parallel async requests to make.

    def __init__(self, cfg: Union[str, dict], sem: Optional[int] = None):
        """Initializes Class

        Args:
            cfg (Union[str, dict]): As a str it should contain a full path
                pointing to a configuration file (json/toml). See
                config.* in the examples folder for reference.
            sem (Optional[int]): An integer that defines the number of parallel
                requests to make."""
        BaseApiClient.__init__(self, cfg=cfg, sem=sem or self.SEM)
        self.load_config()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.logout()
        await BaseApiClient.__aexit__(self, exc_type, exc_val, exc_tb)

    async def __check_login(self) -> NoReturn:
        if not self.header:
            await self.login()

    async def login(self) -> Results:
        payload = {'username': self.cfg['Auth']['Username'], 'password': self.cfg['Auth']['Password']}

        async with aio.ClientSession(headers=self.HDR, json_serialize=ujson.dumps) as session:
            logger.debug('Logging In...')

            tasks = [asyncio.create_task(self.request(method='post', end_point='login/', session=session, json=payload))]
            results = await asyncio.gather(*tasks)

            logger.debug('-> Complete.')

        await session.close()

        results = await self.process_results(results)
        self.header = {**self.HDR, **{'Authorization': f'{results.success[0]["token_type"]} {results.success[0]["token"]}'}}

        return results

    async def logout(self) -> Results:
        payload = {'username': self.cfg['Auth']['Username']}

        async with aio.ClientSession(headers=self.header, json_serialize=ujson.dumps) as session:
            logger.debug('Logging Out...')

            tasks = [asyncio.create_task(self.request(method='post', end_point='logout/', session=session, json=payload))]
            results = await asyncio.gather(*tasks)

            logger.debug('-> Complete.')

        await session.close()

        results = await self.process_results(results)
        self.header = None

        return results

    async def get_alerts(self, **kwargs) -> Results:
        await self.__check_login()

        # todo: handle filters

        async with aio.ClientSession(headers=self.header, json_serialize=ujson.dumps) as session:
            logger.debug('Getting Alerts...')

            tasks = [asyncio.create_task(self.request(method='get', end_point='alerts/', session=session))]
            results = await asyncio.gather(*tasks)

            logger.debug('-> Complete.')

        await session.close()

        results = await self.process_results(results, 'objects')

        return results

    async def get_alert(self, uuid: str) -> Results:
        await self.__check_login()

        async with aio.ClientSession(headers=self.header, json_serialize=ujson.dumps) as session:
            logger.debug('Getting Alerts...')

            tasks = [asyncio.create_task(self.request(method='get', end_point=f'alert/{uuid}', session=session))]
            results = await asyncio.gather(*tasks)

            logger.debug('-> Complete.')

        await session.close()

        results = await self.process_results(results)

        return results

    async def tag_alert(self, uuid: str, tag: str):
        await self.__check_login()

        async with aio.ClientSession(headers=self.header, json_serialize=ujson.dumps) as session:
            logger.debug('Getting Tags...')

            tasks = [asyncio.create_task(self.request(method='put', end_point=f'alerts/{uuid}/tag/{tag}/', session=session))]
            results = await asyncio.gather(*tasks)

            logger.debug('-> Complete.')

        await session.close()

        results = await self.process_results(results)

        return results

    async def untag_alert(self, uuid: str, tag: str):
        await self.__check_login()

        async with aio.ClientSession(headers=self.header, json_serialize=ujson.dumps) as session:
            logger.debug('Getting Tags...')

            tasks = [asyncio.create_task(self.request(method='delete', end_point=f'alerts/{uuid}/tag/{tag}/', session=session))]
            results = await asyncio.gather(*tasks)

            logger.debug('-> Complete.')

        await session.close()

        results = await self.process_results(results)

        return results

    async def get_tags(self) -> Results:
        await self.__check_login()

        async with aio.ClientSession(headers=self.header, json_serialize=ujson.dumps) as session:
            logger.debug('Getting Tags...')

            tasks = [asyncio.create_task(self.request(method='get', end_point='tags/', session=session))]
            results = await asyncio.gather(*tasks)

            logger.debug('-> Complete.')

        await session.close()

        results = await self.process_results(results)

        return results

    async def put_tag(self, tag: TagRequest) -> Results:
        await self.__check_login()

        async with aio.ClientSession(headers=self.header, json_serialize=ujson.dumps) as session:
            logger.debug('Getting Tags...')

            tasks = [asyncio.create_task(self.request(method='put', end_point=f'tags/{tag.name}/', session=session, json=tag.dict))]
            results = await asyncio.gather(*tasks)

            logger.debug('-> Complete.')

        await session.close()

        results = await self.process_results(results)

        return results

    async def delete_tag(self, tag_name: str) -> Results:
        await self.__check_login()

        async with aio.ClientSession(headers=self.header, json_serialize=ujson.dumps) as session:
            logger.debug('Getting Tags...')

            tasks = [asyncio.create_task(self.request(method='delete', end_point=f'tags/{tag_name}/', session=session))]
            results = await asyncio.gather(*tasks)

            logger.debug('-> Complete.')

        await session.close()

        results = await self.process_results(results)

        return results


if __name__ == '__main__':
    print(__doc__)
