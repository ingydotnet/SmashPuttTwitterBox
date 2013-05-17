#!/usr/bin/env python

from distutils.core import setup

setup(
    name='SmashPuttTwitterBox',
    version='0.0.1',
    description="A Twitter Box for Smash Putt",
    license='Python',
    platforms=['POSIX'],
    requires=[
        'tweepy',
        'pygame',
        'RPi.GPIO',
    ],
    author='Andrew Cole',
    author_email='aocole@aocole.net',
    url='https://github.com/aocole/SmashPuttTwitterBox',
    packages=[
        'SmashPuttTwitterBox',
    ],
    scripts=[
        'scripts/smashputttwitterbox',
    ],
    package_data={
        'SmashPuttTwitterBox': ['data/*'],
    },
    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Communications :: Twitter',
    ],

)
