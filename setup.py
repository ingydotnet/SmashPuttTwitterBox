#!/usr/bin/env python

from distutils.core import setup

setup(
    name='SmashPuttTwitterBox',
    version='0.0.1',
    description='The uzh',
    author='Andrew Cole',
    author_email='aocole@aocole.net',
    url='https://github.com/aocole/SmashPuttTwitterBox',
    packages=[
        'SmashPuttTwitterBot',
        'SmashPuttTwitterBot.custom_stream_listener',
        'SmashPuttTwitterBot.printer',
        'SmashPuttTwitterBot.settings',
        'SmashPuttTwitterBot.video',
        'SmashPuttTwitterBot.watcher',
    ],
)
