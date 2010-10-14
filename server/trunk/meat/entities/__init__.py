'''
Created on Sep 14, 2010

@author: skot
'''

from google.appengine.ext import db
from google.appengine.ext.db import ListProperty, StringListProperty, \
    BadValueError

class Measurement(db.Expando):
    '''
    Measurement collected from clients
    '''
    cid = db.StringProperty(indexed=True)
    temp = db.FloatProperty(name="t")
    humidity = db.FloatProperty(name="h")
    when = db.DateTimeProperty(auto_now_add=True)
    ver = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    
    def kind(self):
        return "m"
    
    ''' Kind name to store in the datastore '''
    kind = classmethod(kind)

class Account(db.Expando):
    '''
    An account maps logins to Measurement.cid(s)
    '''
    cids = ListProperty(db.Key)
    logins = ListProperty(db.Key)


def measurements_list_pager(cursor=None, limit=20):
    def get_query(keys_only=False, cursor=None):
        query = Measurement.all(keys_only=keys_only) \
                        .order('-when')

        if cursor is not None:
            query.with_cursor(cursor)

        return query

    query = get_query(cursor=cursor)
    entities = query.fetch(limit)

    if not entities:
        query_cursor = None
    else:
        query_cursor = query.cursor()

        # Check if we have "next" results.
        res = get_query(keys_only=True, cursor=query_cursor).get()
        if res is None:
            query_cursor = None

    return entities, query_cursor