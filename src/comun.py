#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
#
#
# ColorGetter
# 
# Copyright (C) 2011 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'
__date__ ='$10/11/2012'
__copyright__ = 'Copyright (c) 2011, 2012 Lorenzo Carbonell'
__license__ = 'GPLV3'
__url__ = 'http://www.atareao.es'
__version__ = '0.0.1.0'

import os
import locale
import gettext

######################################

def is_package():
    return __file__.find('src') < 0

######################################


VERSION = __version__
APPNAME = 'Dropper'
APP = 'dropper'

# check if running from source
if is_package():
    ROOTDIR = os.path.join('/opt/extras.ubuntu.com/', APP, 'share')
    LANGDIR = os.path.join(ROOTDIR, 'locale-langpack')
    APPDIR = os.path.join(ROOTDIR, APP)
    IMGDIR = APPDIR
else:
    VERSION = VERSION + '-src'
    ROOTDIR = os.path.dirname(__file__)
    LANGDIR = os.path.normpath(os.path.join(ROOTDIR, '../po'))
    APPDIR = ROOTDIR
    IMGDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/icons'))
ICON = os.path.join(IMGDIR,'dropper.svg')

try:
	current_locale, encoding = locale.getdefaultlocale()
	language = gettext.translation(APP, LANGDIR, [current_locale])
	language.install()
	_ = language.gettext
except Exception as e:
	print(e)
	_ = str
