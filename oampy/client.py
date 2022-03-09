from . import utils


class OpenAccessMonitorAPI:

    def __init__(self):
        self.BASE = "https://open-access-monitor.de/api/Data/public"

    def get(self, find, filter=None, limit=10, headers={}):
        query = self.query(find, filter=filter, limit=limit)
        url = "{0}?query={1}".format(self.BASE, query)
        response = utils.json_request(url, headers=headers)
        if response and response["ok"] == 1:
            return response["cursor"]

    @staticmethod
    def query(find, filter=None, limit=10):
        q = {"find": find, "limit": limit}
        if filter is not None:
            q["filter"] = filter
        return utils.json_str(q)
