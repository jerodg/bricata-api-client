#!/usr/bin/env python3.8
"""Bricata API Client
Copyright © 2019 Jerod Gawne <https://github.com/jerodg/>

This program is free software: you can redistribute it and/or modify
it under the terms of the Server Side Public License (SSPL) as
published by MongoDB, Inc., either version 1 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
SSPL for more details.

You should have received a copy of the SSPL along with this program.
If not, see <https://www.mongodb.com/licensing/server-side-public-license>."""
import logging
from asyncio import Semaphore
from json.decoder import JSONDecodeError
from typing import List, Optional, Union
import asyncio
import aiohttp as aio
import ujson
from base_api_client.base_api_client import BaseApiClient
from tenacity import after_log, before_sleep_log, retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential

logger = logging.getLogger(__name__).addHandler(logging.NullHandler())


class BricataApiClient(BaseApiClient):
    SEM: int = 5  # This defines the number of parallel async requests to make.

    def __init__(self, cfg: Optional[Union[str, dict]] = None, sem: Optional[int] = None):
        BaseApiClient.__init__(cfg=cfg, sem=sem or self.SEM)
        self.header = {'Content-Type':  'application/json; charset=utf-8'}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        BaseApiClient.__exit__(self, exc_type, exc_val, exc_tb)

    async def login(self):
        data = {'username': self.cfg['Bricata']['username'], 'password': self.cfg['Bricata']['password']}

        async with aio.ClientSession(headers=self.header) as session:
            logger.debug('Logging In...')

            tasks = [asyncio.create_task(self.__login(session=session, data=ujson.dumps(payload)))]
            results = await asyncio.gather(*tasks)

            self.header['Authorization'] = f'Bearer {results[0]["access_token"]}'

            if NFO:
                logger.info('\tComplete.')

        await session.close()

        return await self.process_results(results)

    @retry(retry=retry_if_exception_type(aio.ClientError),
           wait=wait_random_exponential(multiplier=1.25, min=3, max=60),
           after=after_log(logger, logging.DEBUG),
           stop=stop_after_attempt(7),
           before_sleep=before_sleep_log(logger, logging.DEBUG))
    async def __login(self, session: aio.ClientSession, data: dict) -> Union[dict, aio.ClientResponse]:
        async with self.sem:
            response = await session.post(self.URI_AUTH, ssl=self.VERIFY_SSL, data=data, proxy=self.PROXY)
            if 200 <= response.status <= 299:
                return await response.json()
            elif response.status == 429:
                raise aio.ClientError
            else:
                return response


if __name__ == '__main__':
    print(__doc__)
