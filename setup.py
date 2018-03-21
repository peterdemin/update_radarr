#!/usr/bin/env python

import os
from setuptools import setup


install_requires = [
    'requests',
]

setup(
    name='update_radarr',
    version='0.0.1',
    description="Update Radarr from GitHub",
    long_description='Download latest Radarr release from GitHub and untar it in /opt/Radarr',
    author="Peter Demin",
    author_email='peterdemin@gmail.com',
    url='https://github.com/peterdemin/update_radarr',
    py_modules=['update_radarr'],
    include_package_data=True,
    install_requires=install_requires,
    license="MIT license",
    zip_safe=False,
    keywords='radarr',
    entry_points={
        'console_scripts': [
            'update-radarr = update_radarr:main',
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
