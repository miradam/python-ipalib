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
Contains Debian-specific service class implementations.
"""

import time

from ipaplatform.tasks import tasks
from ipaplatform.base import services as base_services
from ipaplatform.redhat import services as redhat_services
from ipapython import ipautil
from ipapython.ipa_log_manager import root_logger
from ipalib import api
from ipaplatform.paths import paths

# Mappings from service names as FreeIPA code references to these services
# to their actual systemd service names
debian_system_units = redhat_services.redhat_system_units

debian_system_units['named-regular'] = 'bind9.service'
debian_system_units['named-pkcs11'] = 'bind9-pkcs11.service'
debian_system_units['named'] = debian_system_units['named-pkcs11']
debian_system_units['pki-tomcatd'] = 'pki-tomcatd.service'
debian_system_units['pki_tomcatd'] = debian_system_units['pki-tomcatd']
debian_system_units['ods-enforcerd'] = 'opendnssec-enforcer.service'
debian_system_units['ods_enforcerd'] = debian_system_units['ods-enforcerd']
debian_system_units['ods-signerd'] = 'opendnssec-signer.service'
debian_system_units['ods_signerd'] = debian_system_units['ods-signerd']

# Service classes that implement Debian-specific behaviour

class DebianService(redhat_services.RedHatService):
    system_units = debian_system_units


class DebianSysvService(base_services.PlatformService):
    def __wait_for_open_ports(self, instance_name=""):
        """
        If this is a service we need to wait for do so.
        """
        ports = None
        if instance_name in base_services.wellknownports:
            ports = base_services.wellknownports[instance_name]
        else:
            if self.service_name in base_services.wellknownports:
                ports = base_services.wellknownports[self.service_name]
        if ports:
            ipautil.wait_for_open_ports('localhost', ports, api.env.startup_timeout)
    def stop(self, instance_name='', capture_output=True):
        ipautil.run([paths.SBIN_SERVICE, self.service_name, "stop",
                     instance_name], capture_output=capture_output)
        if 'context' in api.env and api.env.context in ['ipactl', 'installer']:
            update_service_list = True
        else:
            update_service_list = False
        super(DebianSysvService, self).stop(instance_name)

    def start(self, instance_name='', capture_output=True, wait=True):
        ipautil.run([paths.SBIN_SERVICE, self.service_name, "start",
                     instance_name], capture_output=capture_output)
        if 'context' in api.env and api.env.context in ['ipactl', 'installer']:
            update_service_list = True
        else:
            update_service_list = False
        if wait and self.is_running(instance_name):
            self.__wait_for_open_ports(instance_name)
        super(DebianSysvService, self).start(instance_name)

    def restart(self, instance_name='', capture_output=True, wait=True):
        ipautil.run([paths.SBIN_SERVICE, self.service_name, "restart",
                     instance_name], capture_output=capture_output)
        if wait and self.is_running(instance_name):
            self.__wait_for_open_ports(instance_name)

    def is_running(self, instance_name=""):
        ret = True
        try:
            result = ipautil.run([paths.SBIN_SERVICE,
                                  self.service_name, "status",
                                  instance_name],
                                  capture_output=True)
            sout = result.output
            if sout.find("NOT running") >= 0:
                ret = False
            if sout.find("stop") >= 0:
                ret = False
            if sout.find("inactive") >= 0:
                ret = False
        except ipautil.CalledProcessError:
                ret = False
        return ret

    def is_installed(self):
        installed = True
        try:
            ipautil.run([paths.SBIN_SERVICE, self.service_name, "status"])
        except ipautil.CalledProcessError, e:
            if e.returncode == 1:
                # service is not installed or there is other serious issue
                installed = False
        return installed

    def is_enabled(self, instance_name=""):
        # Services are always assumed to be enabled when installed
        return True

    def enable(self):
        return True

    def disable(self):
        return True

    def install(self):
        return True

    def remove(self):
        return True

    def tune_nofile_platform(self):
        return True

# For services which have no Debian counterpart
class DebianNoService(base_services.PlatformService):
    def start(self):
        return True

    def stop(self):
        return True

    def restart(self):
        return True

    def disable(self):
        return True

class DebianSSHService(DebianSysvService):
    def get_config_dir(self, instance_name=""):
        return '/etc/ssh'

# Function that constructs proper Debian-specific server classes for services
# of specified name

def debian_service_class_factory(name):
    if name == 'dirsrv':
        return redhat_services.RedHatDirectoryService(name)
    if name == 'domainname':
        return DebianNoService(name)
    if name == 'ipa':
        return redhat_services.RedHatIPAService(name)
    if name == 'httpd':
        return DebianSysvService("apache2")
    if name == 'kadmin':
        return DebianSysvService("krb5-admin-server")
    if name == 'krb5kdc':
        return DebianSysvService("krb5-kdc")
    if name == 'messagebus':
        return DebianNoService(name)
    if name == 'ntpd':
        return DebianSysvService("ntp")
    if name == 'smb':
        return DebianSysvService("smbd")
    if name == 'sshd':
        return DebianSSHService(name)
    return DebianService(name)


# Magicdict containing DebianService instances.

class DebianServices(base_services.KnownServices):
    def __init__(self):
        services = dict()
        for s in base_services.wellknownservices:
            services[s] = debian_service_class_factory(s)
        # Call base class constructor. This will lock services to read-only
        super(DebianServices, self).__init__(services)


# Objects below are expected to be exported by platform module

from ipaplatform.base.services import timedate_services
service = debian_service_class_factory
knownservices = DebianServices()
