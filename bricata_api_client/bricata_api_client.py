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
from ssl import create_default_context, Purpose
from typing import Optional, Union

import aiohttp as aio
import ujson
from tenacity import after_log, before_sleep_log, retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential

from base_api_client.base_api_client import BaseApiClient

logger = logging.getLogger(__name__)


class BricataApiClient(BaseApiClient):
    """Bricata API Client

    Attributes:
    """
    SEM: int = 5  # This defines the number of parallel async requests to make.

    def __init__(self, cfg: Union[str, dict], sem: Optional[int] = None):
        BaseApiClient.__init__(self, cfg=cfg, sem=sem or self.SEM)

        self.header = {'Content-Type': 'application/json; charset=utf-8'}
        self.proxy = None
        self.proxy_auth = None
        self.ssl = None
        self.load_config()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        BaseApiClient.__exit__(self, exc_type, exc_val, exc_tb)

    def load_config(self):
        proxy_uri = self.cfg['Proxy'].pop('URI', None)
        if proxy_uri:
            proxy_port = self.cfg['Proxy'].pop('Port')
            proxy_user = self.cfg['Proxy'].pop('Username')
            proxy_pass = self.cfg['Proxy'].pop('Password')
            self.proxy = f'{proxy_uri}:{proxy_port}'
            self.proxy_auth = aio.BasicAuth(login=proxy_user, password=proxy_pass)

        ssl_path = self.cfg['Options'].pop('CAPath', None)
        if ssl_path:
            self.ssl = create_default_context(purpose=Purpose.CLIENT_AUTH, capath=ssl_path)
        else:
            self.ssl = self.cfg['Options'].pop('VerifySSL', True)

    async def login(self) -> dict:
        data = {'username': self.cfg['Auth']['Username'], 'Password': self.cfg['Auth']['Password']}

        async with aio.ClientSession(headers=self.header, json_serialize=ujson.dumps) as session:
            logger.debug('Logging In...')

            tasks = [asyncio.create_task(self.__login(session=session, data=ujson.dumps(data)))]
            results = await asyncio.gather(*tasks)

            self.header['Authorization'] = f'{results[0]["token_type"]} {results[0]["token"]}'

            logger.debug('-> Complete.')

        await session.close()

        return await self.process_results(results)

    @retry(retry=retry_if_exception_type(aio.ClientError),
           wait=wait_random_exponential(multiplier=1.25, min=3, max=60),
           after=after_log(logger, logging.DEBUG),
           stop=stop_after_attempt(5),
           before_sleep=before_sleep_log(logger, logging.WARNING))
    async def __login(self, session: aio.ClientSession, data: dict) -> Union[dict, aio.ClientResponse]:
        async with self.sem:
            response = await session.post(f'{self.cfg["URI"]["Base"]}/login/', ssl=self.ssl, data=data, proxy=self.proxy)
            if response.status == 200:
                return {'token': await response.text(encoding='utf-8'), 'token_type': 'Bearer'}
            elif response.status == 503:
                raise aio.ClientError
            else:
                return response


if __name__ == '__main__':
    print(__doc__)
