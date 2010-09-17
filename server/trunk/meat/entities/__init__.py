'''
Created on Sep 14, 2010

@author: skot
'''

from google.appengine.ext import db

class Measurement(db.Model):
    '''
    Measurement collected from clients
    '''
    cid = db.StringProperty(indexed=True)
    temp = db.FloatProperty()
    humid = db.FloatProperty()
    dt = db.DateTimeProperty(auto_now_add=True)
    ver = db.StringProperty()
