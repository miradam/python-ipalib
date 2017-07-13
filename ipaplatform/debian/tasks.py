# Authors:
#   Timo Aaltonen <tjaalton@ubuntu.com>
#
# Copyright (C) 2014 Timo Aaltonen
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

"""
This module contains default Debian-specific implementations of system tasks.
"""

from ipaplatform.paths import paths
from ipaplatform.base.tasks import *
from ipaplatform.redhat.tasks import RedHatTaskNamespace

BaseTask = BaseTaskNamespace()

class DebianTaskNamespace(RedHatTaskNamespace):

    def restore_pre_ipa_client_configuration(self, fstore, statestore,
                                             was_sssd_installed,
                                             was_sssd_configured):
        return True

    def set_nisdomain(self, nisdomain):
        return True

    def modify_nsswitch_pam_stack(self, sssd, mkhomedir, statestore):
        return True

    def modify_pam_to_use_krb5(self, statestore):
        return True

    def restore_network_configuration(self, fstore, statestore):
        return True

    def parse_ipa_version(self, version):
        return BaseTask.parse_ipa_version(version)

tasks = DebianTaskNamespace()
