#!/usr/bin/env python

from distutils.core import setup

setup(
    name='SmashPuttTwitterBox',
    version='0.0.1',
    description='The uzh',
    author='Andrew Cole',
    author_email='aocole@aocole.net',
    url='https://github.com/aocole/SmashPuttTwitterBox',
# License: UNKNOWN
# Description: UNKNOWN
# Platform: UNKNOWN
    packages=[
        'SmashPuttTwitterBox',
    ],
    scripts=[
        'scripts/smashputttwitterbox',
    ],
#     package_dir={
#         'SmashPuttTwitterBox': '.',
#     },
    package_data={
        'SmashPuttTwitterBox': ['data/*'],
    },

)
