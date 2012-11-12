"""
This file is part of AWE
Copyright (C) 2012- University of Notre Dame
This software is distributed under the GNU General Public License.
See the file COPYING for details.
"""


from setuptools import setup


setup( author       = "Badi' Abdul-Wahid",
       author_email = 'abdulwahidc@gmail.com',
       url          = 'https://bitbucket.org/badi/trax',
       name         = 'trax',
       packages     = ['trax'],
       test_suite   = 'tests',
       platforms    = ['Linux', 'Mac OS X'],
       description  = 'Transactional logging library'
       )
