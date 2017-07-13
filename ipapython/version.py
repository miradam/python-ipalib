# Authors: Rob Crittenden <rcritten@redhat.com>
#
# Copyright (C) 2007  Red Hat
# see file 'COPYING' for use and warranty information
#
# This program is free software; you can redistribute it and/or modify
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
#

# The full version including strings
VERSION="4.3.1"

# A fuller version including the vendor tag (e.g. 3.3.3-34.fc20)
VENDOR_VERSION="4.3.1"


# Just the numeric portion of the version so one can do direct numeric
# comparisons to see if the API is compatible.
#
# How NUM_VERSION was generated changed over time:
# Before IPA 3.1.3, it was simply concatenated decimal numbers:
#   IPA 2.2.2:  NUM_VERSION=222
#   IPA 2.2.99: NUM_VERSION=2299 (development version)
#   IPA 3.1.0:  NUM_VERSION=310
#   IPA 3.1.3:  NUM_VERSION=313
# In IPA 3.1.4 and 3.2.0, the version was taken as an octal number due to a bug
# (https://fedorahosted.org/freeipa/ticket/3622):
#   IPA 3.1.4:  NUM_VERSION=12356 (octal 030104)
#   IPA 3.2.0:  NUM_VERSION=12416 (octal 030200)
# After IPA 3.2.0, it is decimal number where each part has two digits:
#   IPA 3.2.1:  NUM_VERSION=30201
#   IPA 3.2.99: NUM_VERSION=30299 (development version)
#   IPA 3.3.0:  NUM_VERSION=30300
NUM_VERSION=40301


# The version of the API.
API_VERSION=u'2.164'