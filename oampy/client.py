from . import utils


class OpenAccessMonitorAPI:

    def __init__(self):
        self.BASE = "https://open-access-monitor.de/api"
        self.DATA = "{0}/Data".format(self.BASE)
        self.PUBLIC = "{0}/public".format(self.DATA)

    def info(self):
        return utils.json_request(self.BASE)

    def _databases(self):
        return utils.json_request(self.DATA)

    def collections(self):
        return utils.json_request(self.PUBLIC)

    def get(self, find, filter=None, limit=10, headers={}):
        query = self.query(find, filter=filter, limit=limit)
        url = "{0}?query={1}".format(self.PUBLIC, query)
        response = utils.json_request(url, headers=headers)
        if response and response["ok"] == 1:
            return response["cursor"]

    @staticmethod
    def query(find, filter=None, limit=10):
        q = {"find": find, "limit": limit}
        if filter is not None:
            q["filter"] = filter
        return utils.json_str(q)
