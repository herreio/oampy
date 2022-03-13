from . import utils


class OpenAccessMonitorAPI:

    def __init__(self, headers={}):
        self.BASE = "https://open-access-monitor.de/api"
        self.DATA = "{0}/Data".format(self.BASE)
        self.PUBLIC = "{0}/public".format(self.DATA)
        self.headers = headers

    def info(self):
        return utils.json_request(self.BASE, headers=self.headers)

    def _databases(self):
        return utils.json_request(self.DATA, headers=self.headers)

    def collections(self):
        return utils.json_request(self.PUBLIC, headers=self.headers)

    @staticmethod
    def find_query(find, limit=10, **kwargs):
        q = {"find": find, "limit": limit}
        for key, value in kwargs.items():
            q[key] = value
        return utils.json_str(q)

    def query_url(self, query):
        return "{0}?query={1}".format(self.PUBLIC, query)

    def get(self, query, headers={}):
        url = self.query_url(query)
        return utils.oam_request(url, headers=self.headers)

    def search(self, find, limit=10, headers={}, **kwargs):
        query = self.find_query(find, limit=limit, **kwargs)
        response = self.get(query, headers=self.headers)
        if response is not None:
            return utils.oam_batch(response)

    def scroll(self, find, limit=100, headers={}, **kwargs):
        batch = self.search(find, limit=limit, headers=self.headers, **kwargs)
        if len(batch) < limit:
            return batch
        skip = 0
        batches = []
        batches.extend(batch)
        finished = False
        while not finished:
            skip += limit
            batch = self.search(find, limit=limit, skip=skip,
                                headers=self.headers, **kwargs)
            if batch:
                batches.extend(batch)
                if len(batch) < limit:
                    finished = True
            else:
                finished = True
        return batches
