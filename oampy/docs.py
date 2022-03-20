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
        self._delim = "|"

    @property
    def title(self):
        return self._field("title")

    @property
    def issns(self):
        return self._field("issns")

    def get_issns(self, joined=True):
        issns = self.issns
        if isinstance(issns, list) and len(issns) > 0:
            if joined:
                return self._delim.join(issns)
            return issns

    @property
    def flags(self):
        return self._field("flags")

    def get_flags(self, joined=True):
        flags = self.flags
        if isinstance(flags, list) and len(flags) > 0:
            if joined:
                return self._delim.join(flags)
            return flags

    @property
    def agreements(self):
        return self._field("agreements")

    def get_agreements(self, joined=True):
        agreements = self.agreements
        if isinstance(agreements, list) and len(agreements) > 0:
            if joined:
                return self._delim.join(agreements)
            return agreements

    @property
    def csv_header(self):
        return ["id", "title", "oa_color", "issns", "agreements"]

    @property
    def csv_row(self):
        return [self.id, self.title,
                self.oa_color,
                self.get_issns() or "",
                self.get_agreements() or ""]


class PubObjectParser(OaObjectParser):

    def __init__(self, data):
        super().__init__(data)

    @property
    def _journal(self):
        return self._field("journal")

    @property
    def journal(self):
        field = self._journal
        if field:
            return JournalParser(field)

    @property
    def _publisher(self):
        return self._field("publisher")

    @property
    def publisher(self):
        field = self._publisher
        if field:
            return PublisherParser(field)

    @property
    def published_date(self):
        return self._field("published_date")


class PublicationParser(PubObjectParser):

    def __init__(self, data):
        super().__init__(data)

    @property
    def year(self):
        return self._field("year")

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


class PublicationCostsParser(PubObjectParser):

    def __init__(self, data):
        super().__init__(data)

    # @property
    # def _organisations(self):
    #     return self._field("organisations")

    # @property
    # def organisations(self):
    #     fields = self._organisations
    #     if isinstance(fields, list) and len(fields) > 0:
    #         return [OrganisationParser(o) for o in fields]

    @property
    def doi(self):
        return self._field("doi")

    # @property
    # def year(self):
    #     return self._field("year")

    # @property
    # def oa_charges(self):
    #     return self._field("oa_color")

    # @property
    # def apc(self):
    #     return self._field("apc")

    # @property
    # def color_charges(self):
    #     return self._field("color_charges")

    # @property
    # def cover(self):
    #     return self._field("cover")

    # @property
    # def hybrid_oa(self):
    #     return self._field("hybrid_oa")

    # @property
    # def other(self):
    #     return self._field("other")

    # @property
    # def page_charges(self):
    #     return self._field("page_charges")

    # @property
    # def publication_charges(self):
    #     return self._field("publication_charges")

    # @property
    # def reprint(self):
    #     return self._field("reprint")

    # @property
    # def submission_fee(self):
    #     return self._field("submission_fee")

    # @property
    # def total(self):
    #     return self._field("total")

    @property
    def _openapc(self):
        return self._field("openapc")

    @property
    def openapc(self):
        field = self._openapc
        if field:
            return OpenApcParser(field)


class OpenApcParser(BaseParser):

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
    def year(self):
        return self._field("year")

    @property
    def apc(self):
        return self._field("apc")

    @property
    def total(self):
        return self._field("total")
