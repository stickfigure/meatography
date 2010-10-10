'''
Created on Sep 14, 2010

@author: skot
'''

from google.appengine.ext import db
from google.appengine.ext.db import ListProperty, StringListProperty, \
    BadValueError
from meat import KeyProperty

class Measurement(db.Expando):
    '''
    Measurement collected from clients
    '''
    cid = db.StringProperty(indexed=True)
    temp = db.FloatProperty(name="t")
    humidity = db.FloatProperty(name="h")
    when = db.DateTimeProperty(auto_now_add=True)
    ver = db.StringProperty()
 
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
