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


class RorAddressParser(BaseParser):

    def __init__(self, data):
        super().__init__(data)

    @property
    def city(self):
        return self._field("city")

    @property
    def state(self):
        return self._field("state")

    @property
    def state_code(self):
        return self._field("state_code")

    @property
    def country(self):
        return self._field("country")

    @property
    def country_code(self):
        return self._field("country_code")

    @property
    def lat(self):
        return self._field("lat")

    @property
    def lng(self):
        return self._field("lng")

    @property
    def primary(self):
        return self._field("primary")

    @property
    def postcode(self):
        return self._field("postcode")


class RorLabelParser(BaseParser):

    def __init__(self, data):
        super().__init__(data)

    @property
    def label(self):
        return self._field("label")

    @property
    def iso639(self):
        return self._field("iso639")


class RorRelationshipParser(BaseParser):

    def __init__(self, data):
        super().__init__(data)

    @property
    def type(self):
        return self._field("type")

    @property
    def id(self):
        return self._field("id")

    @property
    def included(self):
        return self._field("included")


class ObjectParser(BaseParser):

    def __init__(self, data):
        super().__init__(data)

    @property
    def id(self):
        return self._field("_id")


class OrganisationParser(ObjectParser):
    """
    {
    "_id": <string>,
    "grid_id": <string>,
    "name": <string>,
    "aliases": [ <string>, <...> ],
    "acronyms": [ <string>, <...> ],
    "type": <string>,
    "address": <RorAddress>,
    "labels": <RorLabels>,
    "relationships": <RorRelationship>,
    "corresponding": <bool?>
    }
    """

    def __init__(self, data):
        super().__init__(data)

    @property
    def grid_id(self):
        return self._field("grid_id")

    @property
    def name(self):
        return self._field("name")

    @property
    def aliases(self):
        return self._field("aliases")

    @property
    def acronyms(self):
        return self._field("acronyms")

    @property
    def type(self):
        return self._field("type")

    @property
    def _address(self):
        return self._field("address")

    @property
    def address(self):
        field = self._address
        if field:
            return RorAddressParser(field)

    @property
    def _labels(self):
        return self._field("labels")

    @property
    def labels(self):
        fields = self._labels
        if isinstance(fields, list) and len(fields) > 0:
            return [RorLabelParser(lab) for lab in fields]

    @property
    def _relationships(self):
        return self._field("relationships")

    @property
    def relationships(self):
        fields = self._relationships
        if isinstance(fields, list) and len(fields) > 0:
            return [RorRelationshipParser(r) for r in fields]

    @property
    def corresponding(self):
        return self._field("corresponding")


class PublicationSourceDataParser(ObjectParser):

    def __init__(self, data):
        super().__init__(data)

    @property
    def _organisations(self):
        return self._field("organisations")

    @property
    def organisations(self):
        fields = self._organisations
        if isinstance(fields, list) and len(fields) > 0:
            return [OrganisationParser(o) for o in fields]

    @property
    def source_id(self):
        return self._field("source_id")

    @property
    def citation_count(self):
        return self._field("citation_count")

    @property
    def url(self):
        return self._field("url")


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
    def publisher(self):
        field = self._publisher
        if field:
            return PublisherParser(field)

    @property
    def _dim(self):
        return self._field("dim")

    @property
    def dim(self):
        field = self._dim
        if field:
            return PublicationSourceDataParser(field)

    @property
    def _wos(self):
        return self._field("wos")

    @property
    def wos(self):
        field = self._wos
        if field:
            return PublicationSourceDataParser(field)
