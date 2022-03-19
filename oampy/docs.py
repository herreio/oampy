# -*- coding: utf-8 -*-
"""
Parser classes for data retrieved from the Open Access Monitor (OAM)

For more information on the database (i.e. MongoDB) schema of OAM, see
https://jugit.fz-juelich.de/synoa/oam-dokumentation/-/wikis/English-Version/Open-Access-Monitor/Database-Schema
"""


class BaseParser:

    def __init__(self, data):
        self.raw = data

    def _names(self):
        if self.raw:
            names = list(self.raw.keys())
            names.sort()
            return names
        return []

    def _field(self, name):
        if self.raw and name in self.raw:
            return self.raw[name]

    def get(self, name):
        return self._field(name)


class ObjectParser(BaseParser):

    def __init__(self, data):
        super().__init__(data)

    @property
    def id(self):
        return self._field("_id")


class OaObjectParser(ObjectParser):

    def __init__(self, data):
        super().__init__(data)

    @property
    def oa_color(self):
        return self._field("oa_color")


class PublisherParser(OaObjectParser):

    def __init__(self, data):
        super().__init__(data)

    @property
    def name(self):
        return self._field("name")


class JournalParser(OaObjectParser):

    def __init__(self, data):
        super().__init__(data)

    @property
    def title(self):
        return self._field("title")

    @property
    def issns(self):
        return self._field("issns")

    @property
    def flags(self):
        return self._field("flags")

    @property
    def agreements(self):
        return self._field("agreements")


class PublicationParser(OaObjectParser):

    def __init__(self, data):
        super().__init__(data)

    @property
    def year(self):
        return self._field("year")

    @property
    def published_date(self):
        return self._field("published_date")

    @property
    def _journal(self):
        return self._field("journal")

    @property
    def _publisher(self):
        return self._field("publisher")

    @property
    def _dim(self):
        return self._field("dim")

    @property
    def _wos(self):
        return self._field("wos")
