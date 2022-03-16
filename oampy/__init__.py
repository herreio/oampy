# -*- coding: utf-8 -*-
"""
This package allows to access data from the Open Access Monitor (OAM),
which is run by Forschungszentrum Jülich (c) 2022.

For the OAM dashboard, see
https://open-access-monitor.de

For the OAM documentation, see
https://jugit.fz-juelich.de/synoa/oam-dokumentation/-/wikis/home
"""

__author__ = "Donatus Herre <donatus.herre@slub-dresden.de>"
__version__ = "0.1.3"

import os

try:
    EMAIL = os.environ["OAM_EMAIL"]
except KeyError:
    import socket
    import getpass
    host = socket.gethostname()
    user = getpass.getuser()
    EMAIL = "{0}@{1}".format(user, host)

from . import client


def get_client(headers={}):
    return client.OpenAccessMonitorAPI(headers=headers)


def get_journal(issn, headers={}):
    oamapi = get_client(headers=headers)
    return oamapi.journal(issn)


def get_publication(doi, headers={}):
    oamapi = get_client(headers=headers)
    return oamapi.publication(doi)


def run_search(find, limit=10, headers={}, **kwargs):
    oamapi = get_client(headers=headers)
    return oamapi.search(find, limit=limit, **kwargs)
