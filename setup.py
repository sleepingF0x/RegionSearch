# coding:utf-8
from setuptools import setup, find_packages
from region_search import __version__


setup(
    name='region-search',
    version=__version__,
    description='归属地查询',
    author='sleepingF0x',
    author_email='agent.999th@gmail.com',
    url='https://github.com/sleepingF0x/RegionSearch',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "dat_maker = region_search.cli:dat_maker",
        ]
    },
    keywords="region search",
    license='MIT',
    include_package_data=True,
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
