from distutils.core import setup

setup(
    name='url_paginator',
    version='0.0.1',
    packages=['url_paginator'],
    url='https://github.com/Frozen/url_paginator',
    license='MIT',
    author='frozen',
    description='Pagination with url',
    install_requires=[
        'django>=1.8.0'
    ]
)