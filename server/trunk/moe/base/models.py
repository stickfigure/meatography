from google.appengine.ext import db

class Area(db.Model):
    name = db.StringProperty()
    owner = db.StringProperty()
    domains = db.StringListProperty()
    
    @classmethod
    def get_by_domain(self, domain):
        return Area.all().filter("domains", domain).fetch(1)
    