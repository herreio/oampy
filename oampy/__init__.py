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
__version__ = "0.1.14"

import os

try:
    EMAIL = os.environ["OAM_EMAIL"]
except KeyError:
    import socket
    import getpass
    host = socket.gethostname()
    user = getpass.getuser()
    EMAIL = "{0}@{1}".format(user, host)

from . import client, query


def get_client(headers={}):
    return client.OpenAccessMonitorAPI(headers=headers)


def get_journal(issn, headers={}):
    oamapi = get_client(headers=headers)
    return oamapi.journal(issn)


def get_publication(doi, headers={}):
    oamapi = get_client(headers=headers)
    return oamapi.publication(doi)


def get_publication_costs(doi, headers={}):
    oamapi = get_client(headers=headers)
    return oamapi.publication_costs(doi)


def run_search(find, limit=10, scroll=False, headers={}, **kwargs):
    oamapi = get_client(headers=headers)
    if scroll:
        return oamapi.scroll(find, limit=limit, **kwargs)
    return oamapi.search(find, limit=limit, **kwargs)


def run_journal_search(limit=10, scroll=True, headers={}, **kwargs):
    result = run_search("Journals", limit=limit, scroll=scroll, headers=headers, **kwargs)
    if result and len(result) > 0:
        return [client.docs.JournalParser(j) for j in result]


def get_agreement_journals(agreement, limit=10, scroll=True, filter={}, headers={}, **kwargs):
    agreement_filter = query.filter_agreements(agreement, filter=filter)
    return run_journal_search(limit=limit, scroll=scroll, headers=headers, filter=agreement_filter, **kwargs)


def run_publication_search(limit=10, scroll=False, headers={}, **kwargs):
    result = run_search("Publications", limit=limit, scroll=scroll, headers=headers, **kwargs)
    if result and len(result) > 0:
        return [client.docs.PublicationParser(p) for p in result]


def get_wos_grid_publications(grid_id, limit=10, scroll=False, filter={}, headers={}, **kwargs):
    grid_filter = query.filter_wos_organisation_grid(grid_id, filter=filter)
    return run_publication_search(limit=limit, scroll=scroll, headers=headers, filter=grid_filter, **kwargs)


def get_wos_grid_latest_publications(grid_id, limit=10, scroll=False, filter={}, headers={}, **kwargs):
    latest_sort = query.sort_desc("published_date")
    return get_wos_grid_publications(grid_id, limit=limit, scroll=scroll, filter=filter, headers=headers, sort=latest_sort, **kwargs)


def get_dim_ror_publications(ror_id, limit=10, scroll=False, filter={}, headers={}, **kwargs):
    ror_filter = query.filter_dim_organisation_ror(ror_id, filter=filter)
    return run_publication_search(limit=limit, scroll=scroll, headers=headers, filter=ror_filter, **kwargs)


def get_dim_ror_latest_publications(ror_id, limit=10, scroll=False, filter={}, headers={}, **kwargs):
    latest_sort = query.sort_desc("published_date")
    return get_dim_ror_publications(ror_id, limit=limit, scroll=scroll, filter=filter, headers=headers, sort=latest_sort, **kwargs)


def get_wos_ror_publications(ror_id, limit=10, scroll=False, filter={}, headers={}, **kwargs):
    ror_filter = query.filter_wos_organisation_ror(ror_id, filter=filter)
    return run_publication_search(limit=limit, scroll=scroll, headers=headers, filter=ror_filter, **kwargs)


def get_wos_ror_latest_publications(ror_id, limit=10, scroll=False, filter={}, headers={}, **kwargs):
    latest_sort = query.sort_desc("published_date")
    return get_wos_ror_publications(ror_id, limit=limit, scroll=scroll, filter=filter, headers=headers, sort=latest_sort, **kwargs)


def get_dim_grid_publications(grid_id, limit=10, scroll=False, filter={}, headers={}, **kwargs):
    grid_filter = query.filter_dim_organisation_grid(grid_id, filter=filter)
    return run_publication_search(limit=limit, scroll=scroll, headers=headers, filter=grid_filter, **kwargs)


def get_dim_grid_latest_publications(grid_id, limit=10, scroll=False, filter={}, headers={}, **kwargs):
    latest_sort = query.sort_desc("published_date")
    return get_dim_grid_publications(grid_id, limit=limit, scroll=scroll, filter=filter, headers=headers, sort=latest_sort, **kwargs)


def run_publication_cost_search(limit=10, scroll=False, headers={}, **kwargs):
    result = run_search("PublicationCosts", limit=limit, scroll=scroll, headers=headers, **kwargs)
    if result and len(result) > 0:
        return [client.docs.PublicationCostsParser(pc) for pc in result]


def get_openapc_grid_publication_cost(grid_id, limit=10, scroll=False, filter={}, headers={}, **kwargs):
    grid_filter = query.filter_openapc_organisation_grid(grid_id, filter=filter)
    return run_publication_cost_search(limit=limit, scroll=scroll, headers=headers, filter=grid_filter, **kwargs)


def get_openapc_ror_publication_cost(ror_id, limit=10, scroll=False, filter={}, headers={}, **kwargs):
    ror_filter = query.filter_openapc_organisation_ror(ror_id, filter=filter)
    return run_publication_cost_search(limit=limit, scroll=scroll, headers=headers, filter=ror_filter, **kwargs)
