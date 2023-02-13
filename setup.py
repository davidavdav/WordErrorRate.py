#!/usr/bin/env python

from setuptools import setup

exec(open("worderrorrate/version.py").read()) ## reads __version__

setup(name="worderrorrate",
      version=__version__,
      description="Align sentences and compute the word error rate",
      author="David A. van Leeuwen",
      author_email="david.vanleeuwen@gmail.com",
      license="MIT",
      classifiers=["Programming Language :: Python :: 3.7"],
      # packages defines which part of the archive is actually copied
      packages=["worderrorrate"],
      scripts=[],
      install_requires=["numpy"],
      dependency_links=[],
      include_package_data=False
)
