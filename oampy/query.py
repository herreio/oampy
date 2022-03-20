"""
Build queries for MongoDB-based Open Access Monitor API

For more information on the database commands, see
https://docs.mongodb.com/manual/reference/command/
"""


def filter_year(value, filter={}):
    filter["year"] = value
    return filter


def filter_year_from(value, filter={}):
    filter["year"] = {
      "$gte": value
    }
    return filter


def filter_year_until(value, filter={}):
    filter["year"] = {
      "$lte": value
    }
    return filter


def filter_published_date(value, filter={}):
    filter["published_date"] = value
    return filter


def filter_published_date_from(value, filter={}):
    filter["published_date"] = {
      "$gte": value
    }
    return filter


def filter_published_date_until(value, filter={}):
    filter["published_date"] = {
      "$lte": value
    }
    return filter


def filter_dim_organisation_ror(ror_id, filter={}):
    filter["dim.organisations._id"] = "https://ror.org/{0}".format(ror_id)
    return filter


def filter_dim_organisation_grid(grid_id, filter={}):
    filter["dim.organisations.grid_id"] = grid_id
    return filter


def filter_wos_organisation_ror(ror_id, filter={}):
    filter["wos.organisations._id"] = "https://ror.org/{0}".format(ror_id)
    return filter


def filter_wos_organisation_grid(grid_id, filter={}):
    filter["wos.organisations.grid_id"] = grid_id
    return filter


def filter_openapc_organisation_ror(ror_id, filter={}):
    filter["openapc.organisations._id"] = "https://ror.org/{0}".format(ror_id)
    return filter


def filter_openapc_organisation_grid(grid_id, filter={}):
    filter["openapc.organisations.grid_id"] = grid_id
    return filter


def filter_agreements(agreement, filter={}):
    filter["agreements"] = agreement
    return filter


def sort_asc(value):
    return {value: 1}


def sort_desc(value):
    return {value: -1}
