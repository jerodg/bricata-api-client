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
from uuid import uuid4

import aiohttp as aio
import rapidjson

from base_api_client import BaseApiClient, Results
from bricata_api_client.models import AlertsFilter, TagRequest, AlertQuery

logger = logging.getLogger(__name__)


class BricataApiClient(BaseApiClient):
    """Bricata API Client"""
    SEM: int = 5  # This defines the number of parallel async requests to make.

    def __init__(self, cfg: Union[str, dict]):
        """Initializes Class

        Args:
            cfg (Union[str, dict]): As a str it should contain a full path
                pointing to a configuration file (json/toml). See
                config.* in the examples folder for reference.
            sem (Optional[int]): An integer that defines the number of parallel
                requests to make."""
        BaseApiClient.__init__(self, cfg=cfg)
        self.header = None

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

        logger.debug('Logging in to Bricata...')

        tasks = [asyncio.create_task(self.request(method='post',
                                                  end_point='/login/',
                                                  request_id=uuid4().hex,
                                                  json=payload))]
        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        results = await self.process_results(results)

        self.header = {**self.HDR, **{'Authorization': f'{results.success[0]["token_type"]} {results.success[0]["token"]}'}}
        await self.session.close()

        self.session = aio.ClientSession(headers=self.header, json_serialize=rapidjson.dumps)
        return results

    async def logout(self) -> Results:
        payload = {'username': self.cfg['Auth']['Username']}

        logger.debug('Logging out of Bricata...')

        tasks = [asyncio.create_task(self.request(method='post',
                                                  end_point='/logout/',
                                                  request_id=uuid4().hex,
                                                  json=payload))]
        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        self.header = None

        return await self.process_results(results)

    async def get_records(self, query: Union[AlertQuery]) -> Results:
        """
        Args:
            query (Union[AlertQuery]):

        Returns:
            results (Results)"""
        await self.__check_login()

        logger.debug(f'Getting {type(query)}, record(s)...')
        tasks = [asyncio.create_task(self.request(method='get',
                                                  end_point=query.end_point,
                                                  request_id=uuid4().hex,
                                                  params=query.dict()))]

        results = await self.process_results(Results(data=await asyncio.gather(*tasks)), query.data_key)

        logger.debug('-> Complete.')

        return results

    async def get_alerts(self, filters: Optional[AlertsFilter] = None) -> Results:
        await self.__check_login()

        logger.debug('Getting alerts from Bricata...')

        tasks = [asyncio.create_task(self.request(method='get',
                                                  end_point='/alerts/',
                                                  request_id=uuid4().hex,
                                                  params=filters.dict if filters else None))]
        results = Results(data=await asyncio.gather(*tasks))

        logger.debug(f'-> Complete; Retrieved {len(results.data)}, alerts.')

        return await self.process_results(results, 'objects')

    async def get_alert(self, uuid: str) -> Results:
        await self.__check_login()

        logger.debug(f'Getting alert: {uuid}, from Bricata...')

        tasks = [asyncio.create_task(self.request(method='get',
                                                  end_point=f'/alert/{uuid}',
                                                  request_id=uuid4().hex))]
        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        return await self.process_results(results)

    async def tag_alert(self, uuid: str, tag: str):
        await self.__check_login()

        logger.debug(f'Tagging: {tag} alert: {uuid}, in Bricata...')

        tasks = [asyncio.create_task(self.request(method='put',
                                                  end_point=f'/alerts/{uuid}/tag/{tag}/',
                                                  request_id=uuid4().hex))]
        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        return await self.process_results(results)

    async def untag_alert(self, uuid: str, tag: str):
        await self.__check_login()

        logger.debug(f'Untagging: {tag} from alert: {uuid}, in Bricata...')

        tasks = [asyncio.create_task(self.request(method='delete',
                                                  end_point=f'/alerts/{uuid}/tag/{tag}/',
                                                  request_id=uuid4().hex))]
        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        return await self.process_results(results)

    async def get_tags(self) -> Results:
        await self.__check_login()

        logger.debug('Getting tags from Bricata...')

        tasks = [asyncio.create_task(self.request(method='get', end_point='/tags/', request_id=uuid4().hex, ))]
        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        return await self.process_results(results)

    async def put_tag(self, tag: TagRequest) -> Results:
        await self.__check_login()

        logger.debug(f'Creating tag: {tag} in Bricata...')

        tasks = [asyncio.create_task(
                self.request(method='put', end_point=f'/tags/{tag.name}/', request_id=uuid4().hex,
                             json=tag.dict))]
        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        return await self.process_results(results)

    async def delete_tag(self, tag_name: str) -> Results:
        await self.__check_login()

        logger.debug(f'Deleting tag: {tag_name}, from Bricata...')

        tasks = [asyncio.create_task(
                self.request(method='delete', end_point=f'/tags/{tag_name}/', request_id=uuid4().hex))]
        results = Results(data=await asyncio.gather(*tasks))

        logger.debug('-> Complete.')

        return await self.process_results(results)


if __name__ == '__main__':
    print(__doc__)
