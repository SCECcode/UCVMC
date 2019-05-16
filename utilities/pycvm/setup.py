##
#  @file setup.py
#  @brief Sets up the Python UCVM package for this computer.
#  @author David Gill - SCEC <davidgil@usc.edu>
#  @author extended by Mei-Hui Su - SCEC <mei@usc.edu>
#  @version 19.4.0
#
#  

from distutils.core import setup

setup(name='pycvm',
      version='19.4.0',
      description='Python code extensions for UCVM.',
      url='http://scec.usc.edu/scecpedia/UCVM',
      author='Southern California Earthquake Center',
      author_email='software@scec.org',
      packages=['pycvm'])
