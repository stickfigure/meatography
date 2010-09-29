# -*- coding: utf-8 -*-
"""
    urls
"""
from tipfy import Rule

def get_rules():
    rules = [
        Rule('/', endpoint='measurements-index', handler='meat.handlers.ListRawMeasurements'),
        Rule('/measurements', endpoint='measurements', handler='meat.handlers.ListRawMeasurements'),
        Rule('/submit', endpoint='new-measurement', handler='meat.handlers.NewMeasurement'),
        Rule('/test', endpoint='new-measurement', handler='meat.handlers.ResultStub'),
    ]

    return rules
