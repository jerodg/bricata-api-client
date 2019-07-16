#!/usr/bin/env python3.8
"""Bricata API Client: Setup
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
from typing import NoReturn

from setuptools import find_packages, setup

logger = logging.getLogger(__name__)


def readme() -> str:
    with open('README.md') as f:
        return f.read()


def main() -> NoReturn:
    setup(name='bricata-api-client',
          version='0!1.0a1.dev1',
          description='Bricata API Client Library',
          long_description=readme(),
          long_description_content_type='text/markdown',
          classifiers=['Development Status :: 3 - Alpha',
                       'Environment :: Console',
                       'Intended Audience :: End Users/Desktop',
                       'Intended Audience :: Developers',
                       'Intended Audience :: System Administrators',
                       'License :: Other/Proprietary License',
                       'Natural Language :: English',
                       'Operating System :: MacOS :: MacOS X',
                       'Operating System :: Microsoft :: Windows',
                       'Operating System :: POSIX',
                       'Programming Language :: Python :: 3.6',
                       'Programming Language :: Python :: 3.7',
                       'Programming Language :: Python :: 3.8',
                       'Topic :: Utilities',
                       'Topic :: Internet',
                       'Topic :: Internet :: WWW/HTTP'],
          keywords='Bricata API Client rest',
          url='https://pypi.org/project/bricata-api-client/',
          author='Jerod Gawne',
          author_email='jerod@jerodg.dev',
          license='Server Side Public License (SSPL)',
          packages=find_packages(),
          install_requires=['aiodns',
                            'aiohttp',
                            'cchardet',
                            'ujson'],
          include_package_data=True,
          zip_safe=True,
          setup_requires=['pytest-runner'],
          tests_require=['pytest', 'pytest-asyncio'],
          scripts=[],
          entry_points={'console_scripts': []},
          python_requires='~=3.6',
          project_urls={'Documentation': 'https://jerodg.github.io/bricata-api-client',
                        'Source':        'https://github.com/jerodg/bricata-api-client',
                        'Bugs':          'https://github.com/jerodg/bricata-api-client/issues'},
          package_data={'bricata-api-client': []})


if __name__ == '__main__':
    try:
        main()
    except Exception as excp:
        logger.exception(excp)