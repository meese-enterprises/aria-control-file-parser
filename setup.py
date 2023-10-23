#!/usr/bin/env python
# -*- coding: utf-8 -*-

# File template from https://github.com/navdeep-G/setup.py
# Note: To use the "upload" functionality of this file, you must:
#   $ pip3 install twine

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = "parse_aria_control_file"
DESCRIPTION = "Parse the information out of aria2 control files."
URL = "https://github.com/meese-enterprises/aria-control-file-parser"
REQUIRES_PYTHON = ">=3.0.0"
VERSION = "1.0.0"

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description
try:
  with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()
except FileNotFoundError:
  long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
  project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
  with open(os.path.join(here, project_slug, "__version__.py")) as f:
    exec(f.read(), about)
else:
  about["__version__"] = VERSION


class UploadCommand(Command):
  """Support setup.py upload."""

  description = "Build and publish the package."
  user_options = []

  @staticmethod
  def status(s):
    """Prints things in bold."""
    print("\033[1m{0}\033[0m".format(s))

  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    try:
      self.status("Removing previous builds…")
      rmtree(os.path.join(here, "dist"))
    except OSError:
      pass

    self.status("Building Source and Wheel (universal) distribution…")
    os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

    self.status("Uploading the package to PyPI via Twine…")
    os.system("python3 -m twine upload dist/*")

    self.status("Pushing git tags…")
    os.system("git tag v{0}".format(about["__version__"]))
    os.system("git push --tags")

    sys.exit()


setup(
  name=NAME,
  version=VERSION,
  description=DESCRIPTION,
  long_description=long_description,
  long_description_content_type="text/markdown",
  python_requires=REQUIRES_PYTHON,
  url=URL,
  packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
  install_requires=["argparse", "setuptools", "wheel"],
  include_package_data=True,
  classifiers=[
    "Programming Language :: Python :: 3",
  ],
  # $ setup.py publish support.
  cmdclass={
    "upload": UploadCommand,
  },
)
