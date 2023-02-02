"""
Client class for the Open Access Monitor API

For more information on the interface, see
https://open-access-monitor.de/api/swagger/index.html
"""

from . import docs
from . import utils


class OpenAccessMonitorAPI:

    def __init__(self, headers={}, token=""):
        self.BASE = "https://open-access-monitor.de/api"
        self.DATA = "{0}/Data".format(self.BASE)
        self.PUBLIC = "{0}/public".format(self.DATA)
        self.headers = headers
        self.token = token

    def info(self):
        return utils.json_request(self.BASE, headers=self.headers)

    def _databases(self):
        return utils.json_request(self.token_url(self.DATA), headers=self.headers)

    def collections(self, token=None):
        return utils.json_request(self.token_url(self.PUBLIC), headers=self.headers)

    @staticmethod
    def find_query(find, limit=10, **kwargs):
        q = {"find": find, "limit": limit}
        for key, value in kwargs.items():
            q[key] = value
        return utils.json_str(q)

    def token_url(self, url):
        return "{0}?token={1}".format(url, self.token or "")

    def query_url(self, query):
        return "{0}?query={1}&token={2}".format(self.PUBLIC, query, self.token or "")

    def get(self, query):
        if self.token is None:
            # raise exception, log message, ...?
            return None
        url = self.query_url(query)
        return utils.oam_request(url, headers=self.headers)

    def search(self, find, limit=10, **kwargs):
        query = self.find_query(find, limit=limit, **kwargs)
        response = self.get(query)
        if response is not None:
            return utils.oam_batch(response)

    def scroll(self, find, limit=100, **kwargs):
        batch = self.search(find, limit=limit, **kwargs)
        if not isinstance(batch, list):
            return None
        if len(batch) < limit:
            return batch
        skip = 0
        batches = []
        batches.extend(batch)
        finished = False
        while not finished:
            skip += limit
            batch = self.search(find, limit=limit, skip=skip, **kwargs)
            if batch:
                batches.extend(batch)
                if len(batch) < limit:
                    finished = True
            else:
                finished = True
        return batches

    def publication(self, doi):
        response = self.search("Publications", limit=1, filter={"doi": doi})
        if response and len(response) > 0:
            return docs.PublicationParser(response[0])

    def publication_costs(self, doi):
        response = self.search("PublicationCosts", limit=1, filter={"doi": doi})
        if response and len(response) > 0:
            return docs.PublicationCostsParser(response[0])

    def journal(self, issn):
        response = self.search("Journals", limit=1, filter={"issns": issn})
        if response and len(response) > 0:
            return docs.JournalParser(response[0])
