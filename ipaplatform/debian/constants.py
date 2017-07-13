#
# Copyright (C) 2015  FreeIPA Contributors see COPYING for license
#

'''
This Debian family platform module exports platform dependant constants.
'''

# Fallback to default path definitions
from ipaplatform.base.constants import BaseConstantsNamespace


class DebianConstantsNamespace(BaseConstantsNamespace):
#   DS_USER = "dirsrv"
#   DS_GROUP = "dirsrv"
    HTTPD_USER = "www-data"
#   IPA_DNS_PACKAGE_NAME = "freeipa-server-dns"
#   KDCPROXY_USER = "kdcproxy"
    NAMED_USER = "bind"
    NAMED_GROUP = "bind"
    # ntpd init variable used for daemon options
    NTPD_OPTS_VAR = "NTPD_OPTS"
    # quote used for daemon options
    NTPD_OPTS_QUOTE = "\'"
    ODS_USER = "opendnssec"
    ODS_GROUP = "opendnssec"
#   PKI_USER = "pkiuser"
    SECURE_NFS_VAR = "NEED_GSSD"
#   SSSD_USER = "sssd"

constants = DebianConstantsNamespace()
